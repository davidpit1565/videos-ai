"use client";

import { useState } from "react";
import { useStudio } from "../providers";

const PRESETS = [
  "מה הפרק הבא שכדאי לי לעשות, ולמה?",
  "מה המדד היחיד שאני צריך לשפר עכשיו?",
  "לפי המספרים, מה עבד ומה לא?",
  "מה חוסם אותי מלהתחיל להרוויח?",
  "כמה נרשמים אני צריך לפני שיש טעם לדבר עם ספונסר?",
];

export default function AgentPage() {
  const { state } = useStudio();
  const [q, setQ] = useState("");
  const [busy, setBusy] = useState(false);
  const [answer, setAnswer] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);

  async function ask(question: string) {
    if (!state || !question.trim() || busy) return;
    setBusy(true);
    setErr(null);
    setAnswer(null);
    try {
      const r = await fetch("/api/agent", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ question, state }),
      });
      const j = (await r.json()) as { ok: boolean; answer?: string; reason?: string };
      if (j.ok && j.answer) setAnswer(j.answer);
      else setErr(j.reason ?? "לא התקבלה תשובה");
    } catch (e) {
      setErr((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <p className="eyebrow">סוכן</p>
      <h1>
        שאל את <em>המספרים</em>
      </h1>
      <p className="sub">
        הסוכן רואה בדיוק את מה שיש במערכת — פרקים, מדדים, תמונות צמיחה, מקורות הכנסה ומשימות
        פתוחות. הוא לא יודע כלום מעבר לזה, ואם חסר מספר הוא יגיד איזה.
      </p>

      <form
        className="ask"
        onSubmit={(e) => {
          e.preventDefault();
          ask(q);
        }}
      >
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="מה לשאול?" />
        <button className="btn" type="submit" disabled={busy || !q.trim()}>
          {busy ? <span className="spin" /> : "שאל"}
        </button>
      </form>

      <div className="presets">
        {PRESETS.map((p) => (
          <button
            key={p}
            onClick={() => {
              setQ(p);
              ask(p);
            }}
            disabled={busy}
          >
            {p}
          </button>
        ))}
      </div>

      {err && (
        <div className="note warn">
          <div className="t">לא עבד</div>
          {err}
        </div>
      )}
      {answer && <div className="answer">{answer}</div>}
      {!answer && !err && !busy && (
        <div className="note">
          <div className="t">שים לב</div>
          כרגע אין עדיין פרק באוויר, ולכן על שאלות שתלויות במדדים התשובה הנכונה היא &quot;אין מספיק
          נתונים&quot;. זה בכוונה — עדיף את זה מעל ניחוש.
        </div>
      )}
    </>
  );
}
