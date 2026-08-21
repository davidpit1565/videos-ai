import Link from "next/link";
import SiteNav from "../../sitenav";
import { notFound } from "next/navigation";
import { episode, published } from "@/lib/site";
import { articleFor, promptFor, ARTICLES } from "@/lib/articles";

export const revalidate = 300;

export async function generateMetadata({ params }: { params: Promise<{ n: string }> }) {
  const n = Number((await params).n);
  const a = articleFor(n);
  const e = await episode(n);
  const title = e?.title || a?.title;
  return title
    ? { title, description: a?.standfirst ?? e?.topic }
    // absolute: the front door is the brand itself, not "Actually Works · Actually Works"
    : { title: { absolute: "Actually Works" } };
}

export default async function EpisodePage({ params }: { params: Promise<{ n: string }> }) {
  const n = Number((await params).n);
  if (!Number.isFinite(n)) notFound();

  // The page exists if EITHER the studio has published the episode or the article is
  // written. Requiring both meant the link in a caption 404'd until someone remembered
  // to flip a switch — and the caption is printed the moment the reel goes out.
  const e = await episode(n);
  const a = articleFor(n);
  if (!e && !a) notFound();

  const prompt = promptFor(a);
  const title = e?.title || a!.title;
  const others = (await published()).filter((x) => x.number !== n);
  const more = others.length
    ? others.slice(0, 3).map((x) => ({ n: x.number, t: x.title }))
    : ARTICLES.filter((x) => x.n !== n).slice(0, 3).map((x) => ({ n: x.n, t: x.title }));

  return (
    <main className="site" dir="ltr">
      <SiteNav />
      <p className="kicker">
        <Link href="/">Actually Works</Link> · Episode {String(n).padStart(2, "0")}
      </p>
      <h1>{title}</h1>
      {a ? <p className="sub">{a.standfirst}</p> : e?.topic ? <p className="sub">{e.topic}</p> : null}

      {e?.ytVideoId ? (
        <div className="vid">
          <iframe
            src={`https://www.youtube-nocookie.com/embed/${e.ytVideoId}`}
            title={title}
            allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"
            allowFullScreen
          />
        </div>
      ) : null}

      {a ? (
        <>
          <section>
            <h2>The exact clicks</h2>
            <ol className="steps">
              {a.steps.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ol>
          </section>

          {prompt ? (
            <section>
              <h2>The prompt</h2>
              <pre className="body">{prompt.body}</pre>
              <p className="sub">
                Copy all of it. <Link href={`/p/${prompt.slug}`}>Its own page</Link> has it
                too, if this one is awkward to select on a phone.
              </p>
            </section>
          ) : null}

          <section>
            <h2>What changes</h2>
            <ul className="changes">
              {a.changes.map((c, i) => (
                <li key={i}>{c}</li>
              ))}
            </ul>
          </section>

          <section>
            <h2>What it will not do</h2>
            <ul className="limits-list">
              {a.limits.map((l, i) => (
                <li key={i}>{l}</li>
              ))}
            </ul>
          </section>
        </>
      ) : null}

      {e?.notes ? (
        <section>
          <h2>Notes</h2>
          {e.notes.split(/\n{2,}/).map((p, i) => (
            <p key={i}>{p}</p>
          ))}
        </section>
      ) : null}

      <footer className="sfoot">
        {more.map((x) => (
          <Link key={x.n} href={`/e/${x.n}`}>
            {String(x.n).padStart(2, "0")} · {x.t}
          </Link>
        ))}
        <Link href="/join">Email list</Link>
      </footer>
    </main>
  );
}
