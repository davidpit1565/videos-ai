import { Pool } from "pg";
import { ReelInsightSnapshot, State } from "./types";
import { seed } from "./seed";

/** Every provider names it differently — Supabase's Vercel integration sets POSTGRES_URL
 *  and friends, Neon sets DATABASE_URL. Take the first one that exists and remember which,
 *  so the app can say what it found instead of just failing quietly. */
const CANDIDATES = [
  "DATABASE_URL",
  "POSTGRES_URL",
  "POSTGRES_URL_NON_POOLING",
  "POSTGRES_PRISMA_URL",
  "SUPABASE_DB_URL",
] as const;

function pick(): { name: string; url: string } | null {
  for (const n of CANDIDATES) {
    const v = process.env[n];
    if (v && v.startsWith("postgres")) return { name: n, url: v };
  }
  return null;
}

let pool: Pool | null = null;
let poolFor = "";

function db(): Pool | null {
  const found = pick();
  if (!found) return null;
  // Reused across invocations — a new pool per request exhausts Postgres connections.
  if (!pool || poolFor !== found.url) {
    // Supabase's pooler presents a certificate signed by its own root, which Node does
    // not carry, and pg lets `sslmode=require` in the URL turn verification back on even
    // when ssl options say otherwise — that is the "self-signed certificate in
    // certificate chain" error. Strip the parameter and state the setting explicitly.
    let conn = found.url;
    try {
      const u = new URL(found.url);
      u.searchParams.delete("sslmode");
      conn = u.toString();
    } catch {
      /* an unparseable URL is the driver's problem to report, not ours to hide */
    }
    pool = new Pool({ connectionString: conn, max: 3, ssl: { rejectUnauthorized: false } });
    poolFor = found.url;
  }
  return pool;
}

/** the shared pool, for features that own their own tables — push subscriptions do.
 *  Named differently from the module-level `pool` variable it hands out. */
export const sharedPool = db;

export const hasDb = () => pick() !== null;
/** The variable name only — never the value, which holds the password. */
export const dbVar = () => pick()?.name ?? null;

async function ensure(p: Pool) {
  await p.query(`CREATE TABLE IF NOT EXISTS studio_state (
    id int PRIMARY KEY DEFAULT 1,
    data jsonb NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT one_row CHECK (id = 1)
  )`);
}

/** Reel insight history has its own table, same reasoning as `subscribers` and
 *  `claude_sessions` above: it grows with every metric change (3,482 rows in the first
 *  three weeks, ~1 MB), and while it lived inside studio_state every page load, poll and
 *  cron run downloaded all of it — 9.35 GB of Supabase egress against a 5 GB free quota.
 *  Nothing is ever overwritten or deleted here either (see ReelInsightSnapshot). */
async function ensureSnapshots(p: Pool) {
  await p.query(`CREATE TABLE IF NOT EXISTS reel_insight_snapshots (
    id text PRIMARY KEY,
    episode_number int NOT NULL,
    collected_at timestamptz NOT NULL,
    data jsonb NOT NULL
  )`);
  await p.query(
    `CREATE INDEX IF NOT EXISTS reel_insight_snapshots_ep
     ON reel_insight_snapshots (episode_number, collected_at DESC)`,
  );
}

let migrated = false;

/** One-time move of the old in-row array into the table. Idempotent (ON CONFLICT DO
 *  NOTHING) and transactional: the array is only removed from the row in the same
 *  transaction that copied it, so a failure leaves the old data exactly where it was.
 *  Never throws — loadState must keep working even if this has to be retried. */
async function migrateSnapshots(p: Pool) {
  if (migrated) return;
  const c = await p.connect();
  try {
    await ensureSnapshots(p);
    await c.query("BEGIN");
    await c.query(
      `INSERT INTO reel_insight_snapshots (id, episode_number, collected_at, data)
       SELECT COALESCE(s->>'id', md5(s::text)),
              COALESCE((s->>'episodeNumber')::int, 0),
              COALESCE((s->>'collectedAt')::timestamptz, 'epoch'::timestamptz),
              s
       FROM studio_state, jsonb_array_elements(data->'reelInsightSnapshots') AS s
       WHERE studio_state.id = 1 AND jsonb_typeof(data->'reelInsightSnapshots') = 'array'
       ON CONFLICT (id) DO NOTHING`,
    );
    await c.query(
      `UPDATE studio_state SET data = data - 'reelInsightSnapshots'
       WHERE id = 1 AND data ? 'reelInsightSnapshots'`,
    );
    await c.query("COMMIT");
    migrated = true;
  } catch (err) {
    await c.query("ROLLBACK").catch(() => {});
    console.error("reel_insight_snapshots migration failed, will retry:", err);
  } finally {
    c.release();
  }
}

