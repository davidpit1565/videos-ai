import Link from "next/link";
import SiteNav from "../sitenav";
import { PROMPTS } from "@/lib/prompts";

export const metadata = {
  title: "Prompts — Actually Works",
  description: "Every prompt an episode uses, in full, with what it cannot do.",
};

export default function PromptsPage() {
  return (
    <main className="site" dir="ltr">
      <SiteNav here="/prompts" />
      <h1>The prompts, in full</h1>
      <p className="sub">
        Complete, with what each one cannot do. No email needed to read them.
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
      <footer className="sfoot">
        <Link href="/">Episodes</Link>
        <Link href="/search">Search</Link>
        <Link href="/join">Email list</Link>
      </footer>
    </main>
  );
}
