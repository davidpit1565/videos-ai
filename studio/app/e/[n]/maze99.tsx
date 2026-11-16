"use client";

/* Episode 99 only: the playable maze race on /e/99 (AI RACE #2). Modelled on race98.tsx.
 *
 * - The dots in race.json are replayed from the real race (video/ep99/arena/run_maze.mjs):
 *   cells copied from the real run, not simulated again here. Until the five AI answers have
 *   been run, race.json holds only our two reference bots and says so (placeholder: true).
 * - "Add my AI" runs a pasted answer in a sandboxed iframe + worker (maze99-host.ts,
 *   public/site/ep99/runner.js). The pasted code never runs in this page's origin,
 *   and nothing is uploaded or saved.
 * How race.json is made, and the security notes: channel/episode-99-page-notes.md. */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { orderBots, runInSandbox, sha256Hex, type MazeResult } from "./maze99-host";
import s from "./maze99.module.css";

const BASE = "/site/ep99/";
const SIZE = 21; // cells per side
const UNIT = 40; // canvas px per cell; the canvas has a one-cell margin all round
const PX = (SIZE + 2) * UNIT;
const SPEED = 30; // steps per second in the replay
const VISITOR_SEED = 1005; // the five AIs use 1000-1004 (run order)

/** PROMPT B, word for word: the request every AI gets (video/ep99/arena/PROMPT-B.txt). */
const PROMPT_B = `Write one JavaScript function for a maze game. Reply with only the code.

function move(v) { ... }

A dot starts in the middle of a 21 x 21 maze and must find the way out.
The game calls move once per step. v has:
v.up, v.down, v.left, v.right: what is next to the dot on that side,
"wall", "open" or "exit" ("exit" means that move leaves the maze).
v.x, v.y: the dot's own cell, x 0 to 20 from left to right,
y 0 to 20 from top to bottom. The dot starts at x 10, y 10.
Return "up", "down", "left" or "right". Up is y minus 1, right is x plus 1.
Anything else, or a move into a wall, keeps the dot where it is for that step.
The exit is one gap in the outer wall. The maze has dead ends and loops.
You never see the maze, only the four sides of the dot.
Your code may keep its own memory between calls. You get 500 steps.
Goal: reach the exit in as few steps as possible. No libraries.`;

const COLORS: Record<string, string> = {
  chatgpt: "#0B0B0B",
  gemini: "#4E7BF0",
  claude: "#D97757",
  meta: "#A23BD6",
  perplexity: "#20808D",
  careful: "#6B6B6B",
  naive: "#B0B0B0",
  you: "#FFE600",
};

type Bot = {
  id: string;
  label: string;
  reference?: boolean;
  status: string;
  steps: number;
  exitStep: number | null;
  closestDist: number;
  closestStep: number;
  wallBumps: number;
  invalidSteps: number;
  firstInvalid: string | null;
  stopReason: string | null;
  cellsVisited: number;
  p: number[];
  mine?: boolean;
};
type RaceFile = {
  placeholder?: boolean;
  note?: string;
  mazeJsSha256: string;
  mazeJsonSha256: string;
  maxSteps: number;
  shortestSteps: number;
  cars: Bot[];
};
type MazeJson = { width: number; height: number; open: string[]; exit: { x: number; y: number }; start: { x: number; y: number } };
type MazeApi = { prepareMaze: (m: MazeJson) => { dist: number[][]; open: number[][] } };

const color = (id: string) => COLORS[id] || "#666666";

function finalText(c: Bot): string {
  if (c.status === "exit") return `Out after ${c.exitStep ?? c.steps} steps`;
  if (c.status === "dnf") return `Did not get out: still inside after ${c.steps} steps`;
  if (c.status === "error") {
    const why = (c.stopReason || "").replace(/^did not start: /, "");
    return (c.stopReason || "").startsWith("did not start") ? `Did not start: ${why}` : `Stopped at step ${c.steps}: ${why}`;
  }
  return "Walking";
}