/** The newest stored snapshot for each episode — all /api/track needs to decide whether a
 *  new one is worth writing (see shouldSnapshot). */
export async function lastSnapshotsByEpisode(): Promise<Map<number, ReelInsightSnapshot>> {
  const p = db();
  const out = new Map<number, ReelInsightSnapshot>();
  if (!p) return out;
  await ensureSnapshots(p);
  const r = await p.query<{ data: ReelInsightSnapshot }>(
    `SELECT DISTINCT ON (episode_number) data FROM reel_insight_snapshots
     ORDER BY episode_number, collected_at DESC`,
  );
  for (const row of r.rows) out.set(row.data.episodeNumber, row.data);
  return out;
}

export async function appendReelSnapshots(list: ReelInsightSnapshot[]): Promise<void> {
  if (list.length === 0) return;
  const p = db();
  if (!p) throw new Error("no database configured");
  await ensureSnapshots(p);
  for (const s of list) {
    await p.query(
      `INSERT INTO reel_insight_snapshots (id, episode_number, collected_at, data)
       VALUES ($1, $2, $3, $4) ON CONFLICT (id) DO NOTHING`,
      [s.id, s.episodeNumber, s.collectedAt, JSON.stringify(s)],
    );
  }
}

export async function loadState(): Promise<State | null> {
  const p = db();
  if (!p) return null;
  await ensure(p);
  await migrateSnapshots(p);
  // `data - 'key'` is evaluated inside Postgres, so a row that still carries the old
  // array (migration not run yet) never sends it over the wire either.
  const r = await p.query<{ data: State }>(
    "SELECT data - 'reelInsightSnapshots' AS data FROM studio_state WHERE id = 1",
  );
  if (r.rowCount === 0) {
    const s = seed();
    await p.query("INSERT INTO studio_state (id, data) VALUES (1, $1)", [JSON.stringify(s)]);
    return s;
  }
  return r.rows[0].data;
}

/** `expectedUpdatedAt` turns this from a blind overwrite into a compare-and-swap: pass the
 *  `updatedAt` the caller's copy of the state was loaded with, and the write only lands if
 *  nobody else has saved since. Without it (the client's own PUT of its own edits) the
 *  write always wins, same as before — that path is one person's browser, debounced, and
 *  is meant to win. /api/track uses the guard because it runs from two independent
 *  triggers (the daily cron and a manual pull) that can genuinely overlap: without it,
 *  whichever one's write lands second silently discards everything the other one computed
 *  — new links, corrected mislinks, newly-created episode rows — with no error and no log. */
export async function saveState(
  s: State,
  expectedUpdatedAt?: string | null,
): Promise<{ ok: true } | { ok: false; conflict: true }> {
  const p = db();
  if (!p) throw new Error("no database configured");
  await ensure(p);
  // The save below replaces the whole row, so the old in-row history must already be in
  // its table. If the move has not succeeded, refuse the write rather than drop 3,000+
  // snapshots on the floor.
  await migrateSnapshots(p);
  if (!migrated) throw new Error("reel_insight_snapshots migration pending - state not saved");
  // History lives in reel_insight_snapshots now; never write it back into the hot row.
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { reelInsightSnapshots: _history, ...slim } = s;
  const body = JSON.stringify(slim);
  if (expectedUpdatedAt !== undefined) {
    const r = await p.query(
      `UPDATE studio_state SET data = $1, updated_at = now()
       WHERE id = 1 AND (data->>'updatedAt') IS NOT DISTINCT FROM $2`,
      [body, expectedUpdatedAt],
    );
    return r.rowCount === 0 ? { ok: false, conflict: true } : { ok: true };
  }
  await p.query(
    `INSERT INTO studio_state (id, data, updated_at) VALUES (1, $1, now())
     ON CONFLICT (id) DO UPDATE SET data = $1, updated_at = now()`,
    [body],
  );
  return { ok: true };
}

