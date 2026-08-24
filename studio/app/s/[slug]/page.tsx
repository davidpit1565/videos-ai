import Link from "next/link";
import SiteNav from "../../sitenav";
import { notFound } from "next/navigation";
import { SKILLS, skillBySlug } from "@/lib/skills";
import CopyOrDownload from "./copy-or-download";

export const dynamic = "force-static";
export function generateStaticParams() {
  return SKILLS.map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const s = skillBySlug((await params).slug);
  return s ? { title: `${s.title} — Actually Works`, description: s.blurb } : {};
}

export default async function SkillPage({ params }: { params: Promise<{ slug: string }> }) {
  const s = skillBySlug((await params).slug);
  if (!s) notFound();
  return (
    <div className="shell pub" dir="ltr">
      <SiteNav />
      <p className="kicker">
        {s.episode ? (
          <Link href={`/e/${s.episode}`}>Episode {String(s.episode).padStart(2, "0")}</Link>
        ) : (
          "SKILL.md"
        )}
      </p>

      <h1>{s.title}</h1>
      <p className="sub" style={{ fontSize: 18 }}>{s.blurb}</p>

      <h2>Install it</h2>
      <ol className="steps">
        <li>Download SKILL.md below, or copy the whole thing</li>
        <li>{`Put it at .claude/skills/${s.slug}/SKILL.md in your own project`}</li>
        <li>Claude Code picks it up automatically — no restart, no config</li>
      </ol>

      <h2>The file</h2>
      <CopyOrDownload text={s.body} filename={`${s.slug}.md`} />

      <div className="foot">
        Every skill on this list is one we actually run, on this project, today. Reply to
        any issue and it reaches a person.
      </div>
      <footer className="sfoot">
        <Link href="/">Episodes</Link>
        <Link href="/skills">All skills</Link>
        <Link href="/search">Search</Link>
        <Link href="/about">About</Link>
      </footer>
    </div>
  );
}
