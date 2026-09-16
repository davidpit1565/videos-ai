"use client";

import { useEffect, useState } from "react";
import type { HealthFinding } from "@/lib/repoHealth";

/** A repo-health board — inspired by David's own personal-work-studio (a local tool that
 *  scans real git state for evidence-based tasks/blockers, never inventing anything it
 *  can't point back to a source). This page borrows its two real rules: every finding
 *  carries Evidence (here: file + line + the marker's own text) and a finding a human
 *  marks resolved never comes back on its own — see lib/health.ts and /api/health for
 *  why this scans text instead of git (Vercel has no live .git at runtime). */

type State = { findings: HealthFinding[]; resolvedCount: number; scannedAt: string } | null;

export default function HealthPage() {
  const [state, setState] = useState<State>(null);
  const [err, setErr] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<string | null>(null);

  function load() {
    fetch("/api/health")
      .then((r) => r.json())
      .then(setState)
      .catch((e) => setErr((e as Error).message));
  }

  useEffect(load, []);

  async function resolve(id: string) {
    setBusyId(id);
    try {
      await fetch("/api/health/resolve", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ id }),
      });
      setState((s) => (s ? { ...s, findings: s.findings.filter((f) => f.id !== id) } : s));
    } finally {
      setBusyId(null);
    }
  }

  if (err) return <p className="sub">שגיאה: {err}</p>;
  if (!state) return <p className="sub">סורק…</p>;

  const byFile = new Map<string, HealthFinding[]>();
  for (const f of state.findings) {
    const arr = byFile.get(f.file) ?? [];
    arr.push(f);
    byFile.set(f.file, arr);
  }

  return (
    <>
      <p className="eyebrow">בריאות הריפו</p>
      <h1>
        TODO/FIXME <em>אמיתיים</em>
      </h1>
      <p className="sub">
        {state.findings.length} פתוחים · {state.resolvedCount} כבר סומנו טופלו · נסרק{" "}
        {new Date(state.scannedAt).toLocaleString("he-IL")}
      </p>
      <p className="sub">
        כל שורה כאן היא ציטוט אמיתי מקובץ אמיתי בריפו (לא ניחוש) — אין כאן חיבור ל-git חי
        (Vercel לא נושא את `.git` בפריסה), אז זו סריקת טקסט על התיקיות המרכזיות, לא{" "}
        <code>git grep</code>. לחיצה על &quot;סומן&quot; לא מוחקת את השורה מהקובץ — היא רק
        מבקשת מהסריקה הבאה להתעלם ממנה.
      </p>

      {state.findings.length === 0 && <p className="sub">אין TODO/FIXME פתוחים כרגע.</p>}

      {[...byFile.entries()].map(([file, items]) => (
        <div className="note" key={file} style={{ marginTop: 14 }}>
          <p className="section-label mono">{file}</p>
          {items.map((f) => (
            <div
              key={f.id}
              style={{
                display: "flex",
                justifyContent: "space-between",
                gap: 10,
                alignItems: "flex-start",
                padding: "6px 0",
                borderTop: "1px solid var(--line, #1F2B3A)",
              }}
            >
              <div>
                <span className="hint mono">
                  שורה {f.line} · {f.marker}
                </span>
                <p style={{ margin: "2px 0 0" }}>{f.excerpt || "(אין טקסט אחרי הסימון)"}</p>
              </div>
              <button
                className="btn ghost"
                disabled={busyId === f.id}
                onClick={() => resolve(f.id)}
              >
                {busyId === f.id ? "…" : "סומן ✓"}
              </button>
            </div>
          ))}
        </div>
      ))}
    </>
  );
}