/** The list is the business, so it lives in our own database and not only in a
 *  provider's. Beehiiv is the sender; this table is the record. If the Beehiiv key is
 *  ever wrong, revoked, or the plan lapses, the addresses are still here. */
export async function ensureSubscribers(): Promise<Pool | null> {
  const p = db();
  if (!p) return null;
  await p.query(`CREATE TABLE IF NOT EXISTS subscribers (
    email text PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    source text,
    forwarded boolean NOT NULL DEFAULT false,
    forward_error text
  )`);
  return p;
}

export async function addSubscriber(
  email: string, source: string,
): Promise<{ created: boolean }> {
  const p = await ensureSubscribers();
  if (!p) throw new Error("no database configured");
  const r = await p.query(
    `INSERT INTO subscribers (email, source) VALUES ($1, $2)
     ON CONFLICT (email) DO NOTHING`,
    [email.toLowerCase(), source.slice(0, 60)],
  );
  return { created: (r.rowCount ?? 0) > 0 };
}

export async function markForwarded(email: string, error?: string): Promise<void> {
  const p = await ensureSubscribers();
  if (!p) return;
  await p.query(
    `UPDATE subscribers SET forwarded = $2, forward_error = $3 WHERE email = $1`,
    [email.toLowerCase(), !error, error ? error.slice(0, 300) : null],
  );
}

export async function subscriberCount(): Promise<number | null> {
  const p = await ensureSubscribers();
  if (!p) return null;
  const r = await p.query<{ n: string }>("SELECT count(*)::text AS n FROM subscribers");
  return Number(r.rows[0]?.n ?? 0);
}

/** Real per-episode attribution, computed from our own table rather than guessed by a
 *  human. /api/subscribe writes the source as "episode-N" whenever the signup happened
 *  on that episode's own page, so counting rows by that exact pattern is the whole
 *  mechanism — no Beehiiv field, no UTM parsing, nothing that can drift from what
 *  actually happened. Before this, subsAttributed was a number typed in by hand with
 *  no source at all (see the comment on that field in lib/types.ts). */
/** Claude Code usage, reported by the Stop hooks running on his own machine
 *  (~/.claude/hooks/cost-tracker.js) — this app has no other way to see them, they never
 *  touch a browser. One row per session, upserted on every report so the table stays a
 *  live snapshot per session rather than growing one row per turn (same reasoning as
 *  studio_state's single-row snapshot-per-day, not a log). Its own table for the same
 *  reason `subscribers` has one: a feature that owns high-frequency writes does not belong
 *  inside the shared JSON state blob. */
export type ClaudeSession = {
  sessionId: string;
  project: string | null;
  model: string | null;
  inputTokens: number;
  outputTokens: number;
  cacheWriteTokens: number;
  cacheReadTokens: number;
  estimatedCostUsd: number;
  turns: number;
  ageMinutes: number;
  firstSeen: string;
  lastSeen: string;
};

async function ensureClaudeUsage(p: Pool) {
  await p.query(`CREATE TABLE IF NOT EXISTS claude_sessions (
    session_id text PRIMARY KEY,
    project text,
    model text,
    input_tokens bigint NOT NULL DEFAULT 0,
    output_tokens bigint NOT NULL DEFAULT 0,
    cache_write_tokens bigint NOT NULL DEFAULT 0,
    cache_read_tokens bigint NOT NULL DEFAULT 0,
    estimated_cost_usd numeric NOT NULL DEFAULT 0,
    turns int NOT NULL DEFAULT 0,
    age_minutes numeric NOT NULL DEFAULT 0,
    first_seen timestamptz NOT NULL DEFAULT now(),
    last_seen timestamptz NOT NULL DEFAULT now()
  )`);
}

