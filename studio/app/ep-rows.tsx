import Link from "next/link";
import { frameFor } from "@/lib/frames";

export type EpRowItem = {
  n: number;
  title: string;
  blurb?: string | null;
  /** a short line above the title: "Episode 93, Nov 2026, ChatGPT" */
  meta?: string | null;
};

/** One scannable list of episodes, used on the home page, /episodes, an episode page's
 *  "More episodes" and the 404: a real still from the reel, the number, the title, one
 *  line of what you get, and the whole row is the link to the episode's setup page.
 *  Plain rows with a rule between them, not cards (site audit 13.11.2026). */
export default function EpRows({ items, compact = false }: { items: EpRowItem[]; compact?: boolean }) {
  return (
    <ol className={`eprows${compact ? " compact" : ""}`}>
      {items.map((e) => {
        const src = frameFor(e.n);
        return (
          <li key={e.n}>
            <Link href={`/e/${e.n}`}>
              {src ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img className="eprow-img" src={src} alt="" width={360} height={640} loading="lazy" decoding="async" />
              ) : (
                <span className="eprow-img eprow-none" aria-hidden="true" />
              )}
              <span className="eprow-text">
                <span className="eprow-meta">{e.meta ?? `Episode ${e.n}`}</span>
                <span className="eprow-t">{e.title}</span>
                {e.blurb && !compact ? <span className="eprow-b">{e.blurb}</span> : null}
              </span>
            </Link>
          </li>
        );
      })}
    </ol>
  );
}
