import { State } from "./types";

/** A stored state outlives the shape it was written in.
 *
 *  Rows in the database predate fields the pages now assume, and the studio reads
 *  its lists plainly — `state.revenue.reduce(...)`, `state.tasks.filter(...)`,
 *  `state.episodes.map(...)`. A row missing any one of them took the whole page down
 *  with "Application error: a client-side exception has occurred".
 *
 *  Guarding four of the six lists by hand is what produced the second crash after the
 *  first was "fixed". So the list is not written by hand any more: LISTS is typed as a
 *  TOTAL map over every array-valued key of State. Add a new list to State and forget
 *  it here, and this file stops compiling — the omission cannot reach production. */
type ListKeys<T> = {
  [K in keyof T]-?: NonNullable<T[K]> extends unknown[] ? K : never;
}[keyof T];

const LISTS: Required<{ [K in ListKeys<State>]: true }> = {
  episodes: true,
  snapshots: true,
  revenue: true,
  tasks: true,
  ideas: true,
  activity: true,
};

export function whole(s: State): State {
  const out = { ...s } as unknown as Record<string, unknown>;
  for (const k of Object.keys(LISTS)) {
    if (!Array.isArray(out[k])) out[k] = [];
  }
  return out as unknown as State;
}
