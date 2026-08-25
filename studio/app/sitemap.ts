import type { MetadataRoute } from "next";
import { published, SITE_URL } from "@/lib/site";
import { ARTICLES } from "@/lib/articles";
import { PROMPTS } from "@/lib/prompts";
import { SKILLS } from "@/lib/skills";

export const revalidate = 3600;

/** Every URL the front door actually wants Google to know exists. An episode page exists
 *  the moment either the studio marks it live or its article is written (see lib/site.ts's
 *  episode()) — same rule here, so this list is never behind what a visitor can already
 *  open, and never ahead of it either. */
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const live = await published();
  const numbers = new Set([...live.map((e) => e.number), ...ARTICLES.map((a) => a.n)]);

  const episodes: MetadataRoute.Sitemap = [...numbers].map((n) => {
    const e = live.find((x) => x.number === n);
    return {
      url: `${SITE_URL}/e/${n}`,
      lastModified: e?.publishedAt ? new Date(e.publishedAt) : undefined,
      changeFrequency: "monthly",
      priority: 0.8,
    };
  });

  const prompts: MetadataRoute.Sitemap = PROMPTS.map((p) => ({
    url: `${SITE_URL}/p/${p.slug}`,
    changeFrequency: "monthly",
    priority: 0.5,
  }));

  const skills: MetadataRoute.Sitemap = SKILLS.map((s) => ({
    url: `${SITE_URL}/s/${s.slug}`,
    changeFrequency: "monthly",
    priority: 0.5,
  }));

  const pages: MetadataRoute.Sitemap = [
    { url: SITE_URL, changeFrequency: "daily", priority: 1 },
    { url: `${SITE_URL}/episodes`, changeFrequency: "daily", priority: 0.9 },
    { url: `${SITE_URL}/prompts`, changeFrequency: "weekly", priority: 0.6 },
    { url: `${SITE_URL}/skills`, changeFrequency: "weekly", priority: 0.6 },
    { url: `${SITE_URL}/about`, changeFrequency: "monthly", priority: 0.3 },
    { url: `${SITE_URL}/join`, changeFrequency: "monthly", priority: 0.4 },
  ];

  return [...pages, ...episodes, ...prompts, ...skills];
}
