import { Suspense } from "react";
import Link from "next/link";
import SiteNav from "../sitenav";
import Search from "./search";
import Reveal from "../reveal";
import { catalogue } from "@/lib/site";
import { PROMPTS } from "@/lib/prompts";
import { ARTICLES } from "@/lib/articles";

export const metadata = {
  title: "Search",
  description: "Find a setup, a prompt, or the episode that explains it.",
};
export const revalidate = 300;

export default async function SearchPage() {
  const entries = await catalogue();
  // The index is built on the server and shipped whole: at this size a search backend
  // would cost more than the page load, and this needs no round trip while typing.
  const index = [
    ...entries.map((e) => {
      const a = ARTICLES.find((x) => x.n === e.n);
      return {
        kind: "episode" as const,
        href: `/e/${e.n}`,
        title: `${String(e.n).padStart(2, "0")} · ${e.title}`,
        blurb: e.blurb,
        views: e.views,
        yt: e.ytVideoId ? `https://youtu.be/${e.ytVideoId}` : null,
        ig: e.igPermalink,
        text: [e.title, e.blurb, ...(a?.steps ?? []), ...(a?.changes ?? []),
               ...(a?.limits ?? [])].join(" ").toLowerCase(),
      };
    }),
    ...PROMPTS.map((p) => ({
      kind: "prompt" as const,
      href: `/p/${p.slug}`,
      title: p.title,
      blurb: p.blurb,
      views: null as number | null,
      yt: null as string | null,
      ig: null as string | null,
      text: [p.title, p.blurb, p.body, p.limits, ...p.install].join(" ").toLowerCase(),
    })),
  ];

  return (
    <main className="site" dir="ltr">
      <SiteNav here="/search" />
      <p className="kicker">
        <Link href="/">Actually Works</Link> · Search
      </p>
      <h1>Search</h1>
      <p className="sub">
        Every episode, every prompt, and the link to each video. Type anything — a tool, a
        word from a prompt, or what you are trying to get done.
      </p>
      <Reveal>
        <Suspense fallback={null}>
          <Search index={index} />
        </Suspense>
      </Reveal>
    </main>
  );
}
