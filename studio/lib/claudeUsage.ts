import { sharedPool } from "./db";

/** What this session's own account looks like right now, in the studio — his request, and
 *  explicitly not part of the channel's own data. Two different questions, and only one of
 *  them can genuinely be kept live from here:
 *
 *  "weekly" is the account's rolling 7-day rate limit — status, whether it is in overage, and
 *  when it resets. That is account-wide, so any Claude Code session can report it correctly,
 *  including a freshly spawned one with no history. A scheduled job keeps it current on its
 *  own.
 *
 *  "current" is this specific conversation's running cost and token count. That number lives
 *  inside the session doing the work — a fresh background session asked to check it would see
 *  its own near-zero numbers, not this one's. So it is only ever as fresh as the last time
 *  this session pushed it, and the studio says so rather than implying it updates on a timer
 *  it cannot actually run on. */

async function db() {
  const p = sharedPool();
  if (!p) return null;
  await p.query(`create table if not exists claude_usage (
    id int primary key default 1,
    weekly_status text, weekly_resets_at timestamptz, weekly_overage boolean,
    weekly_updated_at timestamptz,
    cost_usd numeric, input_tokens bigint, output_tokens bigint,
    cache_read_tokens bigint, cache_write_tokens bigint,
    current_updated_at timestamptz)`);
  return p;
}

export type Usage = {
  weekly: { status: string; resetsAt: string; overage: boolean; updatedAt: string } | null;
  current: {
    costUsd: number; inputTokens: number; outputTokens: number;
    cacheReadTokens: number; cacheWriteTokens: number; updatedAt: string;
  } | null;
};

export async function getUsage(): Promise<Usage | null> {
  const p = await db();
  if (!p) return null;
  const r = await p.query("select * from claude_usage where id = 1");
  const row = r.rows[0];
  if (!row) return { weekly: null, current: null };
  return {
    weekly: row.weekly_status
      ? {
          status: row.weekly_status,
          resetsAt: row.weekly_resets_at,
          overage: row.weekly_overage,
          updatedAt: row.weekly_updated_at,
        }
      : null,
    current: row.cost_usd !== null
      ? {
          costUsd: Number(row.cost_usd),
          inputTokens: Number(row.input_tokens),
          outputTokens: Number(row.output_tokens),
          cacheReadTokens: Number(row.cache_read_tokens),
          cacheWriteTokens: Number(row.cache_write_tokens),
          updatedAt: row.current_updated_at,
        }
      : null,
  };
}

export async function setWeekly(status: string, resetsAt: string, overage: boolean) {
  const p = await db();
  if (!p) throw new Error("no database");
  await p.query(
    `insert into claude_usage (id, weekly_status, weekly_resets_at, weekly_overage, weekly_updated_at)
     values (1, $1, $2, $3, now())
     on conflict (id) do update set
       weekly_status = $1, weekly_resets_at = $2, weekly_overage = $3, weekly_updated_at = now()`,
    [status, resetsAt, overage],
  );
}

export async function setCurrent(
  costUsd: number, inputTokens: number, outputTokens: number,
  cacheReadTokens: number, cacheWriteTokens: number,
) {
  const p = await db();
  if (!p) throw new Error("no database");
  await p.query(
    `insert into claude_usage (id, cost_usd, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, current_updated_at)
     values (1, $1, $2, $3, $4, $5, now())
     on conflict (id) do update set
       cost_usd = $1, input_tokens = $2, output_tokens = $3,
       cache_read_tokens = $4, cache_write_tokens = $5, current_updated_at = now()`,
    [costUsd, inputTokens, outputTokens, cacheReadTokens, cacheWriteTokens],
  );
}
