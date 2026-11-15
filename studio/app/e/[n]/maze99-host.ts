/* Episode 99 "AI RACE #2, the maze": the page side of the sandbox. Only used by maze99.tsx.
 * Same design as race98-host.ts (/e/98).
 *
 * The pasted answer NEVER runs in this page's origin. runInSandbox() creates an
 * <iframe sandbox="allow-scripts"> (no allow-same-origin: opaque origin, so no cookies,
 * no storage, no access to this page) whose srcdoc is CONTROLLER_HTML below. Its CSP
 * (default-src 'none') blocks every network request, and the blob worker it starts
 * inherits that CSP. The pasted code runs only inside that worker
 * (public/site/ep99/runner.js, startWorker); the iframe's own thread runs the frozen
 * rules (maze.js) and the time budgets, and kills the worker when a call hangs.
 * This page only receives numbers back, checks them, and draws them. */

export type MazeResult = {
  status: "exit" | "dnf" | "error";
  steps: number;
  exitStep: number | null;
  closestDist: number;
  closestStep: number;
  invalidSteps: number;
  wallBumps: number;
  firstInvalid: string | null;
  stopReason: string | null;
  cellsVisited: number;
  extraction: string | null;
  loadError: string | null;
  p: number[]; // x0,y0,x1,y1,... one cell per step, step 0 = start
};

export const CONTROLLER_HTML = `<!doctype html><html><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline' 'unsafe-eval' blob:; worker-src blob:">
</head><body><script>
(function () {
  'use strict';
  var P = window.parent, started = false;
  function reply(m) { P.postMessage(m, '*'); }
  window.addEventListener('message', function (e) {
    if (e.source !== P || started) return;
    var d = e.data;
    if (!d || d.type !== 'run' || typeof d.nonce !== 'string') return;
    started = true;
    var nonce = d.nonce;
    try {
      var Maze = new Function('var module, exports, self = {};\\n' + d.mazeSrc + '\\n;return self.Maze;')();
      var AW = new Function('var module, exports, self = {};\\n' + d.runnerSrc + '\\n;return self.AWM99;')();
      var url = URL.createObjectURL(new Blob([d.runnerSrc + '\\n;self.AWM99.startWorker(self);'], { type: 'text/javascript' }));
      var w = new Worker(url);
      var worker = {
        send: function (m) { w.postMessage(m); },
        onReply: function (fn) { w.onmessage = function (ev) { fn(ev.data); }; w.onerror = function (ev) { ev.preventDefault(); }; },
        kill: function () { w.terminate(); URL.revokeObjectURL(url); }
      };
      var timers = {
        set: function (f, ms) { return setTimeout(f, ms); },
        clear: function (id) { clearTimeout(id); },
        now: function () { return performance.now(); }
      };
      AW.runMaze(Maze, d.maze, d.text, d.seed, worker, timers).then(function (r) {
        reply({ type: 'done', nonce: nonce, result: r });
      });
    } catch (err) {
      reply({ type: 'fail', nonce: nonce, message: String((err && err.message) || err).slice(0, 300) });
    }
  });
  reply({ type: 'ready' });
})();
</script></body></html>`;

const STATUSES = ["exit", "dnf", "error"];
const str = (v: unknown, max: number) => (typeof v === "string" ? v.slice(0, max) : null);
const int = (v: unknown, lo: number, hi: number) => (typeof v === "number" && Number.isInteger(v) && v >= lo && v <= hi ? v : null);

/** Everything that comes back from the iframe is checked here before the page uses it:
 *  only known statuses, only whole cells inside the maze (or one cell outside, the exit),
 *  only one-cell moves, bounded lengths, strings cut short. React then renders the strings
 *  as text (escaped), never as HTML. */
export function validateResult(raw: unknown, maxSteps: number, size: number): MazeResult | null {
  if (!raw || typeof raw !== "object") return null;
  const r = raw as Record<string, unknown>;
  if (typeof r.status !== "string" || !STATUSES.includes(r.status)) return null;
  const p = r.p;
  if (!Array.isArray(p) || p.length < 2 || p.length % 2 !== 0 || p.length > (maxSteps + 1) * 2) return null;
  for (const v of p) if (typeof v !== "number" || !Number.isInteger(v) || v < -1 || v > size) return null;
  const steps = int(r.steps, 0, maxSteps);
  if (steps === null || steps !== p.length / 2 - 1) return null;
  for (let i = 2; i < p.length; i += 2) {
    if (Math.abs(p[i] - p[i - 2]) + Math.abs(p[i + 1] - p[i - 1]) > 1) return null;
  }
  const closestDist = int(r.closestDist, 0, size * size);
  const closestStep = int(r.closestStep, 0, maxSteps);
  if (closestDist === null || closestStep === null) return null;
  return {
    status: r.status as MazeResult["status"],
    steps,
    exitStep: r.status === "exit" ? steps : null,
    closestDist,
    closestStep,
    invalidSteps: int(r.invalidSteps, 0, maxSteps) ?? 0,
    wallBumps: int(r.wallBumps, 0, maxSteps) ?? 0,
    firstInvalid: str(r.firstInvalid, 300),
    stopReason: str(r.stopReason, 400),
    cellsVisited: int(r.cellsVisited, 0, size * size + 1) ?? 0,
    extraction: str(r.extraction, 200),
    loadError: str(r.loadError, 800),
    p: p as number[],
  };
}

