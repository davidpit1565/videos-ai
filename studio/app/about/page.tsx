import Link from "next/link";
import SiteNav from "../sitenav";
import Reveal from "../reveal";
import { catalogue } from "@/lib/site";
import { ARTICLES } from "@/lib/articles";

export const metadata = {
  title: "About",
  description: "Who runs this channel, and the one rule it holds to.",
};

export const revalidate = 300;

export default async function About() {
  const eps = await catalogue();
  const live = eps.filter((e) => e.live);
  const totalViews = live.reduce((a, e) => a + (e.views ?? 0), 0);
  const breaksDocumented = ARTICLES.reduce((a, ar) => a + ar.limits.length, 0);
  // Nick Saraev's own about page states hard numbers once, with no adjectives around
  // them, rather than testimonial prose — the pattern a competitor audit flagged as
  // this channel's own differentiator done right. Every figure here is one already
  // computed elsewhere on the site (the hero stats, the episode/article data) — never
  // a second, separate estimate that could quietly drift from the real one.
  const proof = [
    live.length > 0 ? { v: live.length, l: `episode${live.length === 1 ? "" : "s"} published` } : null,
    breaksDocumented > 0 ? { v: breaksDocumented, l: "failure modes written down" } : null,
    totalViews > 0 ? { v: totalViews, l: "views measured" } : null,
  ].filter((x): x is { v: number; l: string } => x !== null);

  return (
    <main className="site" dir="ltr">
      <SiteNav here="/about" />
      <p className="kicker">
        <Link href="/">Actually Works</Link> · About
      </p>
      <h1>Every setup here was run before it was published.</h1>

      <section>
        <p>
          I am David. I am eighteen, I live in Flanders, and I have a day job that is
          not this. This channel is what I do with the hours around it.
        </p>
        <p>
          It exists because of a specific frustration: almost every AI tutorial shows
          the part that works. You copy it, you get a different screen, and the video
          never mentions the step where it breaks. So that step gets the same screen
          time here as the happy path.
        </p>
        {proof.length > 0 && (
          <ul className="proofline">
            {proof.map((p) => (
              <li key={p.l}>
                <b>{p.v.toLocaleString("en-US")}</b>
                <span>{p.l}</span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <Reveal>
        <section>
          <h2>The rule</h2>
          <p>
            Nothing gets published that has not been run. If a setup only half works, the
            episode says which half. If a number is an estimate, it is labelled as one.
            There is no reason to trust me yet, so the only thing I can offer is being
            checkable.
          </p>
        </section>
      </Reveal>

      <Reveal>
        <section>
          <h2>The work behind it</h2>
          <p>
            The episodes are produced by a pipeline I built: the narration is my own voice,
            cloned locally, and every reel passes a set of measurements before it is sent —
            speech pacing, caption position against the platform's safe area, loudness,
            frozen frames. Each of those checks exists because a real defect got through
            first.
          </p>
          <p>
            If you want the same kind of thing built for your business, that is the paid
            side, and it is the same promise: it gets tested before it gets handed over.
          </p>
          <p>
            One example: Flow, a personal finance app — every transaction, subscription,
            and budget stored only on the device, no account or server. Built through
            Actually Works, currently heading toward the App Store.
          </p>
        </section>
      </Reveal>

      <footer className="sfoot">
        <Link href="/">Episodes</Link>
        <Link href="/join">Email list</Link>
      </footer>
    </main>
  );
}
