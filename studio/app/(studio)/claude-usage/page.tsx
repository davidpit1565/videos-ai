"use client";

import { useEffect, useMemo, useState } from "react";
import { n, usd, localDT } from "@/lib/fmt";
import { ClaudeSession } from "@/lib/db";

/** Real usage, reported by the Stop hooks running on his own machine (cost-tracker.js) —
 *  no number here is invented, and a session that never reported shows nothing, not a
 *  zero. Mirrors the agent page's own honesty rule (see app/(studio)/agent/page.tsx). */

const PRESETS = [
  "איזו שיחה עלתה הכי הרבה השבוע?",
  "יש שיחה שכדאי לי לסגור ולפתוח חדשה?",
  "כמה עלה לי היום בסך הכל?",
];

function isStale(s: ClaudeSession): boolean {
  return s.ageMinutes >= 90 || s.turns >= 30;
}

export default function ClaudeUsagePage() {
  const [sessions, setSessions] = useState<ClaudeSession[] | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [q, setQ] = useState("");
  const [busy, setBusy] = useState(false);
  const [answer, setAnswer] = useState<string | null>(null);
  const [askErr, setAskErr] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/claude-usage")
      .then((r) => r.json())
      .then((d) => {
        if (d.ok) setSessions(d.sessions ?? []);
        else setErr(d.reason ?? "שגיאה לא ידועה");
      })
      .catch((e) => setErr((e as Error).message));
  }, []);

  const totals = useMemo(() => {
    if (!sessions) return null;
    const today = new Date().toISOString().slice(0, 10);
    const todaySessions = sessions.filter((s) => s.lastSeen.slice(0, 10) === today);
    return {
      totalCostToday: todaySessions.reduce((a, s) => a + s.estimatedCostUsd, 0),
      totalCostAll: sessions.reduce((a, s) => a + s.estimatedCostUsd, 0),
      staleCount: sessions.filter(isStale).length,
    };
  }, [sessions]);

  async function ask(question: string) {
    if (!sessions || !question.trim() || busy) return;
    setBusy(true);
    setAskErr(null);
    setAnswer(null);
    try {
      const r = await fetch("/api/claude-agent", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ question, sessions }),
      });
      if (!r.ok || !r.body) {
        setAskErr(r.status === 401 ? "הקוד פג — צריך להזין אותו מחדש" : `השרת החזיר ${r.status}`);
        return;
      }
      const reader = r.body.getReader();
      const dec = new TextDecoder();
      let buf = "";
      let text = "";
      let failed: string | null = null;
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const lines = buf.split("\n");
        buf = lines.pop() ?? "";
        for (const line of lines) {
          if (!line.trim()) continue;
          let o: { t?: string; error?: string; done?: boolean };
          try {
            o = JSON.parse(line);
          } catch {
            continue;
          }
          if (o.error) failed = o.error;
          else if (o.t) {
            text += o.t;
            setAnswer(text);
          }
        }
      }
      if (failed) setAskErr(failed);
      else if (!text) setAskErr("לא התקבלה תשובה");
    } catch (e) {
      const m = (e as Error).message;
      setAskErr(m === "Load failed" || m === "Failed to fetch" ? "החיבור נפל באמצע. נסה שוב." : m);
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <p className="eyebrow">מכסה וטוקנים</p>
      <h1>
        כמה עולה <em>כל שיחה</em>
      </h1>
      <p className="sub">
        כל שורה כאן מדווחת אוטומטית מה-Stop hook שרץ על המחשב שלך בכל תגובה — לא מספר
        שהוקלד, ולא הערכה מהזיכרון. שיחה שעדיין לא דיווחה פשוט לא מופיעה כאן.
      </p>

      {err && (
        <div className="note warn">
          <div className="t">לא נטען</div>
          {err}
        </div>
      )}

      {!err && !sessions && <div className="note">טוען…</div>}

      {sessions && sessions.length === 0 && (
        <div className="note">
          <div className="t">עדיין אין נתונים</div>
          ה-hook עדיין לא דיווח שום שיחה לכתובת הזו — ודא ש-
          <code>CLAUDE_USAGE_SECRET</code> מוגדר גם ב-Vercel וגם בקובץ המקומי של ה-hook.
        </div>
      )}

      {sessions && sessions.length > 0 && totals && (
        <>
          <div className="tiles">
            <div className="tile">
              <div className="k">היום</div>
              <div className="v num">{usd(totals.totalCostToday)}</div>
              <div className="s">סכום כל השיחות שדיווחו היום</div>
            </div>
            <div className="tile">
              <div className="k">סה&quot;כ נמדד</div>
              <div className="v num">{usd(totals.totalCostAll)}</div>
              <div className="s">מאז שה-hook הותקן</div>
            </div>
            <div className="tile">
              <div className="k">שיחות שכדאי לסגור</div>
              <div className="v num">{n(totals.staleCount)}</div>
              <div className="s">מעל 90 דקות או 30 תגובות</div>
            </div>
          </div>

          <div className="tw">
            <table>
              <thead>
                <tr>
                  <th>פרויקט</th>
                  <th>מודל</th>
                  <th>תגובות</th>
                  <th>גיל</th>
                  <th>עלות</th>
                  <th>נראתה לאחרונה</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {sessions.map((s) => (
                  <tr key={s.sessionId}>
                    <td className="name">{s.project ?? "—"}</td>
                    <td>{s.model ?? "—"}</td>
                    <td className="num">{n(s.turns)}</td>
                    <td className="num">{Math.round(s.ageMinutes)} דק&apos;</td>
                    <td className="num">{usd(s.estimatedCostUsd)}</td>
                    <td className="num">{localDT(s.lastSeen)}</td>
                    <td>{isStale(s) && <span className="chip s-testing">כדאי לסגור</span>}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <form
            className="ask"
            onSubmit={(e) => {
              e.preventDefault();
              ask(q);
            }}
          >
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="מה לשאול על השיחות שלך?" />
            <button className="btn" type="submit" disabled={busy || !q.trim()}>
              {busy ? <span className="spin" /> : "שאל"}
            </button>
          </form>
          <div className="presets">
            {PRESETS.map((p) => (
              <button key={p} onClick={() => { setQ(p); ask(p); }} disabled={busy}>
                {p}
              </button>
            ))}
          </div>
          {askErr && (
            <div className="note warn">
              <div className="t">לא עבד</div>
              {askErr}
            </div>
          )}
          {answer && <div className="answer">{answer}</div>}
        </>
      )}
    </>
  );
}
