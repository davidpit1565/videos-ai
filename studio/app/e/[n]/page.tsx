import Link from "next/link";
import SiteNav from "../../sitenav";
import { notFound } from "next/navigation";
import { episode, published } from "@/lib/site";
import { articleFor, promptFor, ARTICLES } from "@/lib/articles";
import { SEQUEL_OF, SEQUEL_FOR, captionFor, captionTitleFor, reels } from "@/lib/reels";
import Signup from "../../signup";
import SiteNotify from "../../site-notify";
import IgEmbed from "../../ig-embed";
import { SITE_URL } from "@/lib/site";

export const revalidate = 300;

export async function generateMetadata({ params }: { params: Promise<{ n: string }> }) {
  const n = Number((await params).n);
  const a = articleFor(n);
  const e = await episode(n);
  const title = e?.title || a?.title || captionTitleFor(n) || undefined;
  if (!title) {
    // absolute: the front door is the brand itself, not "Actually Works · Actually Works"
    return { title: { absolute: "Actually Works" } };
  }
  const description = a?.standfirst ?? e?.topic ?? undefined;
  // The image itself comes from the sibling opengraph-image.tsx (Next resolves it per
  // route automatically); this only needs to override the title/description a shared
  // link shows, per episode instead of the site-wide default in layout.tsx.
  return {
    title,
    description,
    openGraph: { title, description, type: "article" as const },
    twitter: { title, description },
  };
}

