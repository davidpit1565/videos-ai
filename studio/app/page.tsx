import Link from "next/link";
import { catalogue } from "@/lib/site";
import { PROMPTS } from "@/lib/prompts";
import { ARTICLES } from "@/lib/articles";
import { frameFor } from "@/lib/frames";
import { publicDay, publicMonth } from "@/lib/fmt";
import SiteNav from "./sitenav";
import EpRows from "./ep-rows";
import { IG_HANDLE, IG_URL } from "./site-social";

export const metadata = {
  title: { absolute: "Actually Works: AI setups that actually work" },
  description:
    "Short reels about AI tools, and a page for every episode with the steps and the prompt.",
};
export const revalidate = 300;

/** The front door for a visitor who tapped the link in a reel's bio.
 *
 *  Rebrand 13.11.2026 (logo A, light page) stripped the template look; rebrand 2 (same
 *  day, David: "the site looked better before, it is more bare now") brings back what was
 *  good and true, in the new identity:
 *  - the reels themselves, as real stills from the rendered files (lib/frames.ts), at the
 *    top of the first screen, instead of a third-party embed that loads late;
 *  - the real counts, as one plain sentence (no count-up, no big-number tiles);
 *  - the episode list with a picture per row;
 *  - "what breaks", the channel's own section, with real limits from the articles;
 *  - who makes it, short, with the link to the About page and the Flow app.
 *  Every number here is computed from the same data the pages show. Nothing is typed in. */
export default async function Home() {
  const eps = await catalogue();
  const live = eps.filter((e) => e.live);
  const strip = live.filter((e) => frameFor(e.n)).slice(0, 6);
  const stripNs = new Set(strip.map((e) => e.n));
  const earlier = live.filter((e) => !stripNs.has(e.n)).slice(0, 6);
  const newestDay = publicDay(live[0]?.publishedAt ?? null);

  // "What breaks": the newest live episodes that have a written limits section, one limit
  // each (the first one the article lists), so the section is real text from real pages,
  // not a summary written for the home page.
  const articleByN = new Map(ARTICLES.map((a) => [a.n, a]));
  const withLimits = live.filter((e) => (articleByN.get(e.n)?.limits.length ?? 0) > 0);
  const breaks = withLimits.slice(0, 3).map((e) => ({ e, limit: articleByN.get(e.n)!.limits[0] }));
  const limitsTotal = withLimits.reduce((a, e) => a + (articleByN.get(e.n)?.limits.length ?? 0), 0);

  return (
    <main className="site home" dir="ltr">
      <SiteNav />

      <section className="hero" aria-labelledby="hero-h">
        <h1 id="hero-h" className="display">AI setups that actually work.</h1>
        <p className="lede">
          Short reels where an AI tool gets tried on a real screen. Every episode has a page
          here with the exact steps, the prompt, and what it will not do.
        </p>
        <div className="hero-act">
          <a className="button solid" href={IG_URL} target="_blank" rel="noopener noreferrer">
            Follow {IG_HANDLE}
          </a>
          {live.length > 0 ? (
            <p className="hero-fact">
              {live.length} episode{live.length === 1 ? "" : "s"} so far.
              {newestDay ? ` The newest went out on ${newestDay}.` : ""}
            </p>
          ) : null}
        </div>
      </section>

      {strip.length > 0 ? (
        <section className="reels" aria-labelledby="reels-h">
          <div className="block-head">
            <h2 id="reels-h">Newest reels</h2>
            <Link href="/episodes">All episodes</Link>
          </div>
          <ol className="strip">
            {strip.map((e, i) => (
              <li key={e.n} style={{ "--i": i } as React.CSSProperties}>
                <Link href={`/e/${e.n}`}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={frameFor(e.n)!}
                    alt={`A frame from episode ${e.n}`}
                    width={360}
                    height={640}
                    loading={i < 3 ? "eager" : "lazy"}
                    decoding="async"
                  />
                  <span className="strip-no">Episode {e.n}</span>
                  <span className="strip-t">{e.title}</span>
                </Link>
              </li>
            ))}
          </ol>
          <p className="fine strip-note">Each picture is a frame from the reel. Tap one for its steps.</p>
        </section>
      ) : null}

      <div className="home-cols">
        <div className="home-main">
          {earlier.length > 0 ? (
            <section className="block" aria-labelledby="earlier-h">
              <div className="block-head">
                <h2 id="earlier-h">Earlier episodes</h2>
                <Link href="/episodes">All {live.length}</Link>
              </div>
              <EpRows
                items={earlier.map((e) => ({
                  n: e.n,
                  title: e.title,
                  blurb: e.blurb,
                  meta: [`Episode ${e.n}`, publicMonth(e.publishedAt)].filter(Boolean).join(", "),
                }))}
              />
            </section>
          ) : eps.length === 0 ? (
            <p className="empty">No episode is published yet.</p>
          ) : null}

          {breaks.length > 0 ? (
            <section className="block" aria-labelledby="breaks-h">
              <div className="block-head">
                <h2 id="breaks-h">What breaks</h2>
                <Link href="/failure-modes">All of them</Link>
              </div>
              <p className="sub">
                Every episode page ends with what the setup will not do: {limitsTotal} limits
                written down so far, across {withLimits.length} episode
                {withLimits.length === 1 ? "" : "s"}. The newest three:
              </p>
              <ul className="breaks">
                {breaks.map(({ e, limit }) => (
                  <li key={e.n}>
                    <p className="breaks-limit">{limit}</p>
                    <Link className="breaks-src" href={`/e/${e.n}`}>
                      Episode {e.n}: {e.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </section>
          ) : null}
        </div>

        <aside className="home-side">
          <section className="block" aria-labelledby="prompts-h">
            <div className="block-head">
              <h2 id="prompts-h">The prompts, in full</h2>
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

          <section className="block whois" aria-labelledby="whois-h">
            <div className="block-head">
              <h2 id="whois-h">Who makes this</h2>
            </div>
            <p>
              David, in Belgium, in the hours around a day job. Nothing goes out that has not
              been run first, and every reel passes a set of checks before it is posted.
            </p>
            <p className="whois-links">
              <Link href="/about">How it is made</Link>
              <a href="https://apps.apple.com/us/app/id6807543350" target="_blank" rel="noopener noreferrer">
                Flow, the finance app built here, on the App Store
              </a>
            </p>
          </section>
        </aside>
      </div>
    </main>
  );
}