function loadMazeScript(): Promise<MazeApi> {
  const w = window as unknown as { Maze?: MazeApi };
  if (w.Maze) return Promise.resolve(w.Maze);
  return new Promise((resolve, reject) => {
    const el = document.createElement("script");
    el.src = BASE + "maze.js";
    el.onload = () => (w.Maze ? resolve(w.Maze) : reject(new Error("maze")));
    el.onerror = () => reject(new Error("maze"));
    document.head.appendChild(el);
  });
}

export default function Maze99() {
  const [race, setRace] = useState<RaceFile | null>(null);
  const [mazeText, setMazeText] = useState("");
  const [mazeDist, setMazeDist] = useState<number[][] | null>(null);
  const [mazeOpen, setMazeOpen] = useState<number[][] | null>(null);
  const [loadErr, setLoadErr] = useState("");
  const [bots, setBots] = useState<Bot[]>([]);
  const [step, setStep] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [copied, setCopied] = useState(false);
  const [adding, setAdding] = useState(false);
  const [pasted, setPasted] = useState("");
  const [busy, setBusy] = useState(false);
  const [runMsg, setRunMsg] = useState("");
  const canvas = useRef<HTMLCanvasElement>(null);
  const raf = useRef(0);
  const clock = useRef({ t0: 0, s0: 0 });
  const srcCache = useRef<{ maze: string; runner: string } | null>(null);

  useEffect(() => {
    let dead = false;
    Promise.all([
      fetch(BASE + "race.json").then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status))))),
      fetch(BASE + "maze.json").then((r) => (r.ok ? r.text() : Promise.reject(new Error(String(r.status))))),
      loadMazeScript(),
    ])
      .then(([rc, mt, Maze]: [RaceFile, string, MazeApi]) => {
        if (dead) return;
        const M = Maze.prepareMaze(JSON.parse(mt));
        setMazeDist(M.dist);
        setMazeOpen(M.open);
        setMazeText(mt);
        setRace(rc);
        setBots(rc.cars);
      })
      .catch(() => !dead && setLoadErr("The maze could not be loaded. Reload the page to try again."));
    return () => {
      dead = true;
    };
  }, []);

  // closest walking distance to the exit reached by step k, per bot (a cell outside the maze = 0)
  const closest = useMemo(() => {
    const out: Record<string, number[]> = {};
    if (!mazeDist) return out;
    for (const b of bots) {
      const arr: number[] = [];
      let m = Infinity;
      for (let i = 0; i <= b.steps; i++) {
        const x = b.p[2 * i], y = b.p[2 * i + 1];
        const d = x < 0 || y < 0 || x >= SIZE || y >= SIZE ? 0 : mazeDist[y][x];
        if (d < m) m = d;
        arr.push(m);
      }
      out[b.id] = arr;
    }
    return out;
  }, [bots, mazeDist]);

  const end = bots.reduce((m, b) => Math.max(m, b.steps), 0);

  const draw = useCallback(
    (k: number) => {
      const cv = canvas.current;
      if (!cv || !mazeOpen) return;
      const cssW = cv.clientWidth || 360;
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      const pxW = Math.round(cssW * dpr);
      if (cv.width !== pxW || cv.height !== pxW) {
        cv.width = pxW;
        cv.height = pxW;
      }
      const g = cv.getContext("2d");
      if (!g) return;
      g.setTransform(1, 0, 0, 1, 0, 0);
      g.fillStyle = "#FFFFFF";
      g.fillRect(0, 0, pxW, pxW);
      g.setTransform(pxW / PX, 0, 0, pxW / PX, 0, 0);
      const cx = (x: number) => (x + 1.5) * UNIT; // centre of cell x (x = -1 is the exit cell outside)
      const cy = (y: number) => (y + 1.5) * UNIT;
      // floor
      g.fillStyle = "#F2F2F2";
      g.fillRect(UNIT, UNIT, SIZE * UNIT, SIZE * UNIT);
      // the way out: a yellow cell in the margin on the exit side
      g.fillStyle = "#FFE600";
      g.fillRect(0, UNIT * 21, UNIT, UNIT);
      g.fillStyle = "#0B0B0B";
      g.font = `700 ${Math.round(UNIT * 0.3)}px sans-serif`;
      g.textAlign = "center";
      g.textBaseline = "middle";
      g.fillText("EXIT", UNIT * 0.5, UNIT * 21.5);
      // start ring
      g.beginPath();
      g.arc(cx(10), cy(10), UNIT * 0.42, 0, Math.PI * 2);
      g.lineWidth = 2;
      g.setLineDash([4, 4]);
      g.strokeStyle = "#0B0B0B";
      g.stroke();
      g.setLineDash([]);
      // walls: every side of a cell without its "open" bit
      g.beginPath();
      for (let y = 0; y < SIZE; y++) {
        for (let x = 0; x < SIZE; x++) {
          const o = mazeOpen[y][x];
          const x0 = (x + 1) * UNIT, y0 = (y + 1) * UNIT, x1 = x0 + UNIT, y1 = y0 + UNIT;
          if (!(o & 1)) { g.moveTo(x0, y0); g.lineTo(x1, y0); }
          if (!(o & 4)) { g.moveTo(x0, y1); g.lineTo(x1, y1); }
          if (!(o & 8)) { g.moveTo(x0, y0); g.lineTo(x0, y1); }
          if (!(o & 2)) { g.moveTo(x1, y0); g.lineTo(x1, y1); }
        }
      }
      g.lineWidth = 4;
      g.lineCap = "round";
      g.strokeStyle = "#0B0B0B";
      g.stroke();
      // ink trails
      bots.forEach((b, i) => {
        const n = Math.min(k, b.steps);
        if (n < 1) return;
        const off = ((i % 3) - 1) * 3;
        g.beginPath();
        g.moveTo(cx(b.p[0]) + off, cy(b.p[1]) + off);
        for (let j = 1; j <= n; j++) g.lineTo(cx(b.p[2 * j]) + off, cy(b.p[2 * j + 1]) + off);
        g.globalAlpha = 0.45;
        g.lineWidth = 4;
        g.lineJoin = "round";
        g.strokeStyle = b.id === "you" ? "#B8A600" : color(b.id);
        g.stroke();
        g.globalAlpha = 1;
      });
      // the dots on top
      bots.forEach((b, i) => {
        const j = Math.min(k, b.steps);
        const off = ((i % 3) - 1) * 3;
        const x = cx(b.p[2 * j]) + off, y = cy(b.p[2 * j + 1]) + off;
        g.globalAlpha = j >= b.steps && b.status === "error" ? 0.45 : 1;
        g.beginPath();
        g.arc(x, y, UNIT * 0.3, 0, Math.PI * 2);
        g.fillStyle = color(b.id);
        g.fill();
        g.lineWidth = 2.5;
        g.strokeStyle = "#0B0B0B";
        g.stroke();
      });
      g.globalAlpha = 1;
    },
    [mazeOpen, bots],
  );

  useEffect(() => {
    draw(step);
  }, [draw, step]);

  useEffect(() => {
    const onResize = () => draw(step);
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, [draw, step]);

  useEffect(() => {
    if (!playing) return;
    const tick = (now: number) => {
      const k = Math.min(end, Math.floor(clock.current.s0 + ((now - clock.current.t0) / 1000) * SPEED));
      setStep(k);
      if (k >= end) {
        setPlaying(false);
        return;
      }
      raf.current = requestAnimationFrame(tick);
    };
    raf.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf.current);
  }, [playing, end]);

  const play = (from?: number) => {
    const s0 = from ?? (step >= end ? 0 : step);
    clock.current = { t0: performance.now(), s0 };
    setStep(s0);
    setPlaying(true);
  };

  const copyRequest = async () => {
    try {
      await navigator.clipboard.writeText(PROMPT_B);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch {
      setCopied(false);
      const pre = document.getElementById("ep99-request-text");
      if (pre) window.getSelection()?.selectAllChildren(pre);
    }
  };

  const raceMine = async () => {
    if (!race || busy) return;
    const text = pasted.trim();
    if (!text) {
      setRunMsg("Paste your AI's answer into the box first.");
      return;
    }
    setBusy(true);
    setPlaying(false);
    setRunMsg("Running your dot. The code runs only in this browser tab.");
    try {
      if (!srcCache.current) {
        const [maze, runner] = await Promise.all([
          fetch(BASE + "maze.js").then((r) => (r.ok ? r.text() : Promise.reject(new Error("maze")))),
          fetch(BASE + "runner.js").then((r) => (r.ok ? r.text() : Promise.reject(new Error("runner")))),
        ]);
        const [hm, hj] = await Promise.all([sha256Hex(maze), sha256Hex(mazeText)]);
        if ((hm && hm !== race.mazeJsSha256) || (hj && hj !== race.mazeJsonSha256)) {
          throw new Error("The maze or the rules file is not the one the race used, so this run was not started.");
        }
        srcCache.current = { maze, runner };
      }
      const r: MazeResult = await runInSandbox({
        text: pasted,
        mazeSrc: srcCache.current.maze,
        runnerSrc: srcCache.current.runner,
        maze: JSON.parse(mazeText),
        seed: VISITOR_SEED,
        maxSteps: race.maxSteps,
        size: SIZE,
      });
      const mine: Bot = {
        id: "you",
        label: "Your AI",
        status: r.status,
        steps: r.steps,
        exitStep: r.exitStep,
        closestDist: r.closestDist,
        closestStep: r.closestStep,
        wallBumps: r.wallBumps,
        invalidSteps: r.invalidSteps,
        firstInvalid: r.firstInvalid,
        stopReason: r.stopReason,
        cellsVisited: r.cellsVisited,
        p: r.p,
        mine: true,
      };
      setBots([...race.cars, mine]);
      setRunMsg(
        mine.status === "error"
          ? `Your dot: ${finalText(mine)}. That is the real result of this code; the list under the maze shows it too.`
          : `Your dot: ${finalText(mine)}. Watch it walk next to the others.`,
      );
      setTimeout(() => {
        clock.current = { t0: performance.now(), s0: 0 };
        setStep(0);
        setPlaying(true);
        document.getElementById("ep99-race")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 50);
    } catch (e) {
      setRunMsg(e instanceof Error ? e.message : "The run failed.");
    } finally {
      setBusy(false);
    }
  };

  const ended = step >= end && end > 0;
  const results = orderBots(bots);

  const liveText = (b: Bot): string => {
    if (step >= b.steps) return finalText(b);
    return `Step ${step} of ${race?.maxSteps ?? 500}`;
  };
  const liveNums = (b: Bot): string => {
    const k = Math.min(step, b.steps);
    const c = closest[b.id]?.[k];
    const done = step >= b.steps;
    const closeTxt = c === undefined ? "" : c === 0 ? "closest: out" : `closest: ${c} steps from the exit`;
    return `steps ${k}${done ? "" : " so far"} · ${closeTxt}`;
  };

  return (
    <>
      <section id="ep99-race" className={s.wrap}>
        <h2>The maze</h2>
        <p className="sub">
          Every AI gets the same maze and sees only the four sides of its own dot. Each dot walks the maze below
          at 30 steps a second. The cells come straight from our recorded run; nothing is re-run here.
          {race ? ` The shortest way out is ${race.shortestSteps} steps.` : ""}
        </p>
        {race?.placeholder ? (
          <div className="note">
            <div className="t">Reference dots only, for now</div>
            <p className="fine">
              The two dots below are our own reference programs, not AIs: one with no memory, one that remembers
              where it has been. They show what the numbers mean. The five AI results are added after the race.
            </p>
          </div>
        ) : null}
        {loadErr ? <p className="empty">{loadErr}</p> : null}
        <div className={s.stage}>
          <canvas ref={canvas} className={s.canvas} role="img" aria-label="Top view of the maze with the dots walking" />
          {!race && !loadErr ? <p className={s.loading}>Loading the maze…</p> : null}
        </div>
        <div className={s.controls}>
          <button
            type="button"
            className="button solid"
            disabled={!race}
            onClick={() => (playing ? setPlaying(false) : play())}
          >
            {playing ? "Pause" : "Play the maze"}
          </button>
          <span className={s.clock} aria-live="off">
            step {Math.min(step, end)}
          </span>
        </div>
        <input
          className={s.scrub}
          type="range"
          min={0}
          max={end || 1}
          value={Math.min(step, end)}
          aria-label="Step"
          disabled={!race}
          onChange={(e) => {
            setPlaying(false);
            setStep(Number(e.target.value));
          }}
        />
        <ul className={s.cars}>
          {bots.map((b) => (
            <li key={b.id} className={s.car}>
              <div className={s.carHead}>
                <span className={s.swatch} style={{ background: color(b.id) }} aria-hidden="true" />
                <span className={s.name}>{b.label}</span>
              </div>
              <div className={s.status}>{liveText(b)}</div>
              <div className={s.nums}>{liveNums(b)}</div>
            </li>
          ))}
        </ul>
        {ended ? (
          <div className="note">
            <div className="t">Result</div>
            <ol className={s.results}>
              {results.map((b) => (
                <li key={b.id}>
                  <b>{b.label}</b>:{" "}
                  {b.status === "exit"
                    ? `out after ${b.exitStep} steps`
                    : `${finalText(b).toLowerCase()}, closest ${b.closestDist} steps from the exit`}
                  {b.wallBumps || b.invalidSteps
                    ? ` (${b.wallBumps} walks into a wall, ${b.invalidSteps} answers that were not a direction)`
                    : ""}
                </li>
              ))}
            </ol>
            <p className="fine">
              A dot that does not get out is ranked by how close it came to the exit, counted in steps along the
              corridors, not in a straight line.
            </p>
          </div>
        ) : null}
      </section>

      <section id="ep99-request">
        <h2>The request</h2>
        <p className="sub">Every AI gets exactly this, once, in a new chat. Nothing is fixed in the answers.</p>
        <pre className="body" id="ep99-request-text">
          {PROMPT_B}
        </pre>
        <div className="actions">
          <button type="button" className="button" onClick={copyRequest}>
            {copied ? "Copied" : "Copy the request"}
          </button>
        </div>
      </section>

      <section id="ep99-add">
        <h2>Run your own AI</h2>
        <p className="sub">
          Paste the answer your AI gave to the request above. Your dot walks the same maze next to the others. The
          code runs only inside a locked-down box in this browser tab: it cannot see this page, cannot reach the
          internet, and nothing is uploaded or saved.
        </p>
        {!adding ? (
          <div className="actions">
            <button type="button" className="button solid" onClick={() => setAdding(true)}>
              Add my AI
            </button>
          </div>
        ) : (
          <div className={s.add}>
            <label htmlFor="ep99-paste" className={s.label}>
              Your AI&apos;s whole answer
            </label>
            <textarea
              id="ep99-paste"
              className={s.paste}
              value={pasted}
              maxLength={100000}
              spellCheck={false}
              autoCapitalize="off"
              autoCorrect="off"
              placeholder="Paste the answer here"
              onChange={(e) => setPasted(e.target.value)}
            />
            <div className="actions">
              <button type="button" className="button solid" disabled={busy} onClick={raceMine}>
                {busy ? "Running…" : "Run"}
              </button>
              {bots.some((b) => b.mine) ? (
                <button
                  type="button"
                  className="button"
                  disabled={busy}
                  onClick={() => {
                    if (race) setBots(race.cars);
                    setRunMsg("");
                    setStep(0);
                    setPlaying(false);
                  }}
                >
                  Remove my dot
                </button>
              ) : null}
            </div>
          </div>
        )}
        {runMsg ? (
          <p className={s.msg} role="status">
            {runMsg}
          </p>
        ) : null}
      </section>
    </>
  );
}
