import Link from "next/link";
import SiteNav from "../sitenav";
import { IG_HANDLE, IG_URL } from "../site-social";
import { catalogue } from "@/lib/site";
import { ARTICLES } from "@/lib/articles";

export const metadata = {
  title: "About",
  description: "Who makes Actually Works, how every episode is tested before it goes out, and Flow, the app built here.",
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
    live.length > 0 ? { v: live.length, l: `episode${live.length === 1 ? "" : "s"} published`, href: null } : null,
    breaksDocumented > 0
      ? { v: breaksDocumented, l: "failure modes written down", href: "/failure-modes" }
      : null,
    totalViews > 0 ? { v: totalViews, l: "views measured", href: null } : null,
  ].filter((x): x is { v: number; l: string; href: string | null } => x !== null);

  return (
    <main className="site" dir="ltr">
      <SiteNav here="/about" />
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
            {proof.map((p) =>
              p.href ? (
                <li key={p.l}>
                  <Link href={p.href} className="stat-link">
                    <b>{p.v.toLocaleString("en-US")}</b>
                    <span>{p.l}</span>
                  </Link>
                </li>
              ) : (
                <li key={p.l}>
                  <b>{p.v.toLocaleString("en-US")}</b>
                  <span>{p.l}</span>
                </li>
              ),
            )}
          </ul>
        )}
      </section>

      <section>
        <h2>The rule</h2>
        <p>
          Nothing gets published that has not been run. If a setup only half works, the
          episode says which half. If a number is an estimate, it is labelled as one.
          There is no reason to trust me yet, so the only thing I can offer is being
          checkable.
        </p>
      </section>

      <section>
        <h2>How an episode is made</h2>
        <ol className="steps">
          <li>
            The topic comes from data: what people search for, and what earlier reels
            showed about what gets watched.
          </li>
          <li>
            The tool gets checked live before a word is written: its current name, what it
            does today, and its limits. AI products rename and change features within weeks.
          </li>
          <li>
            It gets run for real. The text on screen is what the tool actually answered; when
            a chat is retyped for the screen, the reel says so.
          </li>
          <li>
            The narration is my own voice, cloned locally, and every line is measured for
            pacing and for word endings the clone swallows.
          </li>
          <li>
            The rendered file is checked before it is posted: text kept out of the parts
            Instagram covers, loudness, frozen or black frames. Each of those checks exists
            because a real defect got through first.
          </li>
          <li>
            Then the episode&apos;s page goes up here: the exact clicks, the prompt, and what
            it will not do.
          </li>
        </ol>
      </section>

      <section>
        <h2>Built here: Flow</h2>
        <p>
          Flow is a personal finance app: every transaction, subscription and budget is
          stored only on the device, with no account and no server. It was built through
          Actually Works and is on the App Store.
        </p>
        <p className="actions-row">
          <a
            className="button"
            href="https://apps.apple.com/us/app/id6807543350"
            target="_blank"
            rel="noopener noreferrer"
          >
            Flow on the App Store
          </a>
        </p>
      </section>

      <section>
        <h2>Work with me</h2>
        <p>
          If you want the same kind of thing built for your business, that is the paid
          side, and it is the same promise: it gets tested before it gets handed over.
          To ask about it, send a message to{" "}
          <a href={IG_URL} target="_blank" rel="noopener noreferrer">{IG_HANDLE}</a> on
          Instagram.
        </p>
      </section>

    </main>
  );
}
