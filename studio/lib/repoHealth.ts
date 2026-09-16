import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import path from "node:path";

/** A repo-health board, in the spirit of David's own `personal-work-studio` tool: every
 *  fact here traces back to a real line in a real file (Evidence), and nothing gets
 *  invented or guessed at. Vercel's serverless functions have no live `.git` — this repo's
 *  `.git` directory isn't part of the deployment bundle, so there's no working-tree status
 *  or commit log to read at runtime, unlike `personal-work-studio` which runs locally
 *  against a real git checkout. What Vercel *does* bundle is the source tree itself, so
 *  this scans plain text for TODO/FIXME markers instead of shelling out to `git grep`.
 *
 *  Named `repoHealth`, not `health` — this repo already has a `lib/health.ts` for a
 *  completely different thing (Instagram/Beehiiv connection-drop alerts for the cron).
 *  Same word, two unrelated meanings; a shared name would have been the next place this
 *  drifted. */

export type Confidence = "confirmed" | "unknown";

export type HealthFinding = {
  /** stable across line-number churn — a hash of the file path + the marker's own text,
   *  not the line number, so an edit above it in the same file doesn't change its id and
   *  silently "resurrect" something already marked resolved. */
  id: string;
  file: string;
  line: number;
  marker: "TODO" | "FIXME";
  excerpt: string;
  confidence: Confidence;
};

/** Directories worth scanning for a real, findable TODO/FIXME — source and docs, not
 *  build output, dependencies, or binary assets. Kept short and explicit rather than
 *  "everything except node_modules": a scan that quietly grows to include, say, a future
 *  `dist/` folder is exactly the kind of drift this file exists to avoid elsewhere. */
const SCAN_ROOTS = ["studio/lib", "studio/app", "channel", "audio", "export", "video"];
const TEXT_EXTENSIONS = new Set([".ts", ".tsx", ".js", ".mjs", ".py", ".sh", ".md"]);
const SKIP_DIRS = new Set(["node_modules", ".next", ".git", "public"]);
const MAX_FILES = 2000; // a runaway scan must stop, not hang a request

async function walk(dir: string, out: string[]): Promise<void> {
  if (out.length >= MAX_FILES) return;
  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch {
    return; // directory doesn't exist in this deployment — not an error, just nothing to scan
  }
  for (const e of entries) {
    if (out.length >= MAX_FILES) return;
    if (SKIP_DIRS.has(e.name)) continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      await walk(full, out);
    } else if (TEXT_EXTENSIONS.has(path.extname(e.name))) {
      out.push(full);
    }
  }
}

const MARKER_RE = /\b(TODO|FIXME)\b:?\s*(.*)/;

function findingId(file: string, excerpt: string): string {
  return createHash("sha1").update(`${file}\n${excerpt}`).digest("hex").slice(0, 16);
}

/** The repo root as this function sees it — `studio`'s own `process.cwd()` is
 *  `studio/`, but SCAN_ROOTS are relative to the repo root one level up. */
function repoRoot(): string {
  return path.join(process.cwd(), "..");
}

export async function scanTodos(): Promise<HealthFinding[]> {
  const root = repoRoot();
  const files: string[] = [];
  for (const rel of SCAN_ROOTS) {
    await walk(path.join(root, rel), files);
  }

  const findings: HealthFinding[] = [];
  for (const file of files) {
    let text: string;
    try {
      text = await readFile(file, "utf8");
    } catch {
      continue; // unreadable (permissions, or briefly deleted mid-scan) — skip, don't fail the whole scan
    }
    const lines = text.split("\n");
    for (let i = 0; i < lines.length; i++) {
      const m = MARKER_RE.exec(lines[i]);
      if (!m) continue;
      const marker = m[1] as "TODO" | "FIXME";
      const excerpt = (m[2] || lines[i]).trim().slice(0, 200);
      const relFile = path.relative(root, file);
      findings.push({
        id: findingId(relFile, excerpt),
        file: relFile,
        line: i + 1,
        marker,
        excerpt,
        confidence: "confirmed", // a literal text match, not an inference
      });
    }
  }
  return findings;
}
