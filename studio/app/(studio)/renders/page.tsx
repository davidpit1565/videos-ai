import Link from "next/link";
import { reels, canPublish, SEQUEL_OF, SEQUEL_FOR } from "@/lib/reels";
import { localDT } from "@/lib/fmt";
import { loadState } from "@/lib/db";
import { PUBLISH_ORDER } from "@/lib/publish-order";

export const dynamic = "force-dynamic";
export const metadata = { title: "רנדרים" };

/** The list. One line per reel — the player, the gate details and the caption all moved to
 *  /renders/[file], because a page that grows by one section per episode becomes the thing
 *  he cannot find anything in. He said so directly: once there are many reels, getting to
 *  the one he wants gets hard. This page's only job now is pointing at the right one fast. */
export default async function Renders() {
  const all = reels();
  // Whether an episode already went out is state the studio's own database holds, not
  // something a rendered file on disk can say by itself — a render sitting here doesn't
  // mean it wasn't already posted. Cross-referencing is best-effort: no DB configured
  // yet just means the badge doesn't show, not that the page fails.
  const state = await loadState().catch(() => null);
  const liveNumbers = new Set((state?.episodes ?? []).filter((e) => e.status === "live").map((e) => e.number));
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
  const first = rs.find(waiting);
  const nextFile = first && first.episode !== null && PUBLISH_ORDER.includes(first.episode) ? first.file : null;

  return (
    <main>
      <h1>רנדרים</h1>
      <p className="lede">
        סרטונים שממתינים לאישור שלך. לחיצה על אחד פותחת אותו עם תוצאת השער, הקפשן, וכפתורי
        הפרסום (ריל+סטורי+פייסבוק לאינסטגרם, והעלאה ל-YouTube) — מיד אחרי הנגן.
      </p>

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
        {rs.map((r) => (
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
                <span className="pill" style={{ background: "var(--brass)", color: "#000" }}>הבא לפרסום</span>
              )}
              {r.episode !== null && liveNumbers.has(r.episode) && (
                <span className="pill pass">כבר פורסם</span>
              )}
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
              {r.kind === "video" && canPublish(r) && (!r.episode || !liveNumbers.has(r.episode)) && (
                <span className="pill" style={{ borderColor: "var(--brass)", color: "var(--brass)" }}>
                  אפשר לפרסם ⇢
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
