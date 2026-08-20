import Link from "next/link";
import { published } from "@/lib/site";
import { PROMPTS } from "@/lib/prompts";

export const metadata = {
  title: "Actually Works — AI setups that actually work",
  description:
    "One AI setup per episode: the exact screen, the exact paste, and what breaks. No hype.",
};
export const revalidate = 300;

export default async function Home() {
  const eps = await published();
  return (
    <main className="site" dir="ltr">
      <header className="hero">
        <p className="brandline">
          <span className="tick">✓</span> Actually Works
        </p>
        <h1>
          AI setups that <em>actually work</em>.
        </h1>
        <p className="sub">
          One setup per episode. The exact screen, the exact paste, and the part that
          breaks — because the part that breaks is the part everyone else skips.
        </p>
        <Link className="cta" href="/join">
          Get each one by email
        </Link>
      </header>

      <section>
        <h2>Episodes</h2>
        {eps.length === 0 ? (
          <p className="empty">
            The first episode is finished and not published yet. It lands here the day
            it goes out.
          </p>
        ) : (
          <ol className="eps">
            {eps.map((e) => (
              <li key={e.number}>
                <Link href={`/e/${e.number}`}>
                  <span className="n">{String(e.number).padStart(2, "0")}</span>
                  <span className="t">{e.title}</span>
                  <span className="tp">{e.topic}</span>
                </Link>
              </li>
            ))}
          </ol>
        )}
      </section>

      <section>
        <h2>The prompts, in full</h2>
        <p className="sub">
          Every prompt an episode uses is here, complete, with what it cannot do. No
          email needed to read them.
        </p>
        <ul className="prompts">
          {PROMPTS.map((p) => (
            <li key={p.slug}>
              <Link href={`/p/${p.slug}`}>
                <b>{p.title}</b>
                <span>{p.blurb}</span>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <footer className="sfoot">
        <Link href="/about">About</Link>
        <Link href="/join">Email list</Link>
      </footer>
    </main>
  );
}
