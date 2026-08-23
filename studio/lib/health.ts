import { sharedPool } from "./db";
import { fetchInstagram, fetchBeehiiv, IgResult, BeeResult } from "./sources";
import { notify } from "./push";

/** Catches a connection dying between /api/track's once-a-day runs. The full track job stays
 *  daily on purpose (vercel-cost-efficiency: no reason to re-diff and re-write state hourly for
 *  numbers that don't move that fast) — this only re-runs the two read-only API calls and
 *  compares against the last known status, so an outage is caught within the hour instead of
 *  within the day.
 *
 *  Notifies only on a state change (idempotency-safety): a service that's been down for six
 *  hours does not need six identical pings, and a service coming back up is worth saying so it
 *  doesn't have to be checked by hand. */

type Service = "instagram" | "beehiiv";
type Status = { connected: boolean; reason: string | null };

async function table() {
  const p = sharedPool();
  if (!p) return null;
  await p.query(`create table if not exists connection_status (
    service text primary key,
    connected boolean not null,
    reason text,
    checked_at timestamptz not null default now()
  )`);
  return p;
}

async function lastKnown(service: Service): Promise<Status | null> {
  const p = await table();
  if (!p) return null;
  const r = await p.query<{ connected: boolean; reason: string | null }>(
    "select connected, reason from connection_status where service = $1",
    [service],
  );
  return r.rows[0] ?? null;
}

async function record(service: Service, s: Status): Promise<void> {
  const p = await table();
  if (!p) return;
  await p.query(
    `insert into connection_status (service, connected, reason, checked_at) values ($1, $2, $3, now())
     on conflict (service) do update set connected = $2, reason = $3, checked_at = now()`,
    [service, s.connected, s.reason],
  );
}

/** Distinguishes what actually needs doing — a token that never got set is a two-minute env-var
 *  fix; Meta blocking the app at the platform level is a Meta Dashboard problem no amount of
 *  retrying or refreshing reaches (see sources.ts's refreshInstagramToken comment). Telling them
 *  apart in the notification is the difference between him opening the right screen first try
 *  and him retrying a refresh that was never going to work. */
function actionHint(reason: string, detail?: string): string {
  const text = `${reason} ${detail ?? ""}`;
  if (/API access blocked/i.test(text)) {
    return "מטא חוסמת את האפליקציה ברמת ה-App — צריך Meta for Developers, לא רענון טוקן.";
  }
  if (/לא מוגדר/.test(reason)) {
    return "משתנה סביבה חסר ב-Vercel — בדוק Settings → Environment Variables.";
  }
  if (/40[13]/.test(reason)) {
    return "כנראה הטוקן נפסל — צריך לחבר את החשבון מחדש ולהנפיק טוקן חדש.";
  }
  return "בדוק ב-/api/connections לפרטים.";
}

async function checkOne(service: Service, r: IgResult | BeeResult): Promise<void> {
  const now: Status = { connected: r.connected, reason: r.connected ? null : r.reason };
  const prev = await lastKnown(service);
  const label = service === "instagram" ? "אינסטגרם" : "Beehiiv";

  // First-ever check for this service: record it, but don't fire — there's no prior state to
  // have "changed" from, and a fresh deploy would otherwise always send one spurious alert.
  if (prev === null) {
    await record(service, now);
    return;
  }

  if (prev.connected && !now.connected) {
    const detail = "detail" in r ? r.detail : undefined;
    await notify({
      title: `${label} התנתק`,
      body: `${now.reason} — ${actionHint(now.reason ?? "", detail)}`,
      url: "/studio",
      tag: `${service}-down`,
    }).catch(() => {});
  } else if (!prev.connected && now.connected) {
    await notify({
      title: `${label} חזר להתחבר`,
      body: "התיקון עבד — אין צורך לבדוק ידנית.",
      url: "/studio",
      tag: `${service}-up`,
    }).catch(() => {});
  }

  await record(service, now);
}

export async function checkConnections(): Promise<{
  instagram: Status;
  beehiiv: Status;
}> {
  const [ig, bee] = await Promise.all([fetchInstagram(), fetchBeehiiv()]);
  await Promise.all([checkOne("instagram", ig), checkOne("beehiiv", bee)]);
  return {
    instagram: { connected: ig.connected, reason: ig.connected ? null : ig.reason },
    beehiiv: { connected: bee.connected, reason: bee.connected ? null : bee.reason },
  };
}