export async function upsertClaudeSession(row: {
  sessionId: string;
  project: string | null;
  model: string | null;
  inputTokens: number;
  outputTokens: number;
  cacheWriteTokens: number;
  cacheReadTokens: number;
  estimatedCostUsd: number;
  turns: number;
  ageMinutes: number;
}): Promise<void> {
  const p = db();
  if (!p) throw new Error("no database configured");
  await ensureClaudeUsage(p);
  await p.query(
    `INSERT INTO claude_sessions
       (session_id, project, model, input_tokens, output_tokens, cache_write_tokens,
        cache_read_tokens, estimated_cost_usd, turns, age_minutes, last_seen)
     VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10, now())
     ON CONFLICT (session_id) DO UPDATE SET
       project = $2, model = $3, input_tokens = $4, output_tokens = $5,
       cache_write_tokens = $6, cache_read_tokens = $7, estimated_cost_usd = $8,
       turns = $9, age_minutes = $10, last_seen = now()`,
    [
      row.sessionId, row.project, row.model, row.inputTokens, row.outputTokens,
      row.cacheWriteTokens, row.cacheReadTokens, row.estimatedCostUsd, row.turns, row.ageMinutes,
    ],
  );
}

export async function listClaudeSessions(limit = 200): Promise<ClaudeSession[]> {
  const p = db();
  if (!p) return [];
  await ensureClaudeUsage(p);
  const r = await p.query(
    `SELECT session_id, project, model, input_tokens, output_tokens, cache_write_tokens,
            cache_read_tokens, estimated_cost_usd, turns, age_minutes, first_seen, last_seen
     FROM claude_sessions ORDER BY last_seen DESC LIMIT $1`,
    [limit],
  );
  return r.rows.map((x) => ({
    sessionId: x.session_id,
    project: x.project,
    model: x.model,
    inputTokens: Number(x.input_tokens),
    outputTokens: Number(x.output_tokens),
    cacheWriteTokens: Number(x.cache_write_tokens),
    cacheReadTokens: Number(x.cache_read_tokens),
    estimatedCostUsd: Number(x.estimated_cost_usd),
    turns: Number(x.turns),
    ageMinutes: Number(x.age_minutes),
    firstSeen: x.first_seen instanceof Date ? x.first_seen.toISOString() : String(x.first_seen),
    lastSeen: x.last_seen instanceof Date ? x.last_seen.toISOString() : String(x.last_seen),
  }));
}

export async function subscribersByEpisode(): Promise<Map<number, number>> {
  const p = await ensureSubscribers();
  const out = new Map<number, number>();
  if (!p) return out;
  const r = await p.query<{ source: string; n: string }>(
    `SELECT source, count(*)::text AS n FROM subscribers
     WHERE source ~ '^episode-[0-9]+$' GROUP BY source`,
  );
  for (const row of r.rows) {
    const n = Number(row.source.slice("episode-".length));
    if (Number.isFinite(n)) out.set(n, Number(row.n));
  }
  return out;
}

/** Which /health findings a human has already looked at and dismissed — its own table,
 *  not a field on the finding itself, because the finding is recomputed from a fresh
 *  scan every time (see lib/health.ts) and has nowhere durable to carry a flag. Mirrors
 *  personal-work-studio's own rule: a finding a human marked resolved must never come
 *  back from the same source text being seen again in a later scan. */
async function ensureHealthResolved(p: Pool) {
  await p.query(`CREATE TABLE IF NOT EXISTS health_resolved (
    finding_id text PRIMARY KEY,
    resolved_at timestamptz NOT NULL DEFAULT now()
  )`);
}

export async function getResolvedHealthIds(): Promise<Set<string>> {
  const p = db();
  if (!p) return new Set();
  await ensureHealthResolved(p);
  const r = await p.query<{ finding_id: string }>("SELECT finding_id FROM health_resolved");
  return new Set(r.rows.map((x) => x.finding_id));
}

export async function resolveHealthFinding(findingId: string): Promise<void> {
  const p = db();
  if (!p) throw new Error("no database configured");
  await ensureHealthResolved(p);
  await p.query(
    "INSERT INTO health_resolved (finding_id) VALUES ($1) ON CONFLICT (finding_id) DO NOTHING",
    [findingId],
  );
}

export async function unresolveHealthFinding(findingId: string): Promise<void> {
  const p = db();
  if (!p) return;
  await ensureHealthResolved(p);
  await p.query("DELETE FROM health_resolved WHERE finding_id = $1", [findingId]);
}
