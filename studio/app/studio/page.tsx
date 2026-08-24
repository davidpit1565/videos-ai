"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useStudio } from "../providers";
import Notify from "../notify";
import { saveRate, uid } from "@/lib/types";
import { eur, localDT, n, pct, today } from "@/lib/fmt";

type Bee = {
  connected: boolean;
  reason?: string;
  activeSubscribers?: number | null;
  /** false past one page: the count is a floor, so the dashboard must not print it as
   *  the number of subscribers */
  exact?: boolean;
};
type Ig = { connected: boolean; reason?: string; followers?: number | null; username?: string | null };
type Yt = { connected: boolean; reason?: string; subscribers?: number | null; channelTitle?: string | null };

export default function Dashboard() {
  const { state, update, mode, dbVar, hint, refresh, refreshing } = useStudio();
  const [pull, setPull] = useState<string | null>(null);
  const [bee, setBee] = useState<Bee | null>(null);
  const [ig, setIg] = useState<Ig | null>(null);
  const [yt, setYt] = useState<Yt | null>(null);

  useEffect(() => {
    fetch("/api/beehiiv", { cache: "no-store" }).then((r) => r.json()).then(setBee).catch(() => setBee({ connected: false, reason: "הבקשה נכשלה" }));
    fetch("/api/instagram", { cache: "no-store" }).then((r) => r.json()).then(setIg).catch(() => setIg({ connected: false, reason: "הבקשה נכשלה" }));
    fetch("/api/youtube", { cache: "no-store" }).then((r) => r.json()).then(setYt).catch(() => setYt({ connected: false, reason: "הבקשה נכשלה" }));
  }, []);

  if (!state) return <p className="sub">טוען…</p>;

  const last = state.snapshots.at(-1) ?? null;
  const live = state.episodes.filter((e) => e.status === "live");
  const subs =
    bee?.connected && bee.exact !== false
      ? bee.activeSubscribers ?? null
      : last?.subscribers ?? null;
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

      <h2>מה קרה</h2>
      <Notify />

      <div className="actions" style={{ margin: "0 0 14px" }}>
        <button
          className="btn"
          disabled={refreshing}
          onClick={async () => {
            const r = await refresh();
            setPull(
              r.ok
                ? r.reason ?? (r.newEvents ? `${r.newEvents} עדכונים חדשים` : "אין שינוי מאז הפעם הקודמת")
                : r.reason ?? "המשיכה נכשלה",
            );
          }}
        >
          {refreshing ? <span className="spin" /> : "למשוך עכשיו"}
        </button>
        <span style={{ alignSelf: "center", color: "var(--faint)", fontSize: 14.5 }}>
          נמשך לבד כל בוקר ב-9:10 שעון ישראל
        </span>
      </div>
      {pull && <div className="note ok"><div className="t">משיכה</div>{pull}</div>}
      {(state.activity ?? []).length === 0 ? (
        <div className="note">
          <div className="t">עדיין ריק</div>
          כאן יופיע כל שינוי שקורה מעצמו — עוקב חדש, נרשם חדש, צפיות ושמירות שעלו בכל פרק,
          ופוסט באינסטגרם שעוד לא קושר לפרק. <b>אתה לא צריך להזין כלום.</b> זה מתחיל לעבוד
          ברגע שיש מסד נתונים ומפתחות.
        </div>
      ) : (
        <ul className="feed">
          {(state.activity ?? []).slice(0, 25).map((a) => (
            <li key={a.id}>
              <span className="dt">{localDT(a.at).slice(5)}</span>
              <span className="what">{a.label}</span>
              <span className={"d " + (a.delta == null ? "flat" : a.delta > 0 ? "up" : "down")}>
                {a.delta == null ? n(a.value) : (a.delta > 0 ? "+" : "") + n(a.delta)}
              </span>
            </li>
          ))}
        </ul>
      )}

      <h2>חיבורים</h2>
      <ul className="list">
        <Conn ok={!!bee?.connected} name="Beehiiv" reason={bee?.reason} detail="מספר הנרשמים" />
        <Conn ok={!!ig?.connected} name="Instagram" reason={ig?.reason} detail={ig?.username ? `@${ig.username}` : "צפיות, שמירות, שיתופים לכל פרק"} />
        <Conn ok={!!yt?.connected} name="YouTube" reason={yt?.reason} detail={yt?.channelTitle ?? "צפיות ומנויים"} />
      </ul>
      <div className={"note " + (mode === "cloud" ? "ok" : "warn")}>
        <div className="t">{mode === "cloud" ? "מסד נתונים מחובר" : "מסד נתונים לא מחובר"}</div>
        {mode === "cloud" ? (
          <>
            נמצא במשתנה <b>{dbVar}</b>. מהרגע הזה כל עריכה נשמרת בשרת, ואותו מצב בדיוק מופיע
            במק ובטלפון.
          </>
        ) : (
          <>
            {hint ?? "אין כתובת Postgres בסביבה."}
            <br />
            עד אז הכל נשמר בדפדפן הזה — אמיתי, אבל לא מסתנכרן בין מכשירים.
          </>
        )}
      </div>
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