export default async function EpisodePage({ params }: { params: Promise<{ n: string }> }) {
  const n = Number((await params).n);
  if (!Number.isFinite(n)) notFound();

  // The page exists if the studio has published the episode, the article is written, OR
  // the caption exists on disk — that third case is not theoretical: episodes 6, 8, 10,
  // 11 and 12 all shipped with a caption but no youtube.txt and no DB record yet, and the
  // caption itself prints this exact URL the moment the reel goes out. Requiring a DB
  // record or an article meant a real visitor, clicking a real published caption's own
  // link, got a 404.
  const e = await episode(n);
  const a = articleFor(n);
  const capTitle = captionTitleFor(n);
  if (!e && !a && !capTitle) notFound();

  const prompt = promptFor(a);
  const title = e?.title || a?.title || capTitle || `Episode ${n}`;
  // The reel file itself, when it exists and passed its gate — the last-resort video for
  // an episode with no Instagram/YouTube link recorded yet (same gap as the title above).
  const selfHosted = reels().find((r) => r.kind === "video" && r.episode === n && r.gate?.passed);
  // Same last-resort source as the title/video above, for the body: the caption's own
  // paragraphs, minus the first (already the h1) and the Instagram-specific tail — the
  // link back to this exact page, the follow CTA, the hashtag line. Only used when no
  // hand-written article exists; the article is always the better version of this.
  const capBody = !a
    ? (captionFor(n) ?? "")
        .split(/\n{2,}/)
        .slice(1)
        .filter((p) => !/^Full breakdown:|^Follow for|^#/.test(p.trim()))
    : [];
  const allPub = await published();
  const others = allPub.filter((x) => x.number !== n);
  const more = others.length
    ? others.slice(0, 3).map((x) => ({ n: x.number, t: x.title }))
    : ARTICLES.filter((x) => x.n !== n).slice(0, 3).map((x) => ({ n: x.n, t: x.title }));

  // Part 2 recaps this episode's problem, then gives the fix it didn't have — only
  // link to it once it is actually live, never to a page that doesn't exist yet.
  const part2 = SEQUEL_FOR[n] !== undefined ? allPub.find((x) => x.number === SEQUEL_FOR[n]) : null;
  const part1 = SEQUEL_OF[n] !== undefined ? allPub.find((x) => x.number === SEQUEL_OF[n]) : null;

  // contentUrl beats embedUrl when there's an actual, directly-playable file — schema.org's
  // own preferred field for exactly this case — so the self-hosted mp4 gets that instead
  // of being squeezed into "embed" semantics. Otherwise, the two platforms that have a
  // genuinely embeddable URL: the YouTube nocookie embed (Google's own documented
  // VideoObject example) or Instagram's own permalink+"embed" (the exact URL its embed.js
  // renders into an iframe, per Meta's oEmbed docs). Without any of these, Google's
  // rich-result validator flags the markup as incomplete, so an episode with none just
  // gets no VideoObject at all rather than one that fails validation.
  const contentUrl = selfHosted ? `${SITE_URL}${selfHosted.src}` : null;
  const embedUrl = contentUrl
    ? null
    : e?.ytVideoId
      ? `https://www.youtube-nocookie.com/embed/${e.ytVideoId}`
      : e?.igPermalink
        ? `${e.igPermalink.replace(/\/?$/, "/")}embed`
        : null;
  const videoSchema = contentUrl || embedUrl
    ? {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        name: title,
        description: a?.standfirst ?? e?.topic ?? title,
        thumbnailUrl: `${SITE_URL}/e/${n}/opengraph-image`,
        uploadDate: e?.publishedAt ? new Date(e.publishedAt).toISOString() : undefined,
        contentUrl: contentUrl ?? undefined,
        embedUrl: embedUrl ?? undefined,
      }
    : null;

  return (
    <main className="site" dir="ltr">
      {videoSchema && (
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(videoSchema) }} />
      )}
      <SiteNav />
      <p className="kicker">
        <Link href="/">Actually Works</Link> · Episode {String(n).padStart(2, "0")}
      </p>
      <h1>{title}</h1>
      {a ? <p className="sub">{a.standfirst}</p> : e?.topic ? <p className="sub">{e.topic}</p> : null}
      {part1 ? (
        <p className="sub">
          Part 2 of <Link href={`/e/${part1.number}`}>{part1.title}</Link> — the fix for what
          that episode named but didn't solve.
        </p>
      ) : null}
      {part2 ? (
        <p className="sub">
          There's a part 2: <Link href={`/e/${part2.number}`}>{part2.title}</Link> — the fix
          for exactly this.
        </p>
      ) : null}

      {/* The self-hosted file first when it exists — instant, on-brand, no third-party
          script to wait on or get blocked. The Instagram embed depends on embed.js
          loading over the network and shows its own generic blue branding until it does;
          on a page whose one job is showing the clip, that's a real, visible cost, not a
          style preference. Instagram/YouTube become secondary links below instead, which
          is where their real numbers (views, likes) still get their due. */}
      {selfHosted ? (
        <div className="vid-native">
          <video src={selfHosted.src} controls playsInline preload="metadata" />
        </div>
      ) : e?.igPermalink ? (
        <div className="vid-ig">
          <IgEmbed permalink={e.igPermalink} />
        </div>
      ) : e?.ytVideoId ? (
        <div className="vid">
          <iframe
            src={`https://www.youtube-nocookie.com/embed/${e.ytVideoId}`}
            title={title}
            allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"
            allowFullScreen
          />
        </div>
      ) : null}

      {/* Real platforms and real numbers, once the self-hosted file already carried the
          primary watch experience above. */}
      {selfHosted && (e?.igPermalink || e?.ytVideoId) ? (
        <p className="sub">
          {e?.igPermalink && (
            <a href={e.igPermalink} target="_blank" rel="noreferrer">
              View on Instagram{e.views ? ` — ${e.views.toLocaleString("en-US")} views` : ""} ↗
            </a>
          )}
          {e?.igPermalink && e?.ytVideoId ? " · " : ""}
          {e?.ytVideoId && (
            <a href={`https://youtu.be/${e.ytVideoId}`} target="_blank" rel="noreferrer">
              Watch on YouTube ↗
            </a>
          )}
        </p>
      ) : !selfHosted && e?.igPermalink && e?.ytVideoId ? (
        <p className="sub">
          <a href={`https://youtu.be/${e.ytVideoId}`} target="_blank" rel="noreferrer">
            Watch on YouTube instead ↗
          </a>
        </p>
      ) : null}

      {a ? (
        <>
          <section>
            <h2>The exact clicks</h2>
            <ol className="steps">
              {a.steps.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ol>
          </section>

          {prompt ? (
            <section>
              <h2>The prompt</h2>
              <pre className="body">{prompt.body}</pre>
              <p className="sub">
                Copy all of it. <Link href={`/p/${prompt.slug}`}>Its own page</Link> has it
                too, if this one is awkward to select on a phone.
              </p>
            </section>
          ) : null}

          <section>
            <h2>What changes</h2>
            <ul className="changes">
              {a.changes.map((c, i) => (
                <li key={i}>{c}</li>
              ))}
            </ul>
          </section>

          <section>
            <h2>What it will not do</h2>
            <ul className="limits-list">
              {a.limits.map((l, i) => (
                <li key={i}>{l}</li>
              ))}
            </ul>
          </section>
        </>
      ) : capBody.length ? (
        <section>
          {capBody.map((p, i) => (
            <p key={i}>{p}</p>
          ))}
        </section>
      ) : null}

      {e?.notes ? (
        <section>
          <h2>Notes</h2>
          {e.notes.split(/\n{2,}/).map((p, i) => (
            <p key={i}>{p}</p>
          ))}
        </section>
      ) : null}

      <section>
        <h2>Get the next one</h2>
        <p className="sub">One AI setup a week, straight to your inbox.</p>
        <Signup source="episode" />
        <SiteNotify />
      </section>

      <footer className="sfoot">
        {more.map((x) => (
          <Link key={x.n} href={`/e/${x.n}`}>
            {String(x.n).padStart(2, "0")} · {x.t}
          </Link>
        ))}
        <Link href="/join">Email list</Link>
      </footer>
    </main>
  );
}
