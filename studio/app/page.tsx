import Link from "next/link";
import { catalogue } from "@/lib/site";
import { PROMPTS } from "@/lib/prompts";
import Signup from "./signup";
import SiteNav from "./sitenav";
import EpisodesBrowser from "./episodes-browser";

export const metadata = {
  title: { absolute: "Actually Works — AI setups that actually work" },
  description:
    "One AI setup per episode: the exact screen, the exact paste, and what breaks. No hype.",
};
export const revalidate = 300;

export default async function Home() {
  const eps = await catalogue();
  const live = eps.filter((e) => e.live);
  const totalViews = live.reduce((a, e) => a + (e.views ?? 0), 0);

  return (
    <main className="site" dir="ltr">
      <SiteNav here="/" />
      <header className="hero">
        <h1>
          AI setups that <em>actually work</em>.
        </h1>
        <p className="sub">
          One setup per episode. The exact screen, the exact paste, and the part that
          breaks — because the part that breaks is the part everyone else skips.
        </p>
        {/* Real, already-measured numbers only — no series here is invented, and a
            metric with nothing behind it yet (0 views measured so far) doesn't print. */}
        {(live.length > 0 || totalViews > 0) && (
          <p className="herostat">
            {live.length} episode{live.length === 1 ? "" : "s"} live
            {totalViews > 0 ? ` · ${totalViews.toLocaleString("en-US")} real views measured` : ""}
          </p>
        )}
        <Signup source="home" />
      </header>

      <section>
        <h2>Episodes</h2>
        {eps.length === 0 ? (
          <p className="empty">
            The first episode is finished and not published yet. It lands here the day
            it goes out.
          </p>
        ) : (
          <EpisodesBrowser eps={eps} />
        )}
      </section>

      <section>
        <h2>The prompts, in full</h2>
        <p className="sub">
          Every prompt an episode uses is here, complete, with what it cannot do. No
          email needed to read them.
        </p>
        <ul className="prompts">
          {PROMPTS.map((p) => (
            <li key={p.slug}>
              <Link href={`/p/${p.slug}`}>
                <b>{p.title}</b>
                <span>{p.blurb}</span>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <footer className="sfoot">
        <Link href="/prompts">All prompts</Link>
        <Link href="/search">Search</Link>
        <Link href="/about">About</Link>
        <Link href="/join">Email list</Link>
      </footer>
    </main>
  );
}
