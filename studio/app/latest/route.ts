import { NextResponse } from "next/server";
import { catalogue } from "@/lib/site";
import { SITE_URL } from "@/lib/site";

export const dynamic = "force-dynamic";

/** The Instagram bio link's real target, so it never needs hand-editing again.
 *
 *  Root cause behind a real gap found 21.9.2026: `subsAttributed` (lib/db.ts's
 *  subscribersByEpisode) was null for 41 of 42 published episodes. The bio link has
 *  always pointed at the plain homepage (channel/launch-plan.md: "a single landing
 *  page, not a link-tree wall") — every episode's own caption promises "the setup's
 *  in the link in bio," but a viewer who taps it lands on the homepage, not that
 *  episode's own /e/N page, and the homepage's own signup form is attributed to the
 *  generic source "home" (see app/page.tsx), never to an episode number. Two losses
 *  from the same gap: no episode-level attribution, and an extra click/page between
 *  the promise ("the exact setup") and the page that actually has it.
 *
 *  Fix: this route always 307-redirects to whichever episode is currently newest —
 *  set the Instagram bio link to SITE_URL + "/latest" once, and it never goes stale.
 *  307, never a permanent redirect: a cached 308 would freeze "latest" at whatever
 *  episode was live the first time a browser or CDN saw it. */
export async function GET() {
  const eps = await catalogue();
  const newest = eps[0];
  if (!newest) return NextResponse.redirect(SITE_URL, 307);
  return NextResponse.redirect(`${SITE_URL}/e/${newest.n}`, 307);
}
