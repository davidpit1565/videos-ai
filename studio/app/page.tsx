import Link from "next/link";
import { catalogue } from "@/lib/site";
import { PROMPTS } from "@/lib/prompts";
import SiteNav from "./sitenav";
import IgEmbed from "./ig-embed";
import ExternalIcon from "./external-icon";
import { IG_HANDLE, IG_URL } from "./site-social";

export const metadata = {
  title: { absolute: "Actually Works: AI setups that actually work" },
  description:
    "Short reels about AI tools, and a page for every episode with the steps and the prompt.",
};
export const revalidate = 300;

/** The front door for a visitor who tapped the link in a reel's bio.
 *
 *  Rebrand 13.11.2026 (logo A, light page, site audit of the same day): on a phone the
 *  first screen is now the name, one sentence, the follow action with the handle written
 *  out, and the newest reel. Removed: the "AI CREATOR" eyebrow, the word-by-word and
 *  rotating headline, the count-up numbers, the tool ticker and track pills, the glow
 *  behind the hero, the cursor spotlight and magnetic button, the drawn "SETUP.LOG" chart,
 *  and the safe-zone demo (it spoke to video makers, not to people curious about AI). */
export default async function Home() {
  const eps = await catalogue();
  const live = eps.filter((e) => e.live);
  // The newest live episode that has a real post to show. The hero never plays the
  // self-hosted mp4: it is pruned from the deployment once an episode is live (1.11.2026).
  const newest = live.find((e) => e.ytVideoId || e.igPermalink) ?? null;
  const recent = live.filter((e) => e.n !== newest?.n).slice(0, 5);

  return (
    <main className="site home" dir="ltr">
      <SiteNav />
      <div className="hero">
        <div className="hero-text">
          <h1 className="display">AI setups that actually work.</h1>
          <p className="lede">
            Short reels about AI tools. Every episode has its own page here
            with the steps, and the prompt when there is one.
          </p>
          <p className="hero-follow">
            <a className="button solid" href={IG_URL} target="_blank" rel="noopener noreferrer">
              Follow {IG_HANDLE}
            </a>
          </p>
        </div>

        {newest ? (
          <section className="hero-reel" aria-labelledby="newest">
            <h2 id="newest" className="newest-title">
              <span className="newest-no">Episode {newest.n}</span>{" "}
              <Link href={`/e/${newest.n}`}>{newest.title}</Link>
            </h2>
            {newest.igPermalink ? (
              <div className="vid-ig">
                <IgEmbed permalink={newest.igPermalink} />
              </div>
            ) : newest.ytVideoId ? (
              <div className="vid-yt">
                <iframe
                  src={`https://www.youtube-nocookie.com/embed/${newest.ytVideoId}`}
                  title={newest.title}
                  allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"
                  allowFullScreen
                />
              </div>
            ) : null}
            <p className="newest-links">
              <Link href={`/e/${newest.n}`}>The steps for this episode</Link>
              {newest.igPermalink && newest.ytVideoId ? (
                <a href={`https://youtu.be/${newest.ytVideoId}`} target="_blank" rel="noreferrer">
                  Watch on YouTube <ExternalIcon />
                </a>
              ) : null}
            </p>
          </section>
        ) : null}
      </div>

      <section className="block">
        <div className="block-head">
          <h2>Recent episodes</h2>
          <Link href="/episodes">{live.length > 0 ? `All ${live.length} episodes` : "All episodes"}</Link>
        </div>
        {eps.length === 0 ? (
          <p className="empty">No episode is published yet.</p>
        ) : (
          <ol className="rows">
            {(recent.length ? recent : eps.slice(0, 5)).map((e) => (
              <li key={e.n}>
                <Link href={`/e/${e.n}`}>
                  <span className="row-no">{e.n}</span>
                  <span className="row-t">{e.title}</span>
                  {e.blurb ? <span className="row-b">{e.blurb}</span> : null}
                </Link>
              </li>
            ))}
          </ol>
        )}
      </section>

      <section className="block">
        <div className="block-head">
          <h2>The prompts, in full</h2>
        </div>
        <p className="sub">Each one complete, with what it cannot do.</p>
        <ol className="rows">
          {PROMPTS.map((p) => (
            <li key={p.slug}>
              <Link href={`/p/${p.slug}`}>
                <span className="row-t">{p.title}</span>
                <span className="row-b">{p.blurb}</span>
              </Link>
            </li>
          ))}
        </ol>
      </section>
    </main>
  );
}
