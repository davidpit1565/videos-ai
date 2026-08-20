import Link from "next/link";
import { notFound } from "next/navigation";
import { episode, published } from "@/lib/site";
import { PROMPTS } from "@/lib/prompts";

export const revalidate = 300;

export async function generateMetadata({ params }: { params: Promise<{ n: string }> }) {
  const e = await episode(Number((await params).n));
  return e
    ? { title: `${e.title} — Actually Works`, description: e.topic }
    : { title: "Actually Works" };
}

export default async function EpisodePage({ params }: { params: Promise<{ n: string }> }) {
  const n = Number((await params).n);
  if (!Number.isFinite(n)) notFound();
  const e = await episode(n);
  if (!e) notFound();
  const all = await published();
  const prompt = PROMPTS.find((p) => p.episode === n) ?? null;

  return (
    <main className="site" dir="ltr">
      <p className="kicker">
        <Link href="/">Actually Works</Link> · Episode {String(n).padStart(2, "0")}
      </p>
      <h1>{e.title}</h1>
      <p className="sub">{e.topic}</p>

      {e.ytVideoId ? (
        <div className="vid">
          <iframe
            src={`https://www.youtube-nocookie.com/embed/${e.ytVideoId}`}
            title={e.title}
            allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"
            allowFullScreen
          />
        </div>
      ) : null}

      {e.notes ? (
        <section>
          <h2>How it works</h2>
          {e.notes.split(/\n{2,}/).map((para, i) => (
            <p key={i}>{para}</p>
          ))}
        </section>
      ) : null}

      {prompt ? (
        <section>
          <h2>{prompt.title}</h2>
          <p className="sub">{prompt.blurb}</p>
          <ol className="steps">
            {prompt.install.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ol>
          <pre className="body">{prompt.body}</pre>
          <p className="limits">
            <b>What it will not do:</b> {prompt.limits}
          </p>
        </section>
      ) : null}

      <footer className="sfoot">
        {all.filter((x) => x.number !== n).slice(0, 3).map((x) => (
          <Link key={x.number} href={`/e/${x.number}`}>
            {String(x.number).padStart(2, "0")} · {x.title}
          </Link>
        ))}
        <Link href="/join">Email list</Link>
      </footer>
    </main>
  );
}
