import Link from "next/link";
import SiteNav from "./sitenav";

export const metadata = { title: "Page not found" };

/** Every address no route answers, and every address middleware.ts does not recognise
 *  (a typo, an old link to the removed /prompts or /skills pages). Before 13.11.2026 such
 *  a visitor was redirected to the studio's Hebrew PIN screen; this is English, says what
 *  happened, and offers the two places a reel visitor most likely wanted. */
export default function NotFound() {
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
    </main>
  );
}
