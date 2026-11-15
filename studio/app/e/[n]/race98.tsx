"use client";

/* Episode 98 only: the playable AI race on /e/98.
 *
 * - The five real cars are replayed from public/site/ep98/race.json: positions copied
 *   from the real race (video/ep98/arena/run_race.mjs), not simulated again here.
 * - "Add my AI" runs a pasted answer in a sandboxed iframe + worker (race98-host.ts,
 *   public/site/ep98/runner.js). The pasted code never runs in this page's origin,
 *   and nothing is uploaded or saved.
 * How race.json is made, and the security notes: channel/episode-98-page-notes.md. */

import { useCallback, useEffect, useRef, useState } from "react";
import { orderCars, runInSandbox, sha256Hex, type RunResult } from "./race98-host";
import s from "./race98.module.css";

const BASE = "/site/ep98/";
const W = 950;
const H = 808;
const VISITOR_SEED = 1005; // the five real cars used 1000-1004 (run order)

/** PROMPT A, word for word: the request every AI got (channel/episode-98-plan.md). */
const PROMPT_A = `Write one JavaScript function for a racing game. Reply with only the code.

function steer(s) { ... }

The game calls it 60 times a second. s has these numbers:
s.front, s.left, s.right: distance in pixels from the car to the wall,
straight ahead, 45 degrees left and 45 degrees right (0 to 400).
s.speed: the car's speed, 0 to 10.
Return { turn, gas }: turn from -1 (full left) to 1 (full right), gas from 0 to 1.
Gas under 0.2 brakes. The car is 20 pixels wide. The road is 90 to 140 pixels wide
and has one hairpin. Touching a wall ends the race for that car.
Goal: finish 2 laps as fast as you can. No libraries.`;

const COLORS: Record<string, string> = {
  chatgpt: "#0B0B0B",
  gemini: "#4E7BF0",
  claude: "#D97757",
  meta: "#A23BD6",
  perplexity: "#20808D",
  you: "#FFE600",
};

type Car = {
  id: string;
  label: string;
  status: string;
  endFrame: number;
  finishFrame: number | null;
  stopFrame: number | null;
  stopReason: string | null;
  stopSector: string | null;
  progressLaps: number;
  lapFrames: number[];
  answer: string;
  f: number[];
  mine?: boolean;
};
type RaceFile = { fps: number; maxFrames: number; arenaSha256: string; trackSha256: string; cars: Car[] };
type Track = { leftEdge: [number, number][]; rightEdge: [number, number][] };

const sec = (frame: number) => (frame / 60).toFixed(2);

function finalText(c: Car): string {
  if (c.status === "finish" && c.finishFrame != null) return `Finished 2 laps in ${sec(c.finishFrame)} s`;
  if (c.status === "wall") return `Touched the wall${c.stopSector ? ` in the ${c.stopSector}` : ""} at ${sec(c.stopFrame ?? c.endFrame)} s`;
  if (c.status === "dnf") return `Did not finish: still${c.stopSector ? ` in the ${c.stopSector}` : " driving"} at the 60 s limit`;
  if (c.status === "error") {
    const why = (c.stopReason || "").replace(/^did not start: /, "");
    return (c.stopReason || "").startsWith("did not start")
      ? `Did not start: ${why}`
      : `Stopped at ${sec(c.stopFrame ?? c.endFrame)} s: ${why}`;
  }
  return "Driving";
}

function textAt(c: Car, k: number, ended: boolean): string {
  if (k >= c.endFrame || (ended && c.status !== "run")) return finalText(c);
  const laps = c.lapFrames.filter((x) => x <= k).length;
  return `Lap ${Math.min(laps + 1, 2)} of 2`;
}

/** Where the replay stops: a little after the last car whose race is decided. */
function viewEnd(cars: Car[], maxFrames: number): number {
  let m = 0;
  for (const c of cars) {
    if (c.status === "finish" && c.finishFrame != null) m = Math.max(m, c.finishFrame);
    else if ((c.status === "wall" || c.status === "error") && c.stopFrame != null) m = Math.max(m, c.stopFrame);
  }
  return m ? Math.min(maxFrames, m + 90) : maxFrames;
}

