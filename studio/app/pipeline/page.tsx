"use client";

import { useEffect, useState } from "react";
import { useStudio } from "../providers";
import { STATUS_HE, STATUS_ORDER, Status, uid } from "@/lib/types";
import { eur } from "@/lib/fmt";

/** Turns the plain **bold** markers in the backlog file into real emphasis, without
 *  pulling in a markdown library for one internal page. */
function bolded(line: string) {
  const parts = line.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((p, i) =>
    p.startsWith("**") && p.endsWith("**") ? <b key={i}>{p.slice(2, -2)}</b> : <span key={i}>{p}</span>,
  );
}

function IdeasBacklog() {
  const [text, setText] = useState<string | null | undefined>(undefined);
  useEffect(() => {
    fetch("/api/ideas-backlog")
      .then((r) => r.json())
      .then((j) => setText(j.ok ? j.text : null))
      .catch(() => setText(null));
  }, []);

  if (text === undefined) return null;
  if (text === null) {
    return <p className="sub">אין עדיין קובץ רעיונות מוכן (channel/next-episode-ideas.md).</p>;
  }
  const lines = text.split("\n").filter((l) => l.trim() && !l.startsWith("# "));
  return (
    <div className="note" style={{ lineHeight: 1.8 }}>
      {lines.map((l, i) =>
        l.startsWith("## ") ? (
          <p key={i} style={{ margin: "14px 0 4px", fontWeight: 800, color: "var(--brass)" }}>
            {l.slice(3)}
          </p>
        ) : l.startsWith("---") ? (
          <hr key={i} style={{ border: 0, borderTop: "1px solid var(--line)", margin: "12px 0" }} />
        ) : (
          <p key={i} style={{ margin: "0 0 6px" }}>
            {bolded(l)}
          </p>
        ),
      )}
    </div>
  );
}

