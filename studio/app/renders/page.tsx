import Link from "next/link";
import { reels } from "@/lib/reels";
import { localDT } from "@/lib/fmt";

export const dynamic = "force-dynamic";
export const metadata = { title: "רנדרים" };

/** The list. One line per reel — the player, the gate details and the caption all moved to
 *  /renders/[file], because a page that grows by one section per episode becomes the thing
 *  he cannot find anything in. He said so directly: once there are many reels, getting to
 *  the one he wants gets hard. This page's only job now is pointing at the right one fast. */
export default function Renders() {
  const rs = reels();

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
                  ? `פרק ${r.episode}`
                  : r.file}
            </b>
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
