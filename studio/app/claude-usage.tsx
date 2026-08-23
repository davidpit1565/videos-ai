"use client";

import { useEffect, useState } from "react";

/** He asked for this explicitly: not the channel's data, his own Claude account. It sits at
 *  the bottom of the dashboard because it is a side panel, not part of the business the rest
 *  of the page tracks.
 *
 *  The two halves update on genuinely different schedules and the card says so rather than
 *  implying one behaviour for both. "Weekly" is the account's rolling 7-day limit — a
 *  scheduled job can check it from anywhere and it is always right. "Current" is this one
 *  conversation's running cost, which only the session doing the work can see, so it is only
 *  ever as fresh as the last time that session pushed it. */

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

export default function ClaudeUsage() {
  const [u, setU] = useState<{
    weekly: { status: string; resetsAt: string; overage: boolean; updatedAt: string } | null;
    current: {
      costUsd: number; inputTokens: number; outputTokens: number;
      cacheReadTokens: number; cacheWriteTokens: number; updatedAt: string;
    } | null;
    reason?: string;
  } | null>(null);

  useEffect(() => {
    fetch("/api/claude-usage").then((r) => r.json()).then(setU).catch(() => {});
  }, []);

  if (!u) return null;

  return (
    <section className="usage">
      <div className="uhead">
        <b>שימוש בקלוד</b>
        <span className="num" style={{ color: "var(--faint)" }}>החשבון שלך, לא נתוני הערוץ</span>
      </div>

      {u.reason && <p className="hint">{u.reason}</p>}

      {!u.reason && (
        <div className="ucols">
          <div className="ucol">
            <div className="ulabel">שבועי (מתעדכן לבד)</div>
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
      )}
    </section>
  );
}
