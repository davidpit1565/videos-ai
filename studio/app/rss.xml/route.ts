import { published, SITE_URL } from "@/lib/site";
import { realTitleFor, reels, captionTitleFor } from "@/lib/reels";

export const revalidate = 3600;

function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/** For anyone who would rather follow a feed reader than hand an inbox to Beehiiv — same
 *  episodes, same order, no extra signup.
 *
 *  Two sources, same as /e/[n]/page.tsx and sitemap.ts: the DB-tracked live episodes, plus
 *  any gated reel with a caption but no DB record yet (episodes 6, 8, 10-12 as of writing)
 *  — the feed would otherwise silently skip real, already-published episodes. */
export async function GET() {
  const eps = await published();
  const knownNumbers = new Set(eps.map((e) => e.number));
  const captionOnly = reels()
    .filter((r) => r.kind === "video" && r.gate?.passed && r.episode != null && !knownNumbers.has(r.episode))
    .map((r) => ({ number: r.episode as number, title: captionTitleFor(r.episode), topic: "", builtAt: r.builtAt }))
    .filter((r) => r.title);

  const items = [
    ...eps.map((e) => ({
      number: e.number,
      title: realTitleFor(e.number) || e.title,
      topic: e.topic,
      date: e.publishedAt ? new Date(e.publishedAt) : null,
    })),
    ...captionOnly.map((r) => ({ number: r.number, title: r.title as string, topic: r.topic, date: new Date(r.builtAt) })),
  ]
    .sort((a, b) => b.number - a.number)
    .map(({ number, title, topic, date }) => {
      const link = `${SITE_URL}/e/${number}`;
      return `  <item>
    <title>${esc(title)}</title>
    <link>${link}</link>
    <guid isPermaLink="true">${link}</guid>
    ${date ? `<pubDate>${date.toUTCString()}</pubDate>` : ""}
    <description>${esc(topic || "")}</description>
  </item>`;
    })
    .join("\n");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Actually Works</title>
  <link>${SITE_URL}</link>
  <description>AI setups that actually work — one a week, the exact screen and the exact click.</description>
${items}
</channel>
</rss>`;

  return new Response(xml, { headers: { "content-type": "application/rss+xml; charset=utf-8" } });
}
