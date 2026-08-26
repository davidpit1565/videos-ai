import Link from "next/link";
import { catalogue } from "@/lib/site";
import { fetchLatestBeehiivIssue } from "@/lib/sources";
import { PROMPTS } from "@/lib/prompts";
import Signup from "./signup";
import SiteNotify from "./site-notify";
import SiteNav from "./sitenav";
import CountUp from "./count-up";

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
  // The newest live episode with a video, for the hero — the channel's whole premise is
  // "the exact screen", and a home page that never shows one before the fold undercuts it.
  const heroEpisode = live.find((e) => e.ytVideoId) ?? null;
  // A short teaser, not the full browser: the home page is a landing page, not the
  // episode index. He said directly that home reading as the same page as the episode
  // list — no visual break between them — made it feel like there was no home page at all.
  const recent = live.slice(0, 3);
  const latestIssue = await fetchLatestBeehiivIssue();

  return (
    <main className="site" dir="ltr">
      <SiteNav here="/" />
      <header className="hero">
        <div className="herotext">
          <p className="kicker">AI CREATOR</p>
          <h1>
            AI setups that <em>actually work</em>.
          </h1>
          <p className="sub">
            One setup per episode. The exact screen, the exact paste, and the part that
            breaks — because the part that breaks is the part everyone else skips.
          </p>
          <div className="herocta">
            <Link className="cta" href="/episodes">
              Browse episodes →
            </Link>
            <Link href="/about">My story →</Link>
          </div>
          {/* Real, already-measured numbers only — a stat with nothing behind it yet
              doesn't get a tile, rather than a tile showing a fabricated 0. Placed before
              the signup form on purpose: proof before the ask. */}
          {(live.length > 0 || totalViews > 0) && (
            <div className="herostats">
              {live.length > 0 && (
                <div>
                  <b><CountUp value={live.length} /></b>
                  <span>episode{live.length === 1 ? "" : "s"} live</span>
                </div>
              )}
              {totalViews > 0 && (
                <div>
                  <b><CountUp value={totalViews} /></b>
                  <span>views measured</span>
                </div>
              )}
            </div>
          )}
          {/* Something concrete to judge before handing over an email — a signup form
              with nothing behind it is a harder ask than one with a real last issue. */}
          {latestIssue ? (
            <a className="issueteaser" href={latestIssue.url} target="_blank" rel="noopener">
              <span className="ilabel">Last issue</span>
              <span className="ititle">{latestIssue.title}</span>
            </a>
          ) : null}
          <Signup source="home" />
          <SiteNotify />
        </div>
        {heroEpisode?.ytVideoId ? (
          <div className="herovid vid">
            <iframe
              src={`https://www.youtube-nocookie.com/embed/${heroEpisode.ytVideoId}`}
              title={heroEpisode.title}
              allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"
              allowFullScreen
            />
          </div>
        ) : null}
      </header>

      <section>
        <div className="sechead">
          <h2>Recent episodes</h2>
          <Link href="/episodes">All episodes →</Link>
        </div>
        {eps.length === 0 ? (
          <p className="empty">
            The first episode is finished and not published yet. It lands here the day
            it goes out.
          </p>
        ) : (
          <ul className="eps">
            {(recent.length ? recent : eps.slice(0, 3)).map((e) => (
              <li key={e.n}>
                <Link href={`/e/${e.n}`}>
                  <span className="n">{String(e.n).padStart(2, "0")}</span>
                  <span className="t">{e.title}</span>
                  <span className="tp">{e.blurb}</span>
                </Link>
              </li>
            ))}
          </ul>
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
        <Link href="/episodes">Episodes</Link>
        <Link href="/prompts">All prompts</Link>
        <Link href="/search">Search</Link>
        <Link href="/about">About</Link>
        <Link href="/join">Email list</Link>
      </footer>
    </main>
  );
}
