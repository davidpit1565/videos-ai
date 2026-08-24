import Link from "next/link";
import { reels } from "@/lib/reels";
import { localDT } from "@/lib/fmt";
import { loadState } from "@/lib/db";

export const dynamic = "force-dynamic";
export const metadata = { title: "רנדרים" };

/** The list. One line per reel — the player, the gate details and the caption all moved to
 *  /renders/[file], because a page that grows by one section per episode becomes the thing
 *  he cannot find anything in. He said so directly: once there are many reels, getting to
 *  the one he wants gets hard. This page's only job now is pointing at the right one fast. */
export default async function Renders() {
  const rs = reels();
  // Whether an episode already went out is state the studio's own database holds, not
  // something a rendered file on disk can say by itself — a render sitting here doesn't
  // mean it wasn't already posted. Cross-referencing is best-effort: no DB configured
  // yet just means the badge doesn't show, not that the page fails.
  const state = await loadState().catch(() => null);
  const liveNumbers = new Set((state?.episodes ?? []).filter((e) => e.status === "live").map((e) => e.number));

  return (
    <main>
      <h1>רנדרים</h1>
      <p className="lede">
        סרטונים שממתינים לאישור שלך. לחיצה על אחד פותחת אותו עם תוצאת השער והקפשן שלו.
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
                  ? `פרק ${r.episode}${r.title ? ` — ${r.title}` : ""}`
                  : r.file}
            </b>
            {r.episode !== null && liveNumbers.has(r.episode) && (
              <span className="pill pass">כבר פורסם</span>
            )}
            {r.gate === null ? (
              <span className="pill unknown">השער לא רץ</span>
            ) : r.gate.passed ? (
              <span className="pill pass">עבר את השער</span>
            ) : (
              <span className="pill fail">נפל בשער</span>
            )}
            <span className="num rmeta">{(r.bytes / 1e6).toFixed(1)} MB</span>
            <span className="num rmeta">{localDT(r.builtAt)}</span>
          </Link>
        ))}
      </div>
    </main>
  );
}
