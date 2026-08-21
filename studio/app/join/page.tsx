import Link from "next/link";
import SiteNav from "../sitenav";
import { PROMPTS, bySlug } from "@/lib/prompts";
import Signup from "../signup";

export const metadata = {
  title: "Actually Works — get the setups",
  description: "AI setups you can copy in two minutes, including what breaks.",
};

/** The gate. The DM sends people here; Beehiiv redirects them to the prompt page after
 *  they subscribe, which is configured in Beehiiv itself — nothing here stores an email,
 *  because nothing here should. */
export default async function Join({
  searchParams,
}: {
  searchParams: Promise<{ p?: string }>;
}) {
  // the DM links here with ?p=<slug>, so the page can name what they came to claim
  const claimed = bySlug((await searchParams).p ?? "");
  return (
    <div className="shell pub" dir="ltr">
      <SiteNav />

      {claimed ? (
        <>
          <h1>
            You asked for <em>{claimed.title}</em>.
          </h1>
          <p className="sub" style={{ fontSize: 18 }}>
            {claimed.blurb} Put your email in and it opens straight away. One email a week
            after that: one AI setup, the exact screen, and the part that doesn&apos;t work.
          </p>
        </>
      ) : (
        <>
          <h1>
            The setup, and <em>what breaks</em>.
          </h1>
          <p className="sub" style={{ fontSize: 18 }}>
            Put your email in and the setup you asked for opens straight away. One email a week
            after that: one AI setup, the exact screen, and the part that doesn&apos;t work.
          </p>
        </>
      )}

      {/* Our own form, not an embed. The address is stored in our database before
          Beehiiv is called, so the list exists whether or not a provider is wired up —
          and this page stopped telling visitors to go set an environment variable. */}
      <Signup source="join" />

      <h2>What&apos;s in the library</h2>
      <ul className="list">
        {PROMPTS.map((p) => (
          <li key={p.slug}>
            <span />
            <span className="lbl">
              {p.title}
              <small>{p.blurb}</small>
            </span>
            <span />
          </li>
        ))}
      </ul>

      <div className="foot">
        Free, one email a week, unsubscribe in one click. Nothing is sold to anyone.
      </div>
      <footer className="sfoot">
        <Link href="/">Episodes</Link>
        <Link href="/prompts">All prompts</Link>
        <Link href="/search">Search</Link>
        <Link href="/about">About</Link>
      </footer>
    </div>
  );
}
