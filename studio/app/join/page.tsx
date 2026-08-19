import Link from "next/link";
import { PROMPTS, bySlug } from "@/lib/prompts";

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
  const form = process.env.NEXT_PUBLIC_BEEHIIV_FORM || "";
  // the DM links here with ?p=<slug>, so the page can name what they came to claim
  const claimed = bySlug((await searchParams).p ?? "");
  return (
    <div className="shell pub" dir="ltr">
      <div className="top">
        <Link className="brand" href="/join">
          <span className="tick" />
          <b>Actually Works</b>
        </Link>
      </div>

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

      {form ? (
        <iframe
          src={form}
          title="Subscribe"
          className="beehiiv"
          scrolling="no"
          loading="lazy"
        />
      ) : (
        <div className="note warn">
          <div className="t">Form not connected yet</div>
          Set <b>NEXT_PUBLIC_BEEHIIV_FORM</b> to the Beehiiv embed URL and this page starts
          collecting. Beehiiv → Grow → Subscribe Forms → Embed, then set the post-subscribe
          redirect to the prompt page.
        </div>
      )}

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
    </div>
  );
}
