import { Pool } from "pg";
import { State } from "./types";
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

export async function loadState(): Promise<State | null> {
  const p = db();
  if (!p) return null;
  await ensure(p);
  const r = await p.query<{ data: State }>("SELECT data FROM studio_state WHERE id = 1");
  if (r.rowCount === 0) {
    const s = seed();
    await p.query("INSERT INTO studio_state (id, data) VALUES (1, $1)", [JSON.stringify(s)]);
    return s;
  }
  return r.rows[0].data;
}

export async function saveState(s: State): Promise<void> {
  const p = db();
  if (!p) throw new Error("no database configured");
  await ensure(p);
  await p.query(
    `INSERT INTO studio_state (id, data, updated_at) VALUES (1, $1, now())
     ON CONFLICT (id) DO UPDATE SET data = $1, updated_at = now()`,
    [JSON.stringify(s)],
  );
}
