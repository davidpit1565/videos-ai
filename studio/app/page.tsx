"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useStudio } from "./providers";
import { saveRate, uid } from "@/lib/types";
import { eur, n, pct, today } from "@/lib/fmt";

type Bee = { connected: boolean; reason?: string; activeSubscribers?: number | null };
type Ig = { connected: boolean; reason?: string; followers?: number | null; username?: string | null };

export default function Dashboard() {
  const { state, update } = useStudio();
  const [bee, setBee] = useState<Bee | null>(null);
  const [ig, setIg] = useState<Ig | null>(null);

  useEffect(() => {
    fetch("/api/beehiiv", { cache: "no-store" }).then((r) => r.json()).then(setBee).catch(() => setBee({ connected: false, reason: "הבקשה נכשלה" }));
    fetch("/api/instagram", { cache: "no-store" }).then((r) => r.json()).then(setIg).catch(() => setIg({ connected: false, reason: "הבקשה נכשלה" }));
  }, []);

  if (!state) return <p className="sub">טוען…</p>;

  const last = state.snapshots.at(-1) ?? null;
  const live = state.episodes.filter((e) => e.status === "live");
  const subs = bee?.connected ? bee.activeSubscribers ?? null : last?.subscribers ?? null;
  const followers = ig?.connected ? ig.followers ?? null : last?.igFollowers ?? null;

  const rates = live.map(saveRate).filter((v): v is number => v != null);
  const avgSave = rates.length ? rates.reduce((a, b) => a + b, 0) / rates.length : null;
  const mrr = state.revenue.reduce((a, r) => a + (r.mrrEur || 0), 0);
  const nextTask = state.tasks.find((t) => !t.done) ?? null;

  const ranked = [...live].sort((a, b) => (saveRate(b) ?? -1) - (saveRate(a) ?? -1));

  return (
    <>
      <p className="eyebrow">לוח</p>
      <h1>
        המצב <em>כרגע</em>
      </h1>
      <p className="sub">
        המדדים היחידים שקובעים משהו בשלב הזה: כמה נרשמים לרשימה, וכמה אנשים שומרים סרטון.
        שמירות לצפייה זה הסימן שמישהו התכוון לחזור ולהשתמש בזה.
      </p>

      <div className="tiles">
        <div className="tile">
          <div className="k">נרשמים לניוזלטר</div>
          <div className="v num">{n(subs)}</div>
          <div className="s">{bee?.connected ? "חי מ-Beehiiv" : "מהתמונה האחרונה"}</div>
        </div>
        <div className="tile">
          <div className="k">עוקבים באינסטגרם</div>
          <div className="v num">{n(followers)}</div>
          <div className="s">{ig?.connected ? "חי מאינסטגרם" : "מהתמונה האחרונה"}</div>
        </div>
        <div className="tile">
          <div className="k">פרקים באוויר</div>
          <div className="v num">{n(live.length)}</div>
          <div className="s">מתוך {state.episodes.length} בצינור</div>
        </div>
        <div className="tile">
          <div className="k">שמירות לצפייה</div>
          <div className="v num">{avgSave == null ? "—" : pct(avgSave)}</div>
          <div className="s">{avgSave == null ? "אין עדיין נתונים" : "ממוצע על הפרקים באוויר"}</div>
        </div>
        <div className="tile">
          <div className="k">הכנסה חודשית</div>
          <div className="v num">{eur(mrr)}</div>
          <div className="s">מוזן ידנית לפי מה שנכנס בפועל</div>
        </div>
      </div>

      {nextTask && (
        <div className="note">
          <div className="t">הצעד הבא</div>
          <b>{nextTask.text}</b>
          {nextTask.note ? ` — ${nextTask.note}` : ""}
          <br />
          <Link href="/pipeline" style={{ color: "var(--brass)" }}>
            לרשימה המלאה →
          </Link>
        </div>
      )}

      <h2>חיבורים</h2>
      <ul className="list">
        <Conn ok={!!bee?.connected} name="Beehiiv" reason={bee?.reason} detail="מספר הנרשמים" />
        <Conn ok={!!ig?.connected} name="Instagram" reason={ig?.reason} detail={ig?.username ? `@${ig.username}` : "צפיות, שמירות, שיתופים לכל פרק"} />
        <Conn ok={false} name="YouTube" reason="לא מחובר — נוסיף כשיהיה ערוץ עם פרק אחד באוויר" detail="צפיות ומנויים" />
      </ul>
      <p className="sub" style={{ marginTop: 10 }}>
        חיבור שלא עובד מציג בדיוק איזה מפתח חסר. המפתחות נכנסים ב-Vercel → Settings → Environment
        Variables, לא לכאן ולא לגיטהאב.
      </p>

      <h2>צמיחה</h2>
      <div className="tw">
        <table>
          <thead>
            <tr>
              <th>תאריך</th>
              <th>נרשמים</th>
              <th>אינסטגרם</th>
              <th>יוטיוב</th>
              <th>הערה</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {state.snapshots.map((s, i) => (
              <tr key={s.id}>
                <td>
                  <input
                    className="cell num"
                    type="date"
                    value={s.date}
                    onChange={(e) => update((d) => void (d.snapshots[i].date = e.target.value))}
                  />
                </td>
                {(["subscribers", "igFollowers", "ytSubs"] as const).map((k) => (
                  <td key={k}>
                    <input
                      className="cell n"
                      inputMode="numeric"
                      value={s[k] ?? ""}
                      onChange={(e) =>
                        update((d) => {
                          const v = e.target.value.trim();
                          d.snapshots[i][k] = v === "" ? null : Number(v.replace(/[^\d-]/g, ""));
                        })
                      }
                    />
                  </td>
                ))}
                <td>
                  <input
                    className="cell"
                    value={s.note}
                    onChange={(e) => update((d) => void (d.snapshots[i].note = e.target.value))}
                  />
                </td>
                <td>
                  <button
                    className="del"
                    aria-label="מחיקה"
                    onClick={() => update((d) => void d.snapshots.splice(i, 1))}
                  >
                    ×
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="actions">
        <button
          className="btn"
          onClick={() =>
            update((d) =>
              void d.snapshots.push({
                id: uid(),
                date: today(),
                subscribers: subs,
                igFollowers: followers,
                ytSubs: d.snapshots.at(-1)?.ytSubs ?? null,
                note: "",
              }),
            )
          }
        >
          תמונת מצב היום
        </button>
      </div>

      <h2>מה עבד</h2>
      {ranked.length === 0 ? (
        <div className="note warn">
          <div className="t">אין עדיין מה למדוד</div>
          אף פרק לא באוויר, ולכן אין שמירות, צפיות או נרשמים לייחס לפרק. ברגע שפרק אחד מתפרסם
          ומקבל <b>igMediaId</b>, הטבלה הזאת מתמלאת לבד.
        </div>
      ) : (
        <div className="tw">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>פרק</th>
                <th>צפיות</th>
                <th>שמירות</th>
                <th>שמירות לצפייה</th>
                <th>נרשמים</th>
              </tr>
            </thead>
            <tbody>
              {ranked.map((e) => (
                <tr key={e.id}>
                  <td className="num">{e.number}</td>
                  <td className="name">{e.title}</td>
                  <td className="num">{n(e.views)}</td>
                  <td className="num">{n(e.saves)}</td>
                  <td className="num">{pct(saveRate(e))}</td>
                  <td className="num">{n(e.subsAttributed)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}

function Conn({ ok, name, reason, detail }: { ok: boolean; name: string; reason?: string; detail: string }) {
  return (
    <li>
      <span className={"dot" + (ok ? " on" : "")} />
      <span className="lbl">
        {name}
        <small>{ok ? detail : reason ?? "לא מחובר"}</small>
      </span>
      <span className="num" style={{ color: ok ? "var(--ok)" : "var(--faint)", fontSize: 11 }}>
        {ok ? "מחובר" : "לא מחובר"}
      </span>
    </li>
  );
}
