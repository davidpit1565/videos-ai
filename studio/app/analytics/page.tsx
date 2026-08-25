"use client";

import { useMemo, useState } from "react";
import { useStudio } from "../providers";
import { n } from "@/lib/fmt";
import { Episode, Snapshot } from "@/lib/types";
import CountUp from "../count-up";

/** Real progress, from data the studio already tracks — no number here is invented.
 *  Followers come from the daily snapshot Vercel's cron writes (api/track); views/likes/
 *  saves/comments/shares per episode come from the last Instagram sync. A metric with no
 *  data yet shows an empty state that says so, not a zero. */

const W = 720;
const H = 220;
const PAD = { top: 16, right: 16, bottom: 26, left: 44 };

function niceMax(v: number): number {
  if (v <= 0) return 1;
  const mag = Math.pow(10, Math.floor(Math.log10(v)));
  const norm = v / mag;
  const step = norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 5 ? 5 : 10;
  return step * mag;
}

function FollowersLine({ snaps }: { snaps: Snapshot[] }) {
  const pts = snaps
    .map((s) => ({ date: s.date, v: s.igFollowers }))
    .filter((p): p is { date: string; v: number } => p.v != null);

  const [hover, setHover] = useState<number | null>(null);

  if (pts.length < 2) {
    return (
      <div className="chart-empty">
        עדיין אין מספיק נקודות מדידה להראות מגמה — צריך לפחות שני ימים עם עוקבים נמדדים.
        המספר הנוכחי: {pts.length === 1 ? n(pts[0].v) : "—"}.
      </div>
    );
  }

  const innerW = W - PAD.left - PAD.right;
  const innerH = H - PAD.top - PAD.bottom;
  const vMin = Math.min(...pts.map((p) => p.v));
  const vMax = Math.max(...pts.map((p) => p.v));
  const lo = Math.max(0, vMin - Math.max(1, Math.round((vMax - vMin) * 0.15 || vMax * 0.1)));
  const hi = vMax + Math.max(1, Math.round((vMax - vMin) * 0.15 || vMax * 0.1));
  const x = (i: number) => PAD.left + (pts.length === 1 ? innerW / 2 : (i / (pts.length - 1)) * innerW);
  const y = (v: number) => PAD.top + innerH - ((v - lo) / (hi - lo || 1)) * innerH;

  const path = pts.map((p, i) => `${i === 0 ? "M" : "L"}${x(i).toFixed(1)},${y(p.v).toFixed(1)}`).join(" ");
  const ticks = [lo, (lo + hi) / 2, hi];

  const first = pts[0];
  const last = pts[pts.length - 1];
  const delta = last.v - first.v;

  return (
    <div className="chart-wrap">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className="chart"
        role="img"
        aria-label={`עוקבים באינסטגרם לאורך זמן, מ-${n(first.v)} ל-${n(last.v)}`}
        onMouseLeave={() => setHover(null)}
      >
        {ticks.map((t, i) => (
          <g key={i}>
            <line x1={PAD.left} x2={W - PAD.right} y1={y(t)} y2={y(t)} className="grid" />
            <text x={PAD.left - 8} y={y(t)} className="axis" textAnchor="end" dominantBaseline="middle">
              {n(Math.round(t))}
            </text>
          </g>
        ))}
        <path d={path} className="line" fill="none" />
        <circle cx={x(pts.length - 1)} cy={y(last.v)} r="4" className="endpoint" />
        <text x={x(pts.length - 1) - 8} y={y(last.v) - 10} className="end-label" textAnchor="end">
          {n(last.v)}
        </text>
        {pts.map((p, i) => (
          <rect
            key={i}
            x={x(i) - innerW / pts.length / 2}
            y={PAD.top}
            width={innerW / pts.length || 8}
            height={innerH}
            fill="transparent"
            onMouseEnter={() => setHover(i)}
            onFocus={() => setHover(i)}
            tabIndex={0}
          />
        ))}
        {hover != null && (
          <line x1={x(hover)} x2={x(hover)} y1={PAD.top} y2={H - PAD.bottom} className="crosshair" />
        )}
      </svg>
      {hover != null && (
        <div
          className="tooltip"
          style={{ insetInlineStart: `${(x(hover) / W) * 100}%`, top: `${(y(pts[hover].v) / H) * 100}%` }}
        >
          <b>{n(pts[hover].v)}</b>
          <span>{pts[hover].date}</span>
        </div>
      )}
      <p className="chart-note">
        {n(first.v)} → {n(last.v)} עוקבים ({delta >= 0 ? "+" : ""}
        {n(delta)}) מ-{first.date} עד {last.date}
      </p>
    </div>
  );
}

