import { Suspense } from "react";
import SiteNav from "../sitenav";
import EpisodesBrowser from "../episodes-browser";
import { catalogue } from "@/lib/site";

export const metadata = {
  title: "Episodes",
  description: "Every episode, newest first: a frame from the reel, what it shows, and its page with the steps.",
};
export const revalidate = 300;

export default async function EpisodesPage() {
  const eps = await catalogue();

  return (
    <main className="site" dir="ltr">
      <SiteNav here="/episodes" />
      <h1>Episodes</h1>
      <p className="sub">
        Every reel, newest first. Each one has its own page with the exact steps, the
        prompt when there is one, and what it will not do.
      </p>
      {eps.length === 0 ? (
        <p className="empty">
          The first episode is finished and not published yet. It lands here the day it
          goes out.
        </p>
      ) : (
        <Suspense fallback={null}>
          <EpisodesBrowser eps={eps} />
        </Suspense>
      )}
    </main>
  );
}
