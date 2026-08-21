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
      if (!r.ok || !r.body) {
        setErr(r.status === 401 ? "הקוד פג — צריך להזין אותו מחדש" : `השרת החזיר ${r.status}`);
        return;
      }
      // Read the answer as it arrives. Waiting for the whole body is what failed on the
      // phone: sixty seconds of silence, then "Load failed". Now the first words appear
      // in about a second and the connection is never idle.
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
        buf = lines.pop() ?? "";           // the last piece may be half a line
        for (const line of lines) {
          if (!line.trim()) continue;
          let o: { t?: string; error?: string; done?: boolean };
          try {
            o = JSON.parse(line);
          } catch {
            continue;                       // a partial line is not an error
          }
          if (o.error) failed = o.error;
          else if (o.t) {
            text += o.t;
            setAnswer(text);                // visible while it is still being written
          }
        }
      }
      if (failed) setErr(failed);
      else if (!text) setErr("לא התקבלה תשובה");
    } catch (e) {
      // a dropped connection and a server refusal are different problems
      const m = (e as Error).message;
      setErr(m === "Load failed" || m === "Failed to fetch" ? "החיבור נפל באמצע. נסה שוב." : m);
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
