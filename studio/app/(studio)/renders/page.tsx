import Link from "next/link";
import { reels, canPublish, SEQUEL_OF, SEQUEL_FOR } from "@/lib/reels";
import { localDT } from "@/lib/fmt";
import { loadState } from "@/lib/db";
import { PUBLISH_ORDER, PUBLISHED_MANUALLY } from "@/lib/publish-order";
import { igMediaState } from "@/lib/publish";
import { parseTrial } from "@/lib/trials";

/** The publish status filters. There is no "failed" filter: a failed publish is returned to the
 *  button that asked for it and is not recorded anywhere in state, so there is nothing real to filter on. */
const FILTERS = [
  { key: "all", label: "הכל" },
  { key: "published", label: "פורסם" },
  { key: "trial", label: "פורסם כטרייל" },
  { key: "graduated", label: "הוקדם לכולם" },
  { key: "ready", label: "מוכן לפרסום" },
  { key: "unpublished", label: "עוד לא פורסם" },
] as const;
type Pub = "published" | "trial" | "graduated" | "ready" | "untested" | null;

export const dynamic = "force-dynamic";
export const metadata = { title: "רנדרים" };

/** The list. One line per reel — the player, the gate details and the caption all moved to
 *  /renders/[file], because a page that grows by one section per episode becomes the thing
 *  he cannot find anything in. He said so directly: once there are many reels, getting to
 *  the one he wants gets hard. This page's only job now is pointing at the right one fast. */