function ViewsBars({ episodes }: { episodes: Episode[] }) {
  const live = episodes
    .filter((e) => e.status === "live" && e.views != null)
    .sort((a, b) => a.number - b.number);

  const [hover, setHover] = useState<number | null>(null);

  if (live.length === 0) {
    return (
      <div className="chart-empty">
        עדיין אין פרק עם צפיות מדודות. אחרי שפרק ראשון מפורסם ומקושר באינסטגרם
        (ב-/videos), הצפיות שלו יופיעו כאן.
      </div>
    );
  }

  const innerW = W - PAD.left - PAD.right;
  const innerH = H - PAD.top - PAD.bottom;
  const maxV = niceMax(Math.max(...live.map((e) => e.views ?? 0)));
  const bandW = innerW / live.length;
  const barW = Math.min(24, bandW * 0.55);
  const y = (v: number) => PAD.top + innerH - (v / maxV) * innerH;
  const ticks = [0, maxV / 2, maxV];

  return (
    <div className="chart-wrap">
      <svg viewBox={`0 0 ${W} ${H}`} className="chart" role="img" aria-label="צפיות לפי פרק">
        {ticks.map((t, i) => (
          <g key={i}>
            <line x1={PAD.left} x2={W - PAD.right} y1={y(t)} y2={y(t)} className="grid" />
            <text x={PAD.left - 8} y={y(t)} className="axis" textAnchor="end" dominantBaseline="middle">
              {n(Math.round(t))}
            </text>
          </g>
        ))}
        {live.map((e, i) => {
          const cx = PAD.left + bandW * i + bandW / 2;
          const v = e.views ?? 0;
          const top = y(v);
          const isHover = hover === i;
          return (
            <g key={e.id}>
              <rect
                x={cx - barW / 2}
                y={top}
                width={barW}
                height={PAD.top + innerH - top}
                rx="4"
                className={isHover ? "bar bar-hover" : "bar"}
                onMouseEnter={() => setHover(i)}
                onMouseLeave={() => setHover(null)}
                onFocus={() => setHover(i)}
                tabIndex={0}
              />
              <text x={cx} y={H - PAD.bottom + 16} className="axis" textAnchor="middle">
                {e.number}
              </text>
              {isHover && (
                <text x={cx} y={top - 8} className="end-label" textAnchor="middle">
                  {n(v)}
                </text>
              )}
            </g>
          );
        })}
      </svg>
    </div>
  );
}

