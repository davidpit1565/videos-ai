import { NextResponse } from "next/server";
import { addSubscriber, hasDb, markForwarded } from "@/lib/db";
import { BEEHIIV_PUB } from "@/lib/sources";
import { notify } from "@/lib/push";

/** A real signup, and ours.
 *
 *  The address is written to our own table first and only then handed to Beehiiv. That
 *  order is deliberate: if Beehiiv is unconfigured, rate-limited, or the key is wrong,
 *  the person still ends up on the list instead of vanishing with a friendly message.
 *  A provider outage must never cost a subscriber. */

const EMAIL = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;

async function forward(email: string, campaign: string): Promise<string | null> {
  const key = process.env.BEEHIIV_API_KEY;
  // BEEHIIV_PUB carries the public default. This line used to read the environment variable
  // directly, and with it unset every signup was silently kept to ourselves.
  const pub = BEEHIIV_PUB;
  if (!key) return "beehiiv not configured: no BEEHIIV_API_KEY";
  try {
    const r = await fetch(
      `https://api.beehiiv.com/v2/publications/${pub}/subscriptions`,
      {
        method: "POST",
        headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
        body: JSON.stringify({
          email,
          reactivate_existing: true,
          send_welcome_email: true,
          utm_source: "actually-works.com",
          utm_medium: "signup",
          utm_campaign: campaign,
        }),
      },
    );
    if (!r.ok) return `beehiiv ${r.status}: ${(await r.text()).slice(0, 200)}`;
    return null;
  } catch (e) {
    return `beehiiv unreachable: ${e instanceof Error ? e.message : String(e)}`;
  }
}

export async function POST(req: Request) {
  let email = "";
  let source = "site";
  let episode: number | undefined;
  try {
    const b = (await req.json()) as { email?: string; source?: string; episode?: number };
    email = String(b.email ?? "").trim();
    source = String(b.source ?? "site");
    episode = Number.isInteger(b.episode) && (b.episode as number) > 0 ? b.episode : undefined;
  } catch {
    return NextResponse.json({ ok: false, error: "bad request" }, { status: 400 });
  }
  // Which episode page a signup happened on is the one fact that lets it be attributed
  // later — see subscribersByEpisode() in lib/db.ts. Folded into the source column
  // itself rather than a new one, so every existing subscriber row keeps working and
  // an "episode" (no number) source still means what it always did: unknown episode.
  const attributedSource = episode ? `episode-${episode}` : source;
  if (!EMAIL.test(email) || email.length > 200) {
    return NextResponse.json(
      { ok: false, error: "That does not look like an email address." },
      { status: 422 },
    );
  }
  if (!hasDb()) {
    // Saying "thanks" while storing nothing is the one failure mode that loses a
    // subscriber silently, so it fails out loud instead.
    return NextResponse.json(
      { ok: false, error: "The list is not connected yet. Nothing was saved." },
      { status: 503 },
    );
  }
  try {
    const { created } = await addSubscriber(email, attributedSource);
    const err = await forward(email, attributedSource);
    await markForwarded(email, err ?? undefined);
    // He asked to be told about every subscriber, on every device. Never let a notification
    // failure cost the signup that triggered it — the person is already saved by this point.
    if (created) {
      void notify({
        title: "נרשם חדש",
        body: err ? `נשמר אצלנו, אבל לא הועבר ל-Beehiiv: ${err}` : "נשמר והועבר ל-Beehiiv",
        url: "/studio",
        tag: "subscriber",
      }).catch(() => {});
    }
    // Stored is what matters to the visitor; the forward is our problem, and it is
    // recorded per row so a failed batch can be replayed.
    return NextResponse.json({ ok: true, created, forwarded: !err });
  } catch (e) {
    console.error("[subscribe]", e instanceof Error ? e.message : String(e));
    return NextResponse.json(
      { ok: false, error: "Could not save that. Try again in a moment." },
      { status: 500 },
    );
  }
}
