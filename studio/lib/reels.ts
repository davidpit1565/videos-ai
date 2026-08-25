import { readdirSync, statSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

/** The reels waiting for his approval, read from the filesystem at request time.
 *
 *  This exists because the delivery channel was chat, and chat is not a place a file lives:
 *  every container reset lost the render and the build had to be rerun from scratch. A reel
 *  he has to watch and approve belongs in the studio next to the episode it is for, with the
 *  gate's verdict and the caption beside it, so approving is one screen instead of three.
 *
 *  Read from disk rather than the database on purpose: the file being present IS the fact,
 *  and a row claiming a video exists when it does not is exactly the kind of lie the studio
 *  is built to avoid. */

export type Reel = {
  /** the URL the player uses */
  src: string;
  /** audio candidates play in an <audio> element; a video in a <video> one */
  kind: "video" | "audio";
  file: string;
  /** episode number parsed from the name, when the name carries one */
  episode: number | null;
  bytes: number;
  builtAt: string;
  /** the gate's own output, written beside the file by export/check.sh */
  gate: { passed: boolean; text: string } | null;
  /** the caption to post with it, if one is written for this episode */
  caption: string | null;
  /** title + description for YouTube Shorts, if one is written for this episode — a
   *  separate file because YouTube wants a title line first, which an Instagram
   *  caption doesn't have */
  youtube: string | null;
  /** the real, already-approved title, when one exists — see realTitleFor() below */
  title: string | null;
};

/** Episodes that are a direct "part 2" of an earlier one: recap the earlier episode's
 *  problem in the first few seconds, then give the fix it didn't have. Hardcoded because
 *  it is written once, by hand, when the part 2 is scripted — never inferred from a title. */
export const SEQUEL_OF: Record<number, number> = { 6: 3, 8: 4 };
export const SEQUEL_FOR: Record<number, number> = Object.fromEntries(
  Object.entries(SEQUEL_OF).map(([part2, original]) => [original, Number(part2)]),
);

const DIR = join(process.cwd(), "public", "reels");
const CAPTIONS = join(process.cwd(), "..", "channel");

function textFor(n: number | null, suffix: string): string | null {
  if (n === null) return null;
  const p = join(CAPTIONS, `episode-${String(n).padStart(2, "0")}-${suffix}.txt`);
  try {
    return existsSync(p) ? readFileSync(p, "utf8").trim() : null;
  } catch {
    return null;
  }
}

export const captionFor = (n: number | null) => textFor(n, "caption");
const youtubeFor = (n: number | null) => textFor(n, "youtube");

/** The real, already-approved title — its first line is written once, when the episode's
 *  YouTube copy is finalized, and never needs retyping anywhere else. He kept having to
 *  copy it into the studio's title field by hand and it kept not happening (both public
 *  episode pages showed the studio's "פרק חדש" placeholder for weeks after the real title
 *  existed on disk). Read directly from the file that already has it, instead. */
export function realTitleFor(n: number | null): string | null {
  const yt = youtubeFor(n);
  return yt ? yt.split("\n")[0].trim() || null : null;
}

/** The last-resort title, for an episode whose youtube.txt was never written (several
 *  were — the caption alone shipped) and has no hand-written article either. A caption's
 *  first line is always its hook, written to work as a headline on its own, so it reads
 *  fine as a page title. Without this, /e/N 404s for a real, already-published, already-
 *  advertised episode the instant it's missing one companion file — and the caption
 *  itself prints this exact URL, so a real visitor hits that 404. */
export function captionTitleFor(n: number | null): string | null {
  const cap = captionFor(n);
  if (!cap) return null;
  return cap.split("\n").find((l) => l.trim())?.trim() || null;
}

/** The filesystem mtime does not survive a git checkout reliably — Vercel's own build
 *  showed every reel dated 2018-10-20, which is not a date that has ever been true for
 *  this repo. produce.sh now writes the real ship moment to a sidecar file; this reads
 *  that when present and only falls back to mtime for anything shipped before it existed. */
function builtAtFor(file: string, fallback: Date): string {
  const p = join(DIR, file.replace(/\.(mp4|m4a|wav)$/, ".built-at.txt"));
  try {
    if (existsSync(p)) {
      const v = readFileSync(p, "utf8").trim();
      if (v) return v;
    }
  } catch {
    /* fall through to the filesystem's own timestamp */
  }
  return fallback.toISOString();
}

function gateFor(file: string): Reel["gate"] {
  const p = join(DIR, file.replace(/\.mp4$/, ".gate.txt"));
  try {
    if (!existsSync(p)) return null;
    const text = readFileSync(p, "utf8").trim();
    return { passed: /ALL CHECKS PASSED/.test(text), text };
  } catch {
    return null;
  }
}

export function reelByFile(file: string): Reel | null {
  return reels().find((r) => r.file === file) ?? null;
}

export function reels(): Reel[] {
  // Audio as well as video, because the loop that matters most is the shortest one: he says a
  // line's tone is wrong, and the only way to settle it is for him to hear the candidates.
  // Rebuilding a whole narration and re-rendering to ask one question costs forty minutes;
  // playing six takes costs thirty seconds.
  let names: string[];
  try {
    names = readdirSync(DIR).filter((f) => /\.(mp4|m4a|wav)$/.test(f));
  } catch {
    return [];
  }
  return names
    .map((file) => {
      const st = statSync(join(DIR, file));
      const m = file.match(/(\d+)/);
      const episode = m ? Number(m[1]) : null;
      return {
        src: `/reels/${file}`,
        kind: /\.mp4$/.test(file) ? ("video" as const) : ("audio" as const),
        file,
        episode,
        bytes: st.size,
        builtAt: builtAtFor(file, st.mtime),
        gate: gateFor(file),
        caption: captionFor(episode),
        youtube: youtubeFor(episode),
        title: realTitleFor(episode),
      };
    })
    .sort((a, b) => b.builtAt.localeCompare(a.builtAt));
}