export default function Analytics() {
  const { state } = useStudio();

  const rows = useMemo(() => {
    if (!state) return [];
    return [...state.episodes]
      .filter((e) => e.status === "live")
      .sort((a, b) => a.number - b.number);
  }, [state]);

  if (!state) return <p className="sub">טוען…</p>;

  const last = state.snapshots.at(-1) ?? null;
  const totalViews = rows.reduce((a, e) => a + (e.views ?? 0), 0);
  const totalLikes = rows.reduce((a, e) => a + (e.likes ?? 0), 0);
  const totalSaves = rows.reduce((a, e) => a + (e.saves ?? 0), 0);
  const totalShares = rows.reduce((a, e) => a + (e.shares ?? 0), 0);
  // Entered by hand in /videos (no API attributes a subscriber to the post that brought
  // them) — 0 here means "not yet counted," not "brought none," so it stays out of the
  // sum until at least one episode has a real number, same rule ViewsBars already
  // follows for views.
  const attributedRows = rows.filter((e) => e.subsAttributed != null);
  const totalAttributed = attributedRows.reduce((a, e) => a + (e.subsAttributed ?? 0), 0);

  return (
    <main>
      <p className="eyebrow">מדדים אמיתיים בלבד</p>
      <h1>ההתקדמות שלך</h1>
      <p className="sub">
        כל מספר כאן נמדד — עוקבים מהתמונה היומית שהצינור שומר, צפיות/לייקים/שמירות/שיתופים
        מהסנכרון האחרון מול אינסטגרם. פרק בלי נתונים מדודים לא מוצג בטבלה, ולא מומצא לו מספר.
      </p>

      <div className="tiles">
        <div className="tile">
          <div className="k">עוקבים כרגע</div>
          <div className="v"><CountUp value={last?.igFollowers ?? null} /></div>
          <div className="s">מתוך התמונה האחרונה, {last?.date ?? "—"}</div>
        </div>
        <div className="tile">
          <div className="k">סה״כ צפיות</div>
          <div className="v"><CountUp value={totalViews || null} /></div>
          <div className="s">סכום הפרקים שפורסמו ונמדדו</div>
        </div>
        <div className="tile">
          <div className="k">סה״כ לייקים</div>
          <div className="v"><CountUp value={totalLikes || null} /></div>
        </div>
        <div className="tile">
          <div className="k">סה״כ שמירות + שיתופים</div>
          <div className="v"><CountUp value={(totalSaves + totalShares) || null} /></div>
        </div>
        <div className="tile">
          <div className="k">נרשמים שיוחסו לפרקים</div>
          <div className="v"><CountUp value={attributedRows.length ? totalAttributed : null} /></div>
          <div className="s">
            {attributedRows.length
              ? `מ-${attributedRows.length} פרק${attributedRows.length > 1 ? "ים" : ""} שסומנו ב-/videos`
              : "עדיין לא סומן אף פרק — נכנס ידנית ב-/videos"}
          </div>
        </div>
      </div>

      <section className="chart-section">
        <h2>עוקבים באינסטגרם לאורך זמן</h2>
        <FollowersLine snaps={state.snapshots} />
      </section>

      <section className="chart-section">
        <h2>צפיות לפי פרק</h2>
        <ViewsBars episodes={state.episodes} />
      </section>

      <section className="chart-section">
        <h2>הטבלה המלאה</h2>
        <div className="tw boxed">
          <table>
            <thead>
              <tr>
                <th>פרק</th>
                <th>כותרת</th>
                <th>צפיות</th>
                <th>לייקים</th>
                <th>שמירות</th>
                <th>תגובות</th>
                <th>שיתופים</th>
                <th title="נכנס ידנית ב-/videos — אין API שמייחס נרשם לפוסט שהביא אותו">נרשמים</th>
              </tr>
            </thead>
            <tbody>
              {rows.length === 0 && (
                <tr>
                  <td colSpan={8} className="empty-cell">
                    אין עדיין פרק שפורסם ונמדד.
                  </td>
                </tr>
              )}
              {rows.map((e) => (
                <tr key={e.id}>
                  <td className="num">{e.number}</td>
                  <td className="ttl" title={e.title}>{e.title}</td>
                  <td className="num">{n(e.views)}</td>
                  <td className="num">{n(e.likes)}</td>
                  <td className="num">{n(e.saves)}</td>
                  <td className="num">{n(e.comments)}</td>
                  <td className="num">{n(e.shares)}</td>
                  <td className="num">{n(e.subsAttributed)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
