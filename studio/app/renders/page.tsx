import { reels } from "@/lib/reels";
import Copy from "./copy";

export const dynamic = "force-dynamic";
export const metadata = { title: "רנדרים" };

/** Where a finished reel actually lives.
 *
 *  He said it plainly: the videos do not belong in chat, they belong here. Chat lost every
 *  render to a container reset, and approving one meant holding three things at once — the
 *  file, whether it passed the gate, and the caption to post with it. They are on one screen
 *  now, in that order. */
export default function Renders() {
  const rs = reels();

  return (
    <main>
      <h1>רנדרים</h1>
      <p className="lede">
        סרטונים שממתינים לאישור שלך. כל אחד עם תוצאת השער והקפשן שלו.
        קובץ שעבר את השער אפשר לפרסם; קובץ שנפל — לא.
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

      {rs.map((r) => (
        <section key={r.file} className="render">
          <div className="rhead">
            <b>{r.episode !== null ? `פרק ${r.episode}` : r.file}</b>
            {r.gate === null ? (
              <span className="pill unknown">השער לא רץ</span>
            ) : r.gate.passed ? (
              <span className="pill pass">עבר את השער</span>
            ) : (
              <span className="pill fail">נפל בשער — לא לפרסם</span>
            )}
          </div>

          {/* controls, no autoplay: he watches it on purpose, with sound, like a viewer would */}
          <video className="player" src={r.src} controls preload="metadata" playsInline />

          <div className="meta">
            <span className="num">{(r.bytes / 1e6).toFixed(1)} MB</span>
            <span className="num">{r.builtAt.slice(0, 16).replace("T", " ")}</span>
            <a href={r.src} download>
              הורדה
            </a>
          </div>

          {r.gate && !r.gate.passed && (
            <details className="gate">
              <summary>מה נפל</summary>
              <pre>{r.gate.text}</pre>
            </details>
          )}

          {r.caption && <Copy text={r.caption} />}
        </section>
      ))}
    </main>
  );
}
