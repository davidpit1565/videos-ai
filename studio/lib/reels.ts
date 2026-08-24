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
};

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

const captionFor = (n: number | null) => textFor(n, "caption");
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
      };
    })
    .sort((a, b) => b.builtAt.localeCompare(a.builtAt));
}
