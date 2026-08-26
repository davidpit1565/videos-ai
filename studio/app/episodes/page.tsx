import Link from "next/link";
import SiteNav from "../sitenav";
import EpisodesBrowser from "../episodes-browser";
import Reveal from "../reveal";
import { catalogue } from "@/lib/site";

export const metadata = {
  title: "Episodes",
  description: "Every episode: the exact screen, the exact paste, and the part that breaks.",
};
export const revalidate = 300;

export default async function EpisodesPage() {
  const eps = await catalogue();

  return (
    <main className="site" dir="ltr">
      <SiteNav here="/episodes" />
      <h1>Episodes</h1>
      <p className="sub">
        One AI setup per episode. The exact screen, the exact paste, and the part that
        breaks.
      </p>
      {eps.length === 0 ? (
        <p className="empty">
          The first episode is finished and not published yet. It lands here the day it
          goes out.
        </p>
      ) : (
        <Reveal>
          <EpisodesBrowser eps={eps} />
        </Reveal>
      )}
      <footer className="sfoot">
        <Link href="/">Home</Link>
        <Link href="/prompts">Prompts</Link>
        <Link href="/search">Search</Link>
        <Link href="/join">Email list</Link>
      </footer>
    </main>
  );
}
