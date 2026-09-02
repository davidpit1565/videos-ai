import Link from "next/link";
import SiteNav from "../sitenav";
import Reveal from "../reveal";
import { catalogue } from "@/lib/site";
import { ARTICLES } from "@/lib/articles";

export const metadata = {
  title: "Failure modes",
  description: "Every documented limit, per episode — what it will not do, and where it's from.",
};

export const revalidate = 300;

/** Every episode's "what it will not do" section, collected in one place. Nothing here
 *  is a separate list to keep in sync by hand — it reads straight off the same
 *  catalogue() + ARTICLES that already drive the episode pages and the homepage's own
 *  "failure modes written down" count, so a new episode's limits show up here the same
 *  build they ship, with no second place to remember to update. */
export default async function FailureModes() {
  const eps = await catalogue();
  const byNumber = new Map(ARTICLES.map((a) => [a.n, a]));
  const rows = eps
    .map((e) => ({ e, limits: byNumber.get(e.n)?.limits ?? [] }))
    .filter((r) => r.limits.length > 0);
  const total = rows.reduce((a, r) => a + r.limits.length, 0);

  return (
    <main className="site" dir="ltr">
      <SiteNav here="/failure-modes" />
      <p className="kicker">
        <Link href="/">Actually Works</Link> · Failure modes
      </p>
      <h1>What breaks, written down.</h1>
      <p className="sub">
        Every episode ships with its own limits section — the part most tutorials leave
        out. This is all of them in one place: {total} documented so far, across{" "}
        {rows.length} episode{rows.length === 1 ? "" : "s"}.
      </p>

      {rows.length === 0 ? (
        <p className="empty">Nothing documented yet.</p>
      ) : (
        rows.map(({ e, limits }) => (
          <Reveal key={e.n}>
            <section>
              <h2>
                <Link href={`/e/${e.n}`}>
                  Episode {e.n} — {e.title}
                </Link>
              </h2>
              <ul className="limits-list">
                {limits.map((l, i) => (
                  <li key={i}>{l}</li>
                ))}
              </ul>
            </section>
          </Reveal>
        ))
      )}

      <footer className="sfoot">
        <Link href="/episodes">Episodes</Link>
        <Link href="/about">About</Link>
      </footer>
    </main>
  );
}
