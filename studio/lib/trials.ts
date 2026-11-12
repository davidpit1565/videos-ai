/** Trial Reels as recorded in an episode row's `notes` (shared by /trials and /renders):
 *    TRIAL <MANUAL|SS_PERFORMANCE> <mediaId> <permalink> <YYYY-MM-DD>  written by lib/publish.ts
 *    TRIAL-MANUAL <YYYY-MM-DD HH:MM>   a trial posted by hand in the Instagram app
 *    TRIAL-GRADUATED <YYYY-MM-DD>      graduated to everyone by hand in the app
 *  A trial keeps the episode's own number: it is a way of publishing that episode. */
export type Trial = {
  kind: "api" | "manual";
  mode?: string;
  mediaId?: string;
  permalink?: string;
  date: string | null;
  graduated: string | null;
};

export function parseTrial(notes: string | null | undefined): Trial | null {
  const lines = (notes ?? "").split("\n").map((l) => l.trim());
  let t: Trial | null = null;
  let graduated: string | null = null;
  for (const l of lines) {
    const g = /^TRIAL-GRADUATED\b\s*(.*)$/.exec(l);
    if (g) { graduated = g[1].trim() || "—"; continue; }
    const m = /^TRIAL-MANUAL\b\s*(.*)$/.exec(l);
    if (m) { t ??= { kind: "manual", date: m[1].trim() || null, graduated: null }; continue; }
    const a = /^TRIAL\s+(\S+)\s+(\S+)\s+(.*)$/.exec(l);
    if (a) {
      // the permalink may be empty (publish.ts writes `${permalink ?? ""}`), so the date is the last token
      const rest = a[3].trim().split(/\s+/).filter(Boolean);
      const date = rest.length && /^\d{4}-\d{2}-\d{2}$/.test(rest[rest.length - 1]) ? rest.pop()! : null;
      t = { kind: "api", mode: a[1], mediaId: a[2], permalink: rest[0], date, graduated: null };
    }
  }
  if (!t && graduated) t = { kind: "manual", date: null, graduated: null };
  if (t) t.graduated = graduated;
  return t;
}
