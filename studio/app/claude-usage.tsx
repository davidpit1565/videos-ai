"use client";

import { useEffect, useState } from "react";

/** His own Claude account, not the channel's data — bottom of the dashboard, its own section.
 *
 *  Three kinds of number live here, each honest about how it got there:
 *  - the two bars (session %, weekly %) come from claude.ai's own Settings > Usage screen,
 *    which nothing available to this codebase can read — so they are typed in by hand, by him
 *    or by pasting a screenshot into the chat, and the card says exactly when that last
 *    happened rather than pretending it is live.
 *  - "weekly status" is a coarser signal a background job CAN read on its own, kept as a
 *    fallback for whenever the bar above it has gone stale.
 *  - "current session cost" is a diagnostic figure, explicitly labelled as not a bill. */

const STATUS_HE: Record<string, string> = {
  allowed: "תקין",
  allowed_warning: "מתקרב למגבלה",
  blocked: "חסום",
  rejected: "חסום",
};

function rel(iso: string): string {
  const ms = Date.now() - new Date(iso).getTime();
  const h = Math.floor(ms / 3_600_000);
  if (h < 1) return "לפני פחות משעה";
  if (h < 48) return `לפני ${h} שעות`;
  return `לפני ${Math.floor(h / 24)} ימים`;
}

type Bar = { pct: number; resetsLabel: string; updatedAt: string } | null;

function Meter({ label, bar }: { label: string; bar: Bar }) {
  return (
    <div className="meter">
      <div className="mtop">
        <span>{label}</span>
        {bar && <span className="num">{bar.pct}% נוצל</span>}
      </div>
      <div className="mtrack">
        <div className="mfill" style={{ width: `${bar?.pct ?? 0}%` }} />
      </div>
      <div className="hint">
        {bar
          ? `מתאפס בעוד ${bar.resetsLabel} · הוזן ${rel(bar.updatedAt)}`
          : "לא הוזן — תעדכן ידנית, או שלח לי צילום ממסך claude.ai"}
      </div>
    </div>
  );
}

export default function ClaudeUsage() {
  const [u, setU] = useState<{
    weekly: { status: string; resetsAt: string; overage: boolean; updatedAt: string } | null;
    current: {
      costUsd: number; inputTokens: number; outputTokens: number;
      cacheReadTokens: number; cacheWriteTokens: number; updatedAt: string;
    } | null;
    bars: { session: Bar; weekly: Bar };
    reason?: string;
  } | null>(null);
  const [edit, setEdit] = useState(false);
  const [sp, setSp] = useState(""); const [sl, setSl] = useState("");
  const [wp, setWp] = useState(""); const [wl, setWl] = useState("");
  const [saving, setSaving] = useState(false);

  const load = () => { fetch("/api/claude-usage").then((r) => r.json()).then(setU).catch(() => {}); };
  useEffect(() => { load(); }, []);

  async function save() {
    setSaving(true);
    try {
      if (sp.trim()) {
        await fetch("/api/claude-usage", {
          method: "POST", headers: { "content-type": "application/json" },
          body: JSON.stringify({ type: "bar", which: "session", pct: Number(sp), resetsLabel: sl }),
        });
      }
      if (wp.trim()) {
        await fetch("/api/claude-usage", {
          method: "POST", headers: { "content-type": "application/json" },
          body: JSON.stringify({ type: "bar", which: "weekly", pct: Number(wp), resetsLabel: wl }),
        });
      }
      setSp(""); setSl(""); setWp(""); setWl(""); setEdit(false);
      await load();
    } finally {
      setSaving(false);
    }
  }

  if (!u) return null;

  return (
    <section className="usage">
      <div className="uhead">
        <b>שימוש בקלוד</b>
        <span className="num" style={{ color: "var(--faint)" }}>החשבון שלך, לא נתוני הערוץ</span>
      </div>

      {u.reason && <p className="hint">{u.reason}</p>}

      {!u.reason && (
        <>
          <Meter label="השיחה הנוכחית" bar={u.bars.session} />
          <Meter label="מגבלה שבועית" bar={u.bars.weekly} />

          {!edit ? (
            <button className="btn small" onClick={() => setEdit(true)}>
              עדכן מהמסך של claude.ai
            </button>
          ) : (
            <div className="ubaredit">
              <div className="ufield">
                <label>השיחה הנוכחית — % נוצל</label>
                <input value={sp} onChange={(e) => setSp(e.target.value)} inputMode="numeric" placeholder="34" />
                <label>מתאפס בעוד</label>
                <input value={sl} onChange={(e) => setSl(e.target.value)} placeholder="41 min" />
              </div>
              <div className="ufield">
                <label>מגבלה שבועית — % נוצל</label>
                <input value={wp} onChange={(e) => setWp(e.target.value)} inputMode="numeric" placeholder="83" />
                <label>מתאפס בעוד</label>
                <input value={wl} onChange={(e) => setWl(e.target.value)} placeholder="18 hr 41 min" />
              </div>
              <div style={{ display: "flex", gap: 8 }}>
                <button className="btn small" onClick={save} disabled={saving}>
                  {saving ? "…" : "שמור"}
                </button>
                <button className="btn small ghost" onClick={() => setEdit(false)}>ביטול</button>
              </div>
            </div>
          )}

          <details className="gate" style={{ marginTop: 14 }}>
            <summary>מספרים נוספים (אוטומטיים, כלליים יותר)</summary>
            <div className="ucols" style={{ marginTop: 10 }}>
              <div className="ucol">
                <div className="ulabel">סטטוס שבועי (מתעדכן לבד)</div>
                {u.weekly ? (
                  <>
                    <div className="uval">{STATUS_HE[u.weekly.status] ?? u.weekly.status}</div>
                    <div className="hint">
                      מתאפס {new Date(u.weekly.resetsAt).toLocaleDateString("he-IL")}
                      {u.weekly.overage ? " · במצב חריגה (overage)" : ""}
                    </div>
                    <div className="hint">עודכן {rel(u.weekly.updatedAt)}</div>
                  </>
                ) : (
                  <div className="hint">אין עדיין מדידה</div>
                )}
              </div>
              <div className="ucol">
                <div className="ulabel">השיחה הנוכחית (עדכון ידני)</div>
                {u.current ? (
                  <>
                    <div className="uval num">${u.current.costUsd.toFixed(2)}</div>
                    <div className="hint">
                      ערך שווה-כסף פנימי, לא בהכרח מה שנגבה בפועל — הסכום האמיתי הוא ב-
                      <a href="https://claude.ai/settings/billing" target="_blank" rel="noreferrer">
                        Billing
                      </a>
                    </div>
                    <div className="hint num">
                      {(u.current.inputTokens + u.current.outputTokens).toLocaleString()} טוקנים ·
                      {" "}{u.current.cacheReadTokens.toLocaleString()} מהמטמון
                    </div>
                    <div className="hint">עודכן {rel(u.current.updatedAt)}</div>
                  </>
                ) : (
                  <div className="hint">אין עדיין מדידה</div>
                )}
              </div>
            </div>
          </details>
        </>
      )}
    </section>
  );
}
