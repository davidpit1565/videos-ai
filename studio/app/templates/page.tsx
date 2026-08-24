import Image from "next/image";
import { TEMPLATES, MUSIC_MOODS } from "@/lib/templates";

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
            <div className="tplthumb">
              <Image src={t.thumb} alt={t.name} width={270} height={480} />
              <span className="tplnum">{t.n}</span>
            </div>
            <b>{t.name}</b>
            <p className="sub">{t.when}</p>
          </div>
        ))}
      </div>

      <h2>מנגינות רקע</h2>
      <div className="tw">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>שם</th>
              <th>מתי משתמשים</th>
            </tr>
          </thead>
          <tbody>
            {MUSIC_MOODS.map((m) => (
              <tr key={m.n}>
                <td className="num">{m.n}</td>
                <td>{m.name}</td>
                <td>{m.when}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="sub">
        המספר כאן הוא בדיוק ה-<code>--mood</code> שמועבר ל-<code>produce.sh</code> — לא רשימה
        נפרדת שיכולה להתפספס.
      </p>
    </>
  );
}