export default function Pipeline() {
  const { state, update } = useStudio();
  const [task, setTask] = useState("");
  const [idea, setIdea] = useState("");

  if (!state) return <p className="sub">טוען…</p>;

  const count = (s: Status) => state.episodes.filter((e) => e.status === s).length;
  const mrr = state.revenue.reduce((a, r) => a + (r.mrrEur || 0), 0);
  const open = state.tasks.filter((t) => !t.done).length;

  return (
    <>
      <p className="eyebrow">צינור</p>
      <h1>
        מה בעבודה, מה <em>חוסם</em>
      </h1>
      <p className="sub">
        פרק תקוע בשלב אחד יותר משבוע זה סימן שהשלב הזה הוא הצוואר בקבוק — לא שהפרק לא טוב.
      </p>

      <div className="tiles">
        {STATUS_ORDER.map((s) => (
          <div className="tile" key={s}>
            <div className="k">{STATUS_HE[s]}</div>
            <div className="v num">{count(s)}</div>
          </div>
        ))}
      </div>

      <h2>משימות · {open} פתוחות</h2>
      <ul className="list">
        {state.tasks.map((t, i) => (
          <li key={t.id} className={t.done ? "done" : undefined}>
            <input
              type="checkbox"
              checked={t.done}
              onChange={(e) => update((d) => void (d.tasks[i].done = e.target.checked))}
            />
            <span className="lbl">
              {t.text}
              {t.note && <small>{t.note}</small>}
            </span>
            <button className="del" aria-label="מחיקה" onClick={() => update((d) => void d.tasks.splice(i, 1))}>
              ×
            </button>
          </li>
        ))}
      </ul>
      <form
        className="ask"
        style={{ marginTop: 12 }}
        onSubmit={(e) => {
          e.preventDefault();
          const text = task.trim();
          if (!text) return;
          update((d) => void d.tasks.push({ id: uid(), text, note: "", done: false }));
          setTask("");
        }}
      >
        <input value={task} onChange={(e) => setTask(e.target.value)} placeholder="משימה חדשה" />
        <button className="btn" type="submit">
          הוספה
        </button>
      </form>

      <h2>מוכן מראש · 5 רעיונות לפרקים הבאים</h2>
      <p className="sub">
        נכתב מראש כדי שכל פעם שאומרים "תכין את הפרק הבא" כבר יש ממה לבחור, בלי לחשוב
        מאפס. מבוסס על ביקוש נמדד ב-<code>demand-report.md</code>. עדכון עצמו — כל פעם
        שכלי מהרשימה משמש לפרק, כדאי להוסיף רעיון חדש במקומו.
      </p>
      <IdeasBacklog />

      <h2>רעיונות אחרים</h2>
      <ul className="list">
        {state.ideas.map((x, i) => (
          <li key={x.id}>
            <span />
            <span className="lbl">{x.text}</span>
            <span style={{ display: "flex", gap: 4 }}>
              <button
                className="btn ghost"
                style={{ padding: "4px 9px", fontSize: 12 }}
                onClick={() =>
                  update((d) => {
                    // i is captured at render; two taps before the re-render run this
                    // twice and the second finds nothing there
                    const it = d.ideas[i];
                    if (!it) return;
                    d.episodes.push({
                      id: uid(),
                      number: Math.max(0, ...d.episodes.map((e) => e.number)) + 1,
                      title: it.text,
                      format: "reel",
                      status: "idea",
                      topic: "",
                      tested: false,
                      publishedAt: null,
                      igMediaId: null,
                      ytVideoId: null,
                      notes: "",
                      views: null,
                      likes: null,
                      saves: null,
                      comments: null,
                      shares: null,
                      subsAttributed: null,
                    });
                    d.ideas.splice(i, 1);
                  })
                }
              >
                לצינור
              </button>
              <button className="del" aria-label="מחיקה" onClick={() => update((d) => void d.ideas.splice(i, 1))}>
                ×
              </button>
            </span>
          </li>
        ))}
      </ul>
      <form
        className="ask"
        style={{ marginTop: 12 }}
        onSubmit={(e) => {
          e.preventDefault();
          const text = idea.trim();
          if (!text) return;
          update((d) => void d.ideas.push({ id: uid(), text }));
          setIdea("");
        }}
      >
        <input value={idea} onChange={(e) => setIdea(e.target.value)} placeholder="רעיון חדש" />
        <button className="btn" type="submit">
          הוספה
        </button>
      </form>

      <h2>מקורות הכנסה · {eur(mrr)} בחודש</h2>
      <div className="tw">
        <table>
          <thead>
            <tr>
              <th>מקור</th>
              <th>שלב</th>
              <th>€ בחודש</th>
              <th>דורש קהל</th>
              <th>הצעד הבא</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {state.revenue.map((r, i) => (
              <tr key={r.id}>
                <td className="name">
                  <input className="cell" value={r.name} onChange={(e) => update((d) => void (d.revenue[i].name = e.target.value))} />
                </td>
                <td>
                  <select
                    className="cell"
                    value={r.status}
                    onChange={(e) => update((d) => void (d.revenue[i].status = e.target.value as Status))}
                  >
                    {STATUS_ORDER.map((s) => (
                      <option key={s} value={s}>
                        {STATUS_HE[s]}
                      </option>
                    ))}
                  </select>
                </td>
                <td>
                  <input
                    className="cell n"
                    inputMode="numeric"
                    value={r.mrrEur || ""}
                    onChange={(e) =>
                      update((d) => void (d.revenue[i].mrrEur = Number(e.target.value.replace(/[^\d]/g, "") || 0)))
                    }
                  />
                </td>
                <td>
                  <input
                    className="cell"
                    value={r.needsAudience}
                    onChange={(e) => update((d) => void (d.revenue[i].needsAudience = e.target.value))}
                  />
                </td>
                <td>
                  <input
                    className="cell"
                    value={r.nextStep}
                    onChange={(e) => update((d) => void (d.revenue[i].nextStep = e.target.value))}
                  />
                </td>
                <td>
                  <button className="del" aria-label="מחיקה" onClick={() => update((d) => void d.revenue.splice(i, 1))}>
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
          className="btn ghost"
          onClick={() =>
            update((d) =>
              void d.revenue.push({ id: uid(), name: "מקור חדש", status: "idea", mrrEur: 0, needsAudience: "", nextStep: "" }),
            )
          }
        >
          + מקור הכנסה
        </button>
      </div>
    </>
  );
}
