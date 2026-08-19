import Link from "next/link";
import { notFound } from "next/navigation";
import { PROMPTS, bySlug } from "@/lib/prompts";
import Copy from "./copy";

export const dynamic = "force-static";
export function generateStaticParams() {
  return PROMPTS.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const p = bySlug((await params).slug);
  return p ? { title: `${p.title} — Actually Works`, description: p.blurb } : {};
}

export default async function PromptPage({ params }: { params: Promise<{ slug: string }> }) {
  const p = bySlug((await params).slug);
  if (!p) notFound();
  return (
    <div className="shell pub" dir="ltr">
      <div className="top">
        <Link className="brand" href="/join">
          <span className="tick" />
          <b>Actually Works</b>
        </Link>
        <span className="mode">Episode {String(p.episode).padStart(2, "0")}</span>
      </div>

      <h1>{p.title}</h1>
      <p className="sub" style={{ fontSize: 18 }}>{p.blurb}</p>

      <h2>Install it</h2>
      <ol className="steps">
        {p.install.map((s) => (
          <li key={s}>{s}</li>
        ))}
      </ol>

      <h2>The text</h2>
      <Copy text={p.body} />

      <div className="note warn">
        <div className="t">What it isn&apos;t</div>
        {p.limits}
      </div>

      <div className="foot">
        Every setup on this list was run before it was sent. Reply to any issue and it reaches a
        person.
      </div>
    </div>
  );
}
