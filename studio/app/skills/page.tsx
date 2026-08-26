import Link from "next/link";
import SiteNav from "../sitenav";
import { SKILLS } from "@/lib/skills";
import SkillsBrowser from "../skills-browser";

export const metadata = {
  title: "Skills",
  description: "Every Claude Code skill this project built, in full — copy it or download it.",
};

export default function SkillsPage() {
  return (
    <main className="site" dir="ltr">
      <SiteNav here="/skills" />
      <h1>The skills, in full</h1>
      <p className="sub">
        Every skill built for this project is itself something we use daily — the exact
        file, no email needed to read it.
      </p>
      <SkillsBrowser skills={SKILLS} />
      <footer className="sfoot">
        <Link href="/">Episodes</Link>
        <Link href="/prompts">Prompts</Link>
        <Link href="/search">Search</Link>
        <Link href="/join">Email list</Link>
      </footer>
    </main>
  );
}
