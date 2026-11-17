import Link from "next/link";
import SiteNav from "../../sitenav";
import { notFound } from "next/navigation";
import { SKILLS, skillBySlug } from "@/lib/skills";
import CopyOrDownload from "./copy-or-download";
import Reveal from "../../reveal";

export const dynamic = "force-static";
export function generateStaticParams() {
  return SKILLS.map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const s = skillBySlug((await params).slug);
  // bare title: the layout template already adds "· Actually Works"
  return s ? { title: s.title, description: s.blurb } : {};
}

export default async function SkillPage({ params }: { params: Promise<{ slug: string }> }) {
  const s = skillBySlug((await params).slug);
  if (!s) notFound();
  return (
    <main className="site" dir="ltr">
      <SiteNav />
      {s.episode ? (
        <p className="ep-no">
          A skill from <Link href={`/e/${s.episode}`}>episode {s.episode}</Link>
        </p>
      ) : null}

      <h1>{s.title}</h1>
      <p className="lede">{s.blurb}</p>

      <Reveal>
        <h2>Install it</h2>
        <ol className="steps">
          <li>Download SKILL.md below, or copy the whole thing</li>
          <li>{`Put it at .claude/skills/${s.slug}/SKILL.md in your own project`}</li>
          <li>Claude Code picks it up automatically — no restart, no config</li>
        </ol>
      </Reveal>

      <Reveal>
        <h2>The file</h2>
        <CopyOrDownload text={s.body} filename={`${s.slug}.md`} />
      </Reveal>

    </main>
  );
}
