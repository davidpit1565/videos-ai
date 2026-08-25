import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/site";

/** The studio (the whole business, PIN-gated) must never be crawled or indexed — a search
 *  result linking to it would be the first anyone outside this account heard it existed.
 *  Disallowing it here is a courtesy to well-behaved crawlers only; the PIN itself, not
 *  this file, is what actually keeps it private. */
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/studio", "/videos", "/analytics", "/week", "/pipeline", "/agent", "/renders", "/templates", "/api/"],
    },
    sitemap: `${SITE_URL}/sitemap.xml`,
  };
}
