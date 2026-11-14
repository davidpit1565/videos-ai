import Link from "next/link";
import SiteNav from "./sitenav";
import EpRows from "./ep-rows";
import { catalogue } from "@/lib/site";

export const metadata = { title: "Page not found" };

/** Every address no route answers, and every address middleware.ts does not recognise
 *  (a typo, an old link to the removed /prompts or /skills pages). Before 13.11.2026 such
 *  a visitor was redirected to the studio's Hebrew PIN screen; this is English, says what
 *  happened, and offers the two places a reel visitor most likely wanted. */
export default async function NotFound() {
  // The three newest episodes, so a lost visitor still sees the reels. If the database is
  // unreachable the page still renders, just without the list.
  let newest: { n: number; title: string }[] = [];
  try {
    newest = (await catalogue()).slice(0, 3).map((e) => ({ n: e.n, title: e.title }));
  } catch {
    newest = [];
  }
  return (
    <main className="site" dir="ltr">
      <SiteNav />
      <h1>This page does not exist.</h1>
      <p className="lede">
        The link may be old, or a letter got lost. The newest episode is one tap away.
      </p>
      <p className="actions-row">
        <Link className="button solid" href="/latest">
          Newest episode
        </Link>
        <Link className="button" href="/episodes">
          All episodes
        </Link>
      </p>
      {newest.length ? (
        <section className="block">
          <div className="block-head">
            <h2>Newest episodes</h2>
          </div>
          <EpRows items={newest} compact />
        </section>
      ) : null}
    </main>
  );
}