/** Runs one pasted answer in the sandbox. Rejects after `overallMs` no matter what. */
export function runInSandbox(opts: {
  text: string;
  mazeSrc: string;
  runnerSrc: string;
  maze: unknown;
  seed: number;
  maxSteps: number;
  size: number;
  overallMs?: number;
}): Promise<MazeResult> {
  return new Promise((resolve, reject) => {
    const iframe = document.createElement("iframe");
    // allow-scripts only: no allow-same-origin, allow-top-navigation, allow-popups,
    // allow-forms, allow-modals or allow-downloads
    iframe.setAttribute("sandbox", "allow-scripts");
    iframe.setAttribute("referrerpolicy", "no-referrer");
    iframe.setAttribute("aria-hidden", "true");
    iframe.setAttribute("tabindex", "-1");
    iframe.title = "sandbox";
    // not display:none (browsers slow down hidden cross-origin frames); 1 px, invisible
    iframe.style.cssText = "position:fixed;left:0;top:0;width:1px;height:1px;opacity:0;pointer-events:none;border:0";
    const nonce =
      typeof crypto !== "undefined" && "randomUUID" in crypto
        ? crypto.randomUUID()
        : String(Math.random()).slice(2) + String(Date.now());
    let settled = false;
    const cleanup = () => {
      settled = true;
      window.removeEventListener("message", onMsg);
      clearTimeout(timer);
      iframe.remove(); // ends the iframe and its worker
    };
    const timer = setTimeout(() => {
      if (settled) return;
      cleanup();
      reject(new Error("The run took too long and was stopped."));
    }, opts.overallMs ?? 60000);
    function onMsg(e: MessageEvent) {
      if (settled || e.source !== iframe.contentWindow) return;
      const d = e.data as { type?: unknown; nonce?: unknown; result?: unknown; message?: unknown } | null;
      if (!d || typeof d !== "object") return;
      if (d.type === "ready") {
        iframe.contentWindow?.postMessage(
          { type: "run", nonce, mazeSrc: opts.mazeSrc, runnerSrc: opts.runnerSrc, maze: opts.maze, text: opts.text, seed: opts.seed },
          "*", // the sandboxed frame has an opaque origin; nothing secret is in this message
        );
        return;
      }
      if (d.nonce !== nonce) return;
      if (d.type === "done") {
        const r = validateResult(d.result, opts.maxSteps, opts.size);
        cleanup();
        if (r) resolve(r);
        else reject(new Error("The sandbox sent back something that is not a maze result."));
      } else if (d.type === "fail") {
        cleanup();
        reject(new Error(typeof d.message === "string" ? d.message.slice(0, 300) : "The sandbox failed."));
      }
    }
    window.addEventListener("message", onMsg);
    iframe.srcdoc = CONTROLLER_HTML;
    document.body.appendChild(iframe);
  });
}

/** Same order as run_maze.mjs: dots that got out by steps, then the rest by how close they came
 *  to the exit, then who got there first. */
export function orderBots<T extends { status: string; exitStep: number | null; closestDist: number; closestStep: number }>(bots: T[]): T[] {
  return bots.slice().sort((a, b) => {
    if ((a.status === "exit") !== (b.status === "exit")) return a.status === "exit" ? -1 : 1;
    if (a.status === "exit") return (a.exitStep ?? 0) - (b.exitStep ?? 0);
    if (a.closestDist !== b.closestDist) return a.closestDist - b.closestDist;
    return a.closestStep - b.closestStep;
  });
}

/** sha256 of a text as hex, or null where the browser has no crypto.subtle (http pages). */
export async function sha256Hex(text: string): Promise<string | null> {
  try {
    if (typeof crypto === "undefined" || !crypto.subtle) return null;
    const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
    return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join("");
  } catch {
    return null;
  }
}
