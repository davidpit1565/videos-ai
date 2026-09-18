/** One serverless function for every /api/* endpoint.
 *
 *  Vercel's Hobby plan caps a deployment at 12 Serverless Functions. Each `route.ts`
 *  file under app/api used to become its own function — once the studio grew past
 *  30 endpoints, every production deploy from episode 41 onward failed at the deploy
 *  step with `exceeded_serverless_functions_per_deployment`, silently: the build itself
 *  compiled clean, so nothing in the usual build log said why the site was stuck on an
 *  old episode.
 *
 *  The fix: every route's actual logic moved from `route.ts` to a plain module named
 *  `impl.ts` (so Next.js stops treating it as its own route), and this single catch-all
 *  route dispatches every request to the right module by path. One file, one function,
 *  same exact URLs — no caller (Instagram, YouTube, Facebook, the cron, the browser)
 *  needs to change anything it calls. */

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 60;

import * as agent from "../agent/impl";
import * as beehiiv from "../beehiiv/impl";
import * as claudeAgent from "../claude-agent/impl";
import * as claudeUsage from "../claude-usage/impl";
import * as clientlog from "../clientlog/impl";
import * as connections from "../connections/impl";
import * as didStatus from "../d-id/status/impl";
import * as didSubmit from "../d-id/submit/impl";
import * as facebook from "../facebook/impl";
import * as facebookPublish from "../facebook/publish/impl";
import * as health from "../health/impl";
import * as healthCheck from "../health-check/impl";
import * as healthResolve from "../health/resolve/impl";
import * as higgsfieldStatus from "../higgsfield/status/impl";
import * as higgsfieldSubmit from "../higgsfield/submit/impl";
import * as ideaScore from "../idea-score/impl";
import * as ideasBacklog from "../ideas-backlog/impl";
import * as instagram from "../instagram/impl";
import * as instagramPublish from "../instagram/publish/impl";
import * as jarvisInstagram from "../jarvis/instagram/impl";
import * as jarvisPublish from "../jarvis/publish/impl";
import * as jarvisReels from "../jarvis/reels/impl";
import * as pushSubscribe from "../push/subscribe/impl";
import * as pushTest from "../push/test/impl";
import * as state from "../state/impl";
import * as streamCheck from "../stream-check/impl";
import * as subscribe from "../subscribe/impl";
import * as subscribePush from "../subscribe-push/impl";
import * as track from "../track/impl";
import * as unlock from "../unlock/impl";
import * as youtube from "../youtube/impl";
import * as youtubeAuth from "../youtube/auth/impl";
import * as youtubeCallback from "../youtube/callback/impl";
import * as youtubePublish from "../youtube/publish/impl";
import * as youtubeStatus from "../youtube/status/impl";

type Handler = (req: Request) => Response | Promise<Response>;
type Handlers = { GET?: Handler; POST?: Handler; PUT?: Handler; DELETE?: Handler; PATCH?: Handler };

const ROUTES: Record<string, Handlers> = {
  "agent": agent,
  "beehiiv": beehiiv,
  "claude-agent": claudeAgent,
  "claude-usage": claudeUsage,
  "clientlog": clientlog,
  "connections": connections,
  "d-id/status": didStatus,
  "d-id/submit": didSubmit,
  "facebook": facebook,
  "facebook/publish": facebookPublish,
  "health": health,
  "health-check": healthCheck,
  "health/resolve": healthResolve,
  "higgsfield/status": higgsfieldStatus,
  "higgsfield/submit": higgsfieldSubmit,
  "idea-score": ideaScore,
  "ideas-backlog": ideasBacklog,
  "instagram": instagram,
  "instagram/publish": instagramPublish,
  "jarvis/instagram": jarvisInstagram,
  "jarvis/publish": jarvisPublish,
  "jarvis/reels": jarvisReels,
  "push/subscribe": pushSubscribe,
  "push/test": pushTest,
  "state": state,
  "stream-check": streamCheck,
  "subscribe": subscribe,
  "subscribe-push": subscribePush,
  "track": track,
  "unlock": unlock,
  "youtube": youtube,
  "youtube/auth": youtubeAuth,
  "youtube/callback": youtubeCallback,
  "youtube/publish": youtubePublish,
  "youtube/status": youtubeStatus,
};

async function dispatch(
  req: Request,
  method: keyof Handlers,
  paramsPromise: Promise<{ path: string[] }>
): Promise<Response> {
  const { path } = await paramsPromise;
  const handlers = ROUTES[path.join("/")];
  const fn = handlers?.[method];
  if (!fn) return new Response("Not found", { status: 404 });
  return fn(req);
}

type Ctx = { params: Promise<{ path: string[] }> };

export async function GET(req: Request, ctx: Ctx) {
  return dispatch(req, "GET", ctx.params);
}
export async function POST(req: Request, ctx: Ctx) {
  return dispatch(req, "POST", ctx.params);
}
export async function PUT(req: Request, ctx: Ctx) {
  return dispatch(req, "PUT", ctx.params);
}
export async function DELETE(req: Request, ctx: Ctx) {
  return dispatch(req, "DELETE", ctx.params);
}
export async function PATCH(req: Request, ctx: Ctx) {
  return dispatch(req, "PATCH", ctx.params);
}
