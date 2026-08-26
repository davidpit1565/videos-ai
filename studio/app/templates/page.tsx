import { TEMPLATES, MUSIC_MOODS, USED_ACCENTS } from "@/lib/templates";
import TemplateThumb from "./lightbox";

export const metadata = { title: "תבניות" };

export default function TemplatesPage() {
  return (
    <>
      <p className="eyebrow">תבניות</p>
      <h1>
        תבנית <em>מספר</em>, מוזיקה <em>מספר</em>
      </h1>
      <p className="sub">
        לפני שסוגרים על פרק חדש: "תבנית 3, מוזיקה 2" — במקום לתאר מחדש איך זה אמור להיראות
        בכל פעם.
      </p>

      <h2>תבניות עיצוב</h2>
      <div className="tplgrid">
        {TEMPLATES.map((t) => (
          <div className="tplcard" key={t.n}>
            <TemplateThumb src={t.thumb} alt={t.name} num={t.n} />
            <b>{t.name}</b>
            <p className="sub">{t.when}</p>
            {t.psychology && (
              <p className="sub" style={{ color: "var(--brass)" }}>
                <b>הפסיכולוגיה: </b>
                {t.psychology}
              </p>
            )}
          </div>
        ))}
      </div>

      <h2>מנגינות רקע</h2>
      <div className="tw eps boxed">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>שם</th>
              <th>מתי משתמשים</th>
              <th>שמיעה</th>
            </tr>
          </thead>
          <tbody>
            {MUSIC_MOODS.map((m) => (
              <tr key={m.n}>
                <td className="num">{m.n}</td>
                <td>{m.name}</td>
                <td>{m.when}</td>
                <td>
                  <audio controls preload="none" src={m.sample} style={{ height: 32, maxWidth: 200 }} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* A 4-column table with a full description column has no honest way to fit a
          phone screen — "מתי משתמשים" squeezed into a sliver wrapped to 15 lines and
          pushed the name and player off-screen. Below the .cards breakpoint this
          renders instead, one mood per card, full width. */}
      <div className="cards moodcards">
        {MUSIC_MOODS.map((m) => (
          <div className="card" key={m.n}>
            <div className="hd">
              <span className="no">{m.n}</span>
              <b>{m.name}</b>
            </div>
            <p className="sub" style={{ margin: "0 0 10px" }}>
              {m.when}
            </p>
            <audio controls preload="none" src={m.sample} style={{ width: "100%" }} />
          </div>
        ))}
      </div>
      <p className="sub">
        המספר כאן הוא בדיוק ה-<code>--mood</code> שמועבר ל-<code>produce.sh</code> — לא רשימה
        נפרדת שיכולה להתפספס. הקטע ששומעים הוא 8 שניות אמיתיות שנוצרו עם{" "}
        <code>audio/build_music.py</code>, לא תיאור.
      </p>

      <h2>צבעים שכבר שימשו</h2>
      <p className="sub">
        זוג הצבעים שכל פרק יצא איתו בפועל — כדי שהפרק הבא לא יחזור על אותו זוג בטעות.
      </p>
      <div className="tw boxed">
        <table>
          <thead>
            <tr>
              <th>פרק</th>
              <th>brass</th>
              <th>ember</th>
            </tr>
          </thead>
          <tbody>
            {USED_ACCENTS.map((a) => (
              <tr key={a.episode}>
                <td className="num">{a.episode}</td>
                <td className="num">
                  <span
                    style={{
                      display: "inline-block",
                      width: 14,
                      height: 14,
                      borderRadius: 4,
                      background: a.brass,
                      marginInlineEnd: 8,
                      verticalAlign: "middle",
                    }}
                  />
                  {a.brass}
                </td>
                <td className="num">
                  <span
                    style={{
                      display: "inline-block",
                      width: 14,
                      height: 14,
                      borderRadius: 4,
                      background: a.ember,
                      marginInlineEnd: 8,
                      verticalAlign: "middle",
                    }}
                  />
                  {a.ember}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
