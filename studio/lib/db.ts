import { Pool } from "pg";
import { State } from "./types";
import { seed } from "./seed";

const url = process.env.DATABASE_URL || process.env.POSTGRES_URL || "";

/** Reused across invocations — a new pool per request exhausts Postgres connections. */
let pool: Pool | null = null;
function db(): Pool | null {
  if (!url) return null;
  if (!pool) pool = new Pool({ connectionString: url, max: 3, ssl: { rejectUnauthorized: false } });
  return pool;
}

export const hasDb = () => Boolean(url);

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
