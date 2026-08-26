import Link from "next/link";
import SiteNav from "../sitenav";
import { PROMPTS } from "@/lib/prompts";
import PromptsBrowser from "../prompts-browser";
import Reveal from "../reveal";

export const metadata = {
  title: "Prompts",
  description: "Every prompt an episode uses, in full, with what it cannot do.",
};

export default function PromptsPage() {
  return (
    <main className="site" dir="ltr">
      <SiteNav here="/prompts" />
      <p className="kicker">
        <Link href="/">Actually Works</Link> · Prompts
      </p>
      <h1>The prompts, in full</h1>
      <p className="sub">
        Complete, with what each one cannot do. No email needed to read them.
      </p>
      <Reveal>
        <PromptsBrowser prompts={PROMPTS} />
      </Reveal>
      <footer className="sfoot">
        <Link href="/">Episodes</Link>
        <Link href="/search">Search</Link>
        <Link href="/join">Email list</Link>
      </footer>
    </main>
  );
}
