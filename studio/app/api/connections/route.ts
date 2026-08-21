import { NextResponse } from "next/server";
import { fetchInstagram, fetchBeehiiv } from "@/lib/sources";
import { dbVar } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Twice now a connection was "set" and still did not work, and each time the loop cost a
 *  day: the value was pasted into the wrong Vercel environment, or it carried a newline, or
 *  the sibling variable was missing. This endpoint answers the only question that was ever
 *  actually in doubt — is the value THERE, on THIS deployment, and does the service accept
 *  it — without ever returning the value. Shape only: present, length, prefix, whitespace.
 *  It is public on purpose: a check I cannot read myself is a check that does not end the
 *  loop. */

type Shape = {
  set: boolean;
  length: number;
  /** the first two characters, which for a token are its public family prefix (EA…, IG…) */
  starts: string;
  /** the most common invisible cause: a copied trailing newline or space */
  edgeSpace: boolean;
  innerSpace: boolean;
};

function shape(v: string | undefined): Shape {
  const raw = v ?? "";
  return {
    set: raw.length > 0,
    length: raw.length,
    starts: raw.slice(0, 2),
    edgeSpace: raw !== raw.trim(),
    innerSpace: /\s/.test(raw.trim()),
  };
}

/** A variable reported missing has four possible causes and they need different fixes:
 *  saved under a slightly different name, saved to Preview instead of Production, saved on
 *  a different Vercel project, or never saved. "Not set" cannot tell them apart, and I
 *  guessed wrong once already — I said a redeploy would fix it and the next build still
 *  came back empty. So: the NAMES of variables that look related, which are not secrets,
 *  and the total count, which distinguishes "wrong project" from "wrong name". */
const RELATED = /BEEHIIV|BEEHIV|BEHIIV|NEWSLETTER|SUBSCRIB|^IG_|INSTAGRAM|ANTHROPIC|POSTGRES|DATABASE|STUDIO_PIN/i;

function relatedNames(): string[] {
  return Object.keys(process.env).filter((k) => RELATED.test(k)).sort();
}

export async function GET() {
  const [instagram, beehiiv] = await Promise.all([fetchInstagram(), fetchBeehiiv()]);

  return NextResponse.json({
    // Which deployment answered. A variable saved for Production only is simply absent
    // here when a preview URL answers, and that looked identical to "I never saved it".
    deployment: {
      env: process.env.VERCEL_ENV ?? "local",
      branch: process.env.VERCEL_GIT_COMMIT_REF ?? null,
      commit: (process.env.VERCEL_GIT_COMMIT_SHA ?? "").slice(0, 7) || null,
    },
    // names only, never values — this is what tells a typo apart from a wrong environment
    named: relatedNames(),
    totalVars: Object.keys(process.env).length,
    vars: {
      IG_USER_ID: shape(process.env.IG_USER_ID),
      IG_ACCESS_TOKEN: shape(process.env.IG_ACCESS_TOKEN),
      BEEHIIV_API_KEY: shape(process.env.BEEHIIV_API_KEY),
      BEEHIIV_PUBLICATION_ID: shape(
        process.env.BEEHIIV_PUBLICATION_ID || "pub_92556dc6-6f7e-42ab-a414-6e291c61557c",
      ),
      // the provider decides the name (Supabase POSTGRES_URL, Neon DATABASE_URL), so
      // report the one the app actually found rather than the one I guessed
      database: { varName: dbVar(), set: dbVar() !== null },
      ANTHROPIC_API_KEY: shape(process.env.ANTHROPIC_API_KEY),
      STUDIO_PIN: { set: (process.env.STUDIO_PIN ?? "").length > 0 },
    },
    // the live verdict from the services themselves, which is the only thing that counts
    live: {
      // `via` names which of Meta's two Instagram APIs the token was sent to. It is
      // derived from the token's own prefix, so a rejection now says whether the wrong
      // API was asked rather than only that the token was refused.
      instagram: instagram.connected
        ? {
            connected: true,
            via: instagram.via,
            username: instagram.username,
            followers: instagram.followers,
          }
        : {
            connected: false,
            via: instagram.via ?? null,
            reason: instagram.reason,
            detail: instagram.detail ?? null,
          },
      beehiiv: beehiiv.connected
        ? { connected: true, activeSubscribers: beehiiv.activeSubscribers }
        : { connected: false, reason: beehiiv.reason, detail: beehiiv.detail ?? null },
    },
  });
}
