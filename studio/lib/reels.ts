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
  file: string;
  /** episode number parsed from the name, when the name carries one */
  episode: number | null;
  bytes: number;
  builtAt: string;
  /** the gate's own output, written beside the file by export/check.sh */
  gate: { passed: boolean; text: string } | null;
  /** the caption to post with it, if one is written for this episode */
  caption: string | null;
};

const DIR = join(process.cwd(), "public", "reels");
const CAPTIONS = join(process.cwd(), "..", "channel");

function captionFor(n: number | null): string | null {
  if (n === null) return null;
  const p = join(CAPTIONS, `episode-${String(n).padStart(2, "0")}-caption.txt`);
  try {
    return existsSync(p) ? readFileSync(p, "utf8").trim() : null;
  } catch {
    return null;
  }
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

export function reels(): Reel[] {
  let names: string[];
  try {
    names = readdirSync(DIR).filter((f) => f.endsWith(".mp4"));
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
        file,
        episode,
        bytes: st.size,
        builtAt: st.mtime.toISOString(),
        gate: gateFor(file),
        caption: captionFor(episode),
      };
    })
    .sort((a, b) => b.builtAt.localeCompare(a.builtAt));
}
