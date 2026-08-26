import Link from "next/link";
import { catalogue } from "@/lib/site";
import { fetchLatestBeehiivIssue } from "@/lib/sources";
import { PROMPTS } from "@/lib/prompts";
import { ARTICLES } from "@/lib/articles";
import { reels } from "@/lib/reels";
import Signup from "./signup";
import SiteNotify from "./site-notify";
import SiteNav from "./sitenav";
import CountUp from "./count-up";
import IgEmbed from "./ig-embed";
import Reveal from "./reveal";
import { TOOLS, toolFor } from "@/lib/tools";

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
  // Not a vanity number — every other AI-content page leads with subscribers or views.
  // This one counts the thing this channel actually promises: a written, numbered "what
  // it will not do" per setup. Real count off the hand-written articles, never estimated.
  const breaksDocumented = ARTICLES.reduce((a, ar) => a + ar.limits.length, 0);
  // The newest live episode with a video, for the hero — the channel's whole premise is
  // "the exact screen", and a home page that never shows one before the fold undercuts it.
  // Used to only look at ytVideoId, so the hero showed a YouTube embed even on episodes
  // that do have an Instagram post — the opposite of the episode page's own priority
  // (self-hosted file, then Instagram, then YouTube last, see /e/[n]/page.tsx) and
  // exactly the mismatch he flagged directly. Same priority here now.
  const heroEpisode = live.find((e) => e.ytVideoId || e.igPermalink) ?? null;
  const heroSelfHosted = heroEpisode
    ? reels().find((r) => r.kind === "video" && r.episode === heroEpisode.n && r.gate?.passed)
    : undefined;
  // A short teaser, not the full browser: the home page is a landing page, not the
  // episode index. He said directly that home reading as the same page as the episode
  // list — no visual break between them — made it feel like there was no home page at all.
  const recent = live.slice(0, 3);
  const latestIssue = await fetchLatestBeehiivIssue();
  // Named tracks instead of one flat feed — the structural idea a competitor audit
  // flagged directly (Every.to organizes its whole homepage around named verticals
  // rather than an undifferentiated blog list). The tags are real ones already
  // computed for the episode browser (lib/tools.ts), never a separate taxonomy
  // invented just for this row — so a click here and a click on /episodes always
  // agree on what belongs where.
  const trackCounts = new Map<string, number>();
  for (const e of eps) trackCounts.set(toolFor(e.title), (trackCounts.get(toolFor(e.title)) ?? 0) + 1);
  const tracks = TOOLS.filter((t) => trackCounts.has(t)).map((t) => ({ t, n: trackCounts.get(t)! }));

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
          {(live.length > 0 || totalViews > 0 || breaksDocumented > 0) && (
            <div className="herostats">
              {live.length > 0 && (
                <div>
                  <b><CountUp value={live.length} /></b>
                  <span>episode{live.length === 1 ? "" : "s"} live</span>
                </div>
              )}
              {breaksDocumented > 0 && (
                <div>
                  <b><CountUp value={breaksDocumented} /></b>
                  <span>failure modes written down</span>
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
        {heroSelfHosted ? (
          <div className="herovid vid-native">
            <video src={heroSelfHosted.src} controls playsInline preload="metadata" />
            {heroEpisode?.ytVideoId ? (
              <p className="sub herovidlink">
                <a href={`https://youtu.be/${heroEpisode.ytVideoId}`} target="_blank" rel="noreferrer">
                  Also on YouTube ↗
                </a>
              </p>
            ) : null}
          </div>
        ) : heroEpisode?.igPermalink ? (
          <div className="herovid vid-ig">
            <IgEmbed permalink={heroEpisode.igPermalink} />
            {heroEpisode.ytVideoId ? (
              <p className="sub herovidlink">
                <a href={`https://youtu.be/${heroEpisode.ytVideoId}`} target="_blank" rel="noreferrer">
                  Also on YouTube ↗
                </a>
              </p>
            ) : null}
          </div>
        ) : heroEpisode?.ytVideoId ? (
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

      {tracks.length > 1 && (
        <section>
          <Reveal>
            <h2>Browse by tool</h2>
            <ul className="tracks">
              {tracks.map(({ t, n }) => (
                <li key={t}>
                  <Link href={`/episodes?tool=${encodeURIComponent(t)}`}>
                    <span className="tname">{t}</span>
                    <span className="tcount">{n}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </Reveal>
        </section>
      )}

      <section>
        <Reveal>
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
        </Reveal>
      </section>

      <section>
        <Reveal>
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
        </Reveal>
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