export default function Race98() {
  const [race, setRace] = useState<RaceFile | null>(null);
  const [track, setTrack] = useState<Track | null>(null);
  const [trackText, setTrackText] = useState("");
  const [loadErr, setLoadErr] = useState("");
  const [cars, setCars] = useState<Car[]>([]);
  const [frame, setFrame] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [open, setOpen] = useState<Record<string, boolean>>({});
  const [copied, setCopied] = useState(false);
  const [adding, setAdding] = useState(false);
  const [pasted, setPasted] = useState("");
  const [busy, setBusy] = useState(false);
  const [runMsg, setRunMsg] = useState("");
  const canvas = useRef<HTMLCanvasElement>(null);
  const raf = useRef(0);
  const clock = useRef({ t0: 0, f0: 0 });
  const srcCache = useRef<{ arena: string; runner: string } | null>(null);

  useEffect(() => {
    let dead = false;
    Promise.all([
      fetch(BASE + "race.json").then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status))))),
      fetch(BASE + "track.json").then((r) => (r.ok ? r.text() : Promise.reject(new Error(String(r.status))))),
    ])
      .then(([rc, tt]: [RaceFile, string]) => {
        if (dead) return;
        setRace(rc);
        setCars(rc.cars);
        setTrackText(tt);
        setTrack(JSON.parse(tt));
      })
      .catch(() => !dead && setLoadErr("The race could not be loaded. Reload the page to try again."));
    return () => {
      dead = true;
    };
  }, []);

  const end = race ? viewEnd(cars, race.maxFrames) : 0;

  const draw = useCallback(
    (k: number) => {
      const cv = canvas.current;
      if (!cv || !track) return;
      const cssW = cv.clientWidth || 360;
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      const pxW = Math.round(cssW * dpr);
      const pxH = Math.round((cssW * H) / W * dpr);
      if (cv.width !== pxW || cv.height !== pxH) {
        cv.width = pxW;
        cv.height = pxH;
      }
      const g = cv.getContext("2d");
      if (!g) return;
      const sc = pxW / W;
      g.setTransform(1, 0, 0, 1, 0, 0);
      g.fillStyle = "#FFFFFF";
      g.fillRect(0, 0, pxW, pxH);
      g.setTransform(sc, 0, 0, sc, 0, 0);
      // the road between the two edges
      const poly = (p: [number, number][]) => {
        g.moveTo(p[0][0], p[0][1]);
        for (let i = 1; i < p.length; i++) g.lineTo(p[i][0], p[i][1]);
        g.closePath();
      };
      g.beginPath();
      poly(track.leftEdge);
      poly(track.rightEdge);
      g.fillStyle = "#EDEDED";
      g.fill("evenodd");
      g.lineWidth = 2.5;
      g.strokeStyle = "#0B0B0B";
      g.stroke();
      // start / finish line
      const a = track.leftEdge[0], b = track.rightEdge[0];
      g.beginPath();
      g.moveTo(a[0], a[1]);
      g.lineTo(b[0], b[1]);
      g.lineWidth = 6;
      g.strokeStyle = "#FFE600";
      g.stroke();
      g.setLineDash([6, 6]);
      g.lineWidth = 6;
      g.strokeStyle = "#0B0B0B";
      g.stroke();
      g.setLineDash([]);
      // ink trails, then the cars on top
      for (const c of cars) {
        const n = Math.min(k, c.endFrame);
        if (n < 1) continue;
        g.beginPath();
        g.moveTo(c.f[0], c.f[1]);
        for (let i = 1; i <= n; i++) g.lineTo(c.f[3 * i], c.f[3 * i + 1]);
        g.globalAlpha = 0.35;
        g.lineWidth = 2;
        g.strokeStyle = c.id === "you" ? "#B8A600" : COLORS[c.id] || "#666";
        g.stroke();
        g.globalAlpha = 1;
      }
      for (const c of cars) {
        const i = Math.min(k, c.endFrame);
        const x = c.f[3 * i], y = c.f[3 * i + 1], ang = c.f[3 * i + 2];
        const out = i >= c.endFrame && (c.status === "wall" || c.status === "error");
        g.save();
        g.translate(x, y);
        g.rotate(ang);
        g.globalAlpha = out ? 0.45 : 1;
        g.fillStyle = COLORS[c.id] || "#666";
        g.fillRect(-17, -10, 34, 20);
        g.lineWidth = 2;
        g.strokeStyle = "#0B0B0B";
        g.strokeRect(-17, -10, 34, 20);
        g.fillStyle = c.id === "you" ? "#0B0B0B" : "#FFFFFF";
        g.fillRect(9, -7, 5, 14); // windscreen: shows which way the car faces
        g.restore();
      }
      g.globalAlpha = 1;
    },
    [track, cars],
  );

  useEffect(() => {
    draw(frame);
  }, [draw, frame]);

  useEffect(() => {
    const onResize = () => draw(frame);
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, [draw, frame]);

  useEffect(() => {
    if (!playing) return;
    const tick = (now: number) => {
      const k = Math.min(end, Math.floor(clock.current.f0 + ((now - clock.current.t0) / 1000) * 60));
      setFrame(k);
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
    const f0 = from ?? (frame >= end ? 0 : frame);
    clock.current = { t0: performance.now(), f0 };
    setFrame(f0);
    setPlaying(true);
  };

  const copyRequest = async () => {
    try {
      await navigator.clipboard.writeText(PROMPT_A);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch {
      setCopied(false);
      const pre = document.getElementById("ep98-request-text");
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
    setRunMsg("Racing your car. The code runs only in this browser tab.");
    try {
      if (!srcCache.current) {
        const [arena, runner] = await Promise.all([
          fetch(BASE + "arena.js").then((r) => (r.ok ? r.text() : Promise.reject(new Error("arena")))),
          fetch(BASE + "runner.js").then((r) => (r.ok ? r.text() : Promise.reject(new Error("runner")))),
        ]);
        const [ha, ht] = await Promise.all([sha256Hex(arena), sha256Hex(trackText)]);
        if ((ha && ha !== race.arenaSha256) || (ht && ht !== race.trackSha256)) {
          throw new Error("The road or the physics file is not the one the race used, so this run was not started.");
        }
        srcCache.current = { arena, runner };
      }
      const r: RunResult = await runInSandbox({
        text: pasted,
        arenaSrc: srcCache.current.arena,
        runnerSrc: srcCache.current.runner,
        track: JSON.parse(trackText),
        seed: VISITOR_SEED,
        maxFrames: race.maxFrames,
      });
      const mine: Car = {
        id: "you",
        label: "Your AI",
        status: r.status,
        endFrame: r.endFrame,
        finishFrame: r.finishFrame,
        stopFrame: r.stopFrame,
        stopReason: r.stopReason,
        stopSector: r.stopSector,
        progressLaps: r.progressLaps,
        lapFrames: r.lapFrames,
        answer: pasted,
        f: r.f,
        mine: true,
      };
      setCars([...race.cars, mine]);
      setRunMsg(
        mine.status === "error"
          ? `Your car: ${finalText(mine)}. That is the real result of this code; the list under the road shows it too.`
          : `Your car: ${finalText(mine)}. Watch it race the other five.`,
      );
      setTimeout(() => {
        clock.current = { t0: performance.now(), f0: 0 };
        setFrame(0);
        setPlaying(true);
        document.getElementById("ep98-race")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 50);
    } catch (e) {
      setRunMsg(e instanceof Error ? e.message : "The run failed.");
    } finally {
      setBusy(false);
    }
  };

  const ended = frame >= end && end > 0;
  const results = orderCars(cars);

  return (
    <>
      <section id="ep98-race" className={s.wrap}>
        <h2>The race</h2>
        <p className="sub">
          The five real answers on the road from the video, at true speed. The positions come straight from our
          recorded race; nothing is re-run here.
        </p>
        {loadErr ? <p className="empty">{loadErr}</p> : null}
        <div className={s.stage}>
          <canvas ref={canvas} className={s.canvas} role="img" aria-label="Top view of the road with the cars racing" />
          {!race && !loadErr ? <p className={s.loading}>Loading the race…</p> : null}
        </div>
        <div className={s.controls}>
          <button
            type="button"
            className="button solid"
            disabled={!race}
            onClick={() => (playing ? setPlaying(false) : play())}
          >
            {playing ? "Pause" : "Play the race"}
          </button>
          <span className={s.clock} aria-live="off">
            {sec(frame)} s
          </span>
        </div>
        <input
          className={s.scrub}
          type="range"
          min={0}
          max={end || 1}
          value={Math.min(frame, end)}
          aria-label="Race time"
          disabled={!race}
          onChange={(e) => {
            setPlaying(false);
            setFrame(Number(e.target.value));
          }}
        />
        <ul className={s.cars}>
          {cars.map((c) => (
            <li key={c.id} className={s.car}>
              <div className={s.carHead}>
                <span className={s.swatch} style={{ background: COLORS[c.id] || "#666" }} aria-hidden="true" />
                <span className={s.name}>{c.label}</span>
                <button
                  type="button"
                  className={s.link}
                  aria-expanded={!!open[c.id]}
                  onClick={() => setOpen((o) => ({ ...o, [c.id]: !o[c.id] }))}
                >
                  {open[c.id] ? "Hide code" : "Show code"}
                </button>
              </div>
              <div className={s.status}>{textAt(c, frame, ended)}</div>
              {open[c.id] ? (
                <pre className={`body ${s.code}`}>{c.answer}</pre>
              ) : null}
            </li>
          ))}
        </ul>
        {ended ? (
          <div className="note">
            <div className="t">Result</div>
            <ol className={s.results}>
              {results.map((c) => (
                <li key={c.id}>
                  <b>{c.label}</b>: {finalText(c)}
                </li>
              ))}
            </ol>
            {cars.some((c) => c.status === "dnf") ? (
              <p className="fine">
                The replay stops shortly after the last decided car. A car marked &quot;did not finish&quot; keeps
                driving without getting round until the race gives up at 60 s.
              </p>
            ) : null}
          </div>
        ) : null}
      </section>

      <section id="ep98-request">
        <h2>The request</h2>
        <p className="sub">Every AI got exactly this, once, in a new chat. Nothing was fixed in the answers.</p>
        <pre className="body" id="ep98-request-text">
          {PROMPT_A}
        </pre>
        <div className="actions">
          <button type="button" className="button" onClick={copyRequest}>
            {copied ? "Copied" : "Copy the request"}
          </button>
        </div>
      </section>

      <section id="ep98-add">
        <h2>Race your own AI</h2>
        <p className="sub">
          Paste the answer your AI gave to the request above. Your car joins the same road as a sixth car. The code
          runs only inside a locked-down box in this browser tab: it cannot see this page, cannot reach the
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
            <label htmlFor="ep98-paste" className={s.label}>
              Your AI&apos;s whole answer
            </label>
            <textarea
              id="ep98-paste"
              className={s.paste}
              value={pasted}
              maxLength={100000}
              spellCheck={false}
              autoCapitalize="off"
              autoCorrect="off"
              placeholder="function steer(s) { ... }"
              onChange={(e) => setPasted(e.target.value)}
            />
            <div className="actions">
              <button type="button" className="button solid" disabled={busy} onClick={raceMine}>
                {busy ? "Racing…" : "Race"}
              </button>
              {cars.some((c) => c.mine) ? (
                <button
                  type="button"
                  className="button"
                  disabled={busy}
                  onClick={() => {
                    if (race) setCars(race.cars);
                    setRunMsg("");
                    setFrame(0);
                    setPlaying(false);
                  }}
                >
                  Remove my car
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
