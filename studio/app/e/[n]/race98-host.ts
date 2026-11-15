/* Episode 98 "Add my AI": the page side of the sandbox. Only used by race98.tsx.
 *
 * The pasted answer NEVER runs in this page's origin. runInSandbox() creates an
 * <iframe sandbox="allow-scripts"> (no allow-same-origin: opaque origin, so no cookies,
 * no storage, no access to this page) whose srcdoc is CONTROLLER_HTML below. Its CSP
 * (default-src 'none') blocks every network request, and the blob worker it starts
 * inherits that CSP. The pasted code runs only inside that worker
 * (public/site/ep98/runner.js, startWorker); the iframe's own thread runs the frozen
 * physics (arena.js) and the time budgets, and kills the worker when a call hangs.
 * This page only receives numbers back, checks them, and draws them. */

export type RunResult = {
  status: "finish" | "wall" | "error" | "dnf" | "run";
  endFrame: number;
  finishFrame: number | null;
  stopFrame: number | null;
  stopReason: string | null;
  stopSector: string | null;
  progressLaps: number;
  lapFrames: number[];
  extraction: string | null;
  loadError: string | null;
  f: number[];
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
      var Arena = new Function('var module, exports, self = {};\\n' + d.arenaSrc + '\\n;return self.Arena;')();
      var AW = new Function('var module, exports, self = {};\\n' + d.runnerSrc + '\\n;return self.AW98;')();
      var url = URL.createObjectURL(new Blob([d.runnerSrc + '\\n;self.AW98.startWorker(self);'], { type: 'text/javascript' }));
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
      AW.runRace(Arena, d.track, d.text, d.seed, worker, timers).then(function (r) {
        reply({ type: 'done', nonce: nonce, result: r });
      });
    } catch (err) {
      reply({ type: 'fail', nonce: nonce, message: String((err && err.message) || err).slice(0, 300) });
    }
  });
  reply({ type: 'ready' });
})();
</script></body></html>`;

const STATUSES = ["finish", "wall", "error", "dnf", "run"];
const str = (v: unknown, max: number) => (typeof v === "string" ? v.slice(0, max) : null);
const int = (v: unknown) => (typeof v === "number" && Number.isInteger(v) && v >= 0 && v <= 4000 ? v : null);

/** Everything that comes back from the iframe is checked here before the page uses it:
 *  only known statuses, only finite numbers, bounded lengths, strings cut short. React
 *  then renders the strings as text (escaped), never as HTML. */
export function validateResult(raw: unknown, maxFrames: number): RunResult | null {
  if (!raw || typeof raw !== "object") return null;
  const r = raw as Record<string, unknown>;
  if (typeof r.status !== "string" || !STATUSES.includes(r.status)) return null;
  const f = r.f;
  if (!Array.isArray(f) || f.length < 3 || f.length % 3 !== 0 || f.length > (maxFrames + 2) * 3) return null;
  for (const v of f) if (typeof v !== "number" || !Number.isFinite(v) || Math.abs(v) > 1e6) return null;
  const endFrame = int(r.endFrame);
  if (endFrame === null || endFrame !== f.length / 3 - 1) return null;
  const lapFrames = Array.isArray(r.lapFrames) ? r.lapFrames.map(int).filter((x): x is number => x !== null).slice(0, 10) : [];
  const progressLaps = typeof r.progressLaps === "number" && Number.isFinite(r.progressLaps) ? r.progressLaps : 0;
  return {
    status: r.status as RunResult["status"],
    endFrame,
    finishFrame: int(r.finishFrame),
    stopFrame: int(r.stopFrame),
    stopReason: str(r.stopReason, 400),
    stopSector: str(r.stopSector, 60),
    progressLaps,
    lapFrames,
    extraction: str(r.extraction, 200),
    loadError: str(r.loadError, 800),
    f,
  };
}

/** Runs one pasted answer in the sandbox. Rejects after `overallMs` no matter what. */
export function runInSandbox(opts: {
  text: string;
  arenaSrc: string;
  runnerSrc: string;
  track: unknown;
  seed: number;
  maxFrames: number;
  overallMs?: number;
}): Promise<RunResult> {
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
          { type: "run", nonce, arenaSrc: opts.arenaSrc, runnerSrc: opts.runnerSrc, track: opts.track, text: opts.text, seed: opts.seed },
          "*", // the sandboxed frame has an opaque origin; nothing secret is in this message
        );
        return;
      }
      if (d.nonce !== nonce) return;
      if (d.type === "done") {
        const r = validateResult(d.result, opts.maxFrames);
        cleanup();
        if (r) resolve(r);
        else reject(new Error("The sandbox sent back something that is not a race result."));
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

/** Same order as run_race.mjs: finishers by time, then by distance covered, then by how long they ran. */
export function orderCars<T extends { status: string; finishFrame: number | null; progressLaps: number; stopFrame: number | null }>(cars: T[]): T[] {
  return cars.slice().sort((a, b) => {
    if ((a.status === "finish") !== (b.status === "finish")) return a.status === "finish" ? -1 : 1;
    if (a.status === "finish") return (a.finishFrame ?? 0) - (b.finishFrame ?? 0);
    if (b.progressLaps !== a.progressLaps) return b.progressLaps - a.progressLaps;
    return (b.stopFrame ?? 0) - (a.stopFrame ?? 0);
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
