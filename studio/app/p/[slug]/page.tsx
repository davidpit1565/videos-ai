import Link from "next/link";
import SiteNav from "../../sitenav";
import { notFound } from "next/navigation";
import { PROMPTS, bySlug } from "@/lib/prompts";
import Copy from "./copy";
import Reveal from "../../reveal";

export const dynamic = "force-static";
export function generateStaticParams() {
  return PROMPTS.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const p = bySlug((await params).slug);
  // bare title: the layout template already adds "· Actually Works"
  return p ? { title: p.title, description: p.blurb } : {};
}

export default async function PromptPage({ params }: { params: Promise<{ slug: string }> }) {
  const p = bySlug((await params).slug);
  if (!p) notFound();
  return (
    <main className="site" dir="ltr">
      <SiteNav />
      <p className="ep-no">
        A prompt from <Link href={`/e/${p.episode}`}>episode {p.episode}</Link>
      </p>

      <h1>{p.title}</h1>
      <p className="lede">{p.blurb}</p>

      <Reveal>
        <h2>Install it</h2>
        <ol className="steps">
          {p.install.map((s) => (
            <li key={s}>{s}</li>
          ))}
        </ol>
      </Reveal>

      <Reveal>
        <h2>The text</h2>
        <Copy text={p.body} />
      </Reveal>

      <Reveal>
        <div className="note warn">
          <div className="t">What it isn&apos;t</div>
          {p.limits}
        </div>
      </Reveal>

    </main>
  );
}
