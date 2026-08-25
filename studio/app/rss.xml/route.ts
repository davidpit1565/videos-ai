import { published, SITE_URL } from "@/lib/site";
import { realTitleFor } from "@/lib/reels";

export const revalidate = 3600;

function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/** For anyone who would rather follow a feed reader than hand an inbox to Beehiiv — same
 *  episodes, same order, no extra signup. */
export async function GET() {
  const eps = await published();
  const items = eps
    .map((e) => {
      const title = realTitleFor(e.number) || e.title;
      const link = `${SITE_URL}/e/${e.number}`;
      const date = e.publishedAt ? new Date(e.publishedAt) : null;
      return `  <item>
    <title>${esc(title)}</title>
    <link>${link}</link>
    <guid isPermaLink="true">${link}</guid>
    ${date ? `<pubDate>${date.toUTCString()}</pubDate>` : ""}
    <description>${esc(e.topic || "")}</description>
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