export default async function Renders({ searchParams }: { searchParams: Promise<{ f?: string }> }) {
  const { f } = await searchParams;
  const filter = FILTERS.some((x) => x.key === f) ? f! : "all";
  const all = reels();
  // Whether an episode already went out is state the studio's own database holds, not
  // something a rendered file on disk can say by itself — a render sitting here doesn't
  // mean it wasn't already posted. Cross-referencing is best-effort: no DB configured
  // yet just means the badge doesn't show, not that the page fails.
  const state = await loadState().catch(() => null);
  const liveNumbers = new Set((state?.episodes ?? []).filter((e) => e.status === "live").map((e) => e.number));
  for (const n of PUBLISHED_MANUALLY) liveNumbers.add(n);
  // A reel in the publish queue that the studio calls live but whose Instagram post was deleted by hand
  // goes back to waiting (checked with Instagram itself, only for episodes in PUBLISH_ORDER).
  for (const e of state?.episodes ?? []) {
    // Only an episode Instagram CONFIRMS is still up stays "live". When Instagram cannot be asked (token dead),
    // the hand-kept PUBLISH_ORDER wins: it lists what David has not published yet. Before this, a dead token
    // made a deleted-by-hand post look live and the wrong reel (67) was shown as next.
    if (e.status === "live" && PUBLISH_ORDER.includes(e.number) && (!e.igMediaId || (await igMediaState(e.igMediaId)) !== "exists")) {
      liveNumbers.delete(e.number);
    }
  }
  // Order for deciding what to post: reels still waiting come first, lowest episode number first
  // (PUBLISH_ORDER: the order the closing lines promise each other), already-published ones after.
  const waiting = (r: (typeof all)[number]) => r.kind === "video" && canPublish(r) && (r.episode === null || !liveNumbers.has(r.episode));
  const rs = [...all].sort((a, b) => {
    const wa = waiting(a), wb = waiting(b);
    if (wa !== wb) return wa ? -1 : 1;
    if (wa) {
      const rank = (n: number | null) => { const i = n === null ? -1 : PUBLISH_ORDER.indexOf(n); return i < 0 ? 1e6 + (n ?? 1e9) : i; };
      return rank(a.episode) - rank(b.episode);
    }
    return b.builtAt.localeCompare(a.builtAt);
  });
  // Always the first waiting reel, whether or not it is in PUBLISH_ORDER: a freshly built episode that
  // nobody added to the list still sorts after the listed ones, and the badge never goes missing.
  const nextFile = rs.find(waiting)?.file ?? null;

  // Trials come from the episode's notes lines (lib/trials.ts), the same source as /trials.
  const trialOf = new Map((state?.episodes ?? []).map((e) => [e.number, parseTrial(e.notes)] as const));
  const pub = (r: (typeof all)[number]): Pub => {
    if (r.kind !== "video") return null;
    const t = r.episode !== null ? trialOf.get(r.episode) : null;
    if (t?.graduated) return "graduated";
    if (t) return "trial";
    if (r.episode !== null && liveNumbers.has(r.episode)) return "published";
    return canPublish(r) ? "ready" : "untested";
  };
  const shown = rs.filter((r) => {
    const p = pub(r);
    if (filter === "all") return true;
    if (filter === "unpublished") return p === "ready" || p === "untested";
    return p === filter;
  });

  return (
    <main>
      <h1>רנדרים</h1>
      <p className="lede">
        סרטונים שממתינים לאישור שלך. לחיצה על אחד פותחת אותו עם תוצאת השער, הקפשן, וכפתורי
        הפרסום (ריל+סטורי+פייסבוק לאינסטגרם, והעלאה ל-YouTube) — מיד אחרי הנגן.
      </p>

      <nav className="rbadges" style={{ marginTop: 14 }} aria-label="סינון לפי סטטוס פרסום">
        {FILTERS.map((x) => (
          <Link
            key={x.key}
            href={x.key === "all" ? "/renders" : `/renders?f=${x.key}`}
            className="pill"
            aria-current={filter === x.key ? "page" : undefined}
            style={filter === x.key ? { color: "var(--text)", borderColor: "var(--brass)", fontWeight: 700, textDecoration: "none" } : { color: "inherit", textDecoration: "none" }}
          >
            {x.label}
          </Link>
        ))}
      </nav>

      {rs.length > 0 && shown.length === 0 && (
        <div className="empty" style={{ marginTop: 14 }}>
          <b>אין רנדרים בסטטוס הזה.</b>
        </div>
      )}

      {rs.length === 0 && (
        <div className="empty">
          <b>אין רנדרים כרגע.</b>
          <p>
            כשבנייה מסתיימת ועוברת את השער, הקובץ נכנס ל־<code>studio/public/reels/</code>
            {" "}ומופיע כאן. הוא נשמר בגיט, כך שאיפוס מכונה לא מוחק אותו.
          </p>
        </div>
      )}

      <div className="rlist">
        {shown.map((r) => (
          <Link key={r.file} href={`/renders/${encodeURIComponent(r.file)}`} className="rrow">
            <b className="rname">
              {r.kind === "audio"
                ? r.file.replace(/\.[^.]+$/, "")
                : r.episode !== null
                  ? `ריל ${r.episode}${r.title ? ` — ${r.title}` : ""}`
                  : r.file}
            </b>
            <span className="rbadges">
              {r.file === nextFile && (
                <span className="pill" style={{ borderColor: "var(--brass)", color: "var(--brass)", fontWeight: 700 }}>הבא לפרסום</span>
              )}
              {pub(r) === "published" && <span className="pill pass">פורסם</span>}
              {pub(r) === "trial" && (
                <span className="pill" style={{ background: "#6D28D9", borderColor: "#6D28D9", color: "#fff" }}>פורסם כטרייל</span>
              )}
              {pub(r) === "graduated" && (
                <span className="pill" style={{ background: "#DDD6FE", borderColor: "#A78BFA", color: "#2E1065" }}>הוקדם לכולם</span>
              )}
              {pub(r) === "untested" && <span className="pill fail">עוד לא עבר בדיקות</span>}
              {r.episode !== null && SEQUEL_FOR[r.episode] !== undefined && (
                <span className="pill unknown">
                  חלק 2: ריל {String(SEQUEL_FOR[r.episode]).padStart(2, "0")}
                </span>
              )}
              {r.episode !== null && SEQUEL_OF[r.episode] !== undefined && (
                <span className="pill unknown">
                  חלק 2 לריל {String(SEQUEL_OF[r.episode]).padStart(2, "0")}
                </span>
              )}
              {r.gate === null ? (
                <span className="pill unknown">השער לא רץ</span>
              ) : r.gate.passed ? (
                <span className="pill pass">עבר את השער</span>
              ) : r.approval ? (
                <span className="pill pass">אושר ידנית</span>
              ) : (
                <span className="pill fail">נפל בשער</span>
              )}
              {pub(r) === "ready" && (
                <span className="pill" style={{ borderColor: "var(--brass)", color: "var(--brass)" }}>
                  מוכן לפרסום ⇢
                </span>
              )}
            </span>
            <span className="rmetas">
              <span className="num rmeta">{(r.bytes / 1e6).toFixed(1)} MB</span>
              <span className="num rmeta">{localDT(r.builtAt)}</span>
            </span>
          </Link>
        ))}
      </div>
    </main>
  );
}
