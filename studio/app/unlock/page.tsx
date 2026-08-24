"use client";

import { useState } from "react";
import Mark from "../mark";

export default function Unlock() {
  const [pin, setPin] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  return (
    <div className="shell" lang="he" dir="rtl" style={{ maxWidth: 420 }}>
      <div className="top">
        <span className="brand">
          <Mark />
          <b>Actually Works</b>
        </span>
      </div>
      <h1>הסטודיו</h1>
      <p className="sub">קוד אחד, פעם אחת במכשיר הזה.</p>
      <form
        className="ask"
        onSubmit={async (e) => {
          e.preventDefault();
          setBusy(true);
          setErr(null);
          const to = new URLSearchParams(location.search).get("to") || "/";
          const r = await fetch("/api/unlock", {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify({ pin }),
          });
          setBusy(false);
          if (r.ok) location.href = to;
          else setErr("קוד לא נכון");
        }}
      >
        <input
          value={pin}
          onChange={(e) => setPin(e.target.value)}
          type="password"
          inputMode="numeric"
          autoFocus
          placeholder="קוד"
        />
        <button className="btn" type="submit" disabled={busy || !pin}>
          {busy ? <span className="spin" /> : "כניסה"}
        </button>
      </form>
      {err && <div className="note warn"><div className="t">לא נכנס</div>{err}</div>}
    </div>
  );
}
