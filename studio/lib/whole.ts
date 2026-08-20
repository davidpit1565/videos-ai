import { ActivityEvent, State } from "./types";

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
    const v = out[k];
    // a null hole in a list is as fatal as a missing list: `episodes.filter(e => e.status)`
    out[k] = Array.isArray(v) ? v.filter((x) => x != null) : [];
  }
  // Containers were guaranteed; members were not. ActivityEvent.at is declared required,
  // so nothing here knows it can be absent — but an event written by an earlier tracker
  // has no `at`, and the dashboard does `a.at.slice(5, 16)` on open. The activity feed
  // only exists in production, because the cron is what writes it, which is exactly why
  // a local reproduction of the crash came back clean.
  out.activity = (out.activity as ActivityEvent[]).map((a) => ({
    ...a,
    at: typeof a.at === "string" ? a.at : "",
    label: typeof a.label === "string" ? a.label : "",
  }));
  return out as unknown as State;
}
