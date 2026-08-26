"use client";

import { useState } from "react";
import { useStudio } from "../../providers";
import {
  CHANNELS, CHANNEL_HE, Channel, DAY_HE, Episode, STATUS_HE, weekDays,
} from "@/lib/types";
import { n, pct } from "@/lib/fmt";
import { saveRate } from "@/lib/types";

export default function Week() {
  const { state, update } = useStudio();
  const [offset, setOffset] = useState(0);

  if (!state) return <p className="sub">טוען…</p>;

  const base = new Date();
  base.setDate(base.getDate() + offset * 7);
  const days = weekDays(base);
  const label = `${days[0].slice(5)} – ${days[5].slice(5)}`;

  // Once an episode is actually live, the day it went out is a fact (publishedAt, set
  // from Instagram/YouTube's own timestamp) — not something to keep typing in by hand.
  // publishOn stays for planning episodes that haven't shipped yet; a live episode's
  // real date always wins once it exists, which is why reel 3 not being here after he
  // published it was the bug: the calendar only ever looked at the manual field.
  const dateFor = (e: Episode) => e.publishedAt ?? e.publishOn ?? null;
  const forDay = (d: string) => state.episodes.filter((e) => dateFor(e) === d);
  const unplanned = state.episodes.filter((e) => !dateFor(e));

  /** One a day, Sunday to Friday, in episode order — the schedule he asked for. */
  function fill() {
    update((s) => {
      const free = days.filter((d) => !s.episodes.some((e) => dateFor(e) === d));
      const ready = s.episodes
        .filter((e) => !dateFor(e))
        .sort((a, b) => a.number - b.number);
      for (const d of free) {
        const e = ready.shift();
        if (!e) break;
        e.publishOn = d;
        if (!e.channels?.length) e.channels = ["ig", "tiktok", "yt"];
      }
    });
  }

  const toggle = (id: string, c: Channel) =>
    update((s) => {
      const e = s.episodes.find((x) => x.id === id);
      if (!e) return;
      const cur = new Set(e.channels ?? []);
      cur.has(c) ? cur.delete(c) : cur.add(c);
      e.channels = [...cur];
    });

  return (
    <>
      <p className="eyebrow">השבוע</p>
      <h1>
        מה יוצא <em>מתי</em>
      </h1>
      <p className="sub">
        סרטון אחד ביום, ראשון עד שישי. שבת לא מופיעה כאן בכלל — <b>אין יום שביעי לתכנן</b>.
        גרירה לא נדרשת: בוחרים תאריך בכרטיס של הפרק, או לוחצים על מילוי אוטומטי.
      </p>

      <div className="actions" style={{ marginBottom: 6 }}>
        <button className="btn ghost" onClick={() => setOffset(offset - 1)}>← שבוע קודם</button>
        <span style={{ alignSelf: "center", fontWeight: 700 }} className="num">{label}</span>
        <button className="btn ghost" onClick={() => setOffset(offset + 1)}>שבוע הבא →</button>
        <button className="btn" onClick={fill} disabled={!unplanned.length}>
          מילוי אוטומטי
        </button>
      </div>

      <div className="week">
        {days.map((d, i) => {
          const eps = forDay(d);
          return (
            <div className={"day" + (eps.length ? " has" : "")} key={d}>
              <div className="dh">
                <b>{DAY_HE[i]}</b>
                <span className="num">{d.slice(5)}</span>
              </div>
              {eps.length === 0 ? (
                <div className="empty">—</div>
              ) : (
                eps.map((e) => <Card key={e.id} e={e} onToggle={toggle} />)
              )}
            </div>
          );
        })}
      </div>

      <h2>ממתינים לתאריך · {unplanned.length}</h2>
      {unplanned.length === 0 ? (
        <p className="sub">כל הפרקים שלא באוויר משובצים.</p>
      ) : (
        <ul className="list">
          {unplanned.map((e) => (
            <li key={e.id}>
              <span />
              <span className="lbl">
                {e.number}. {e.title}
                <small>{STATUS_HE[e.status]} · {e.topic || "בלי נושא"}</small>
              </span>
              <input
                className="cell num"
                type="date"
                style={{ maxWidth: 150 }}
                value={e.publishOn ?? ""}
                onChange={(ev) =>
                  update((s) => {
                    const t = s.episodes.find((x) => x.id === e.id);
                    if (t) t.publishOn = ev.target.value || null;
                  })
                }
              />
            </li>
          ))}
        </ul>
      )}
    </>
  );
}

function Card({ e, onToggle }: { e: Episode; onToggle: (id: string, c: Channel) => void }) {
  return (
    <div className="wcard">
      <div className="t">
        <span className="num">{e.number}</span> {e.title}
      </div>
      <div className="chs">
        {CHANNELS.map((c) => (
          <button
            key={c}
            className={"ch" + ((e.channels ?? []).includes(c) ? " on" : "")}
            onClick={() => onToggle(e.id, c)}
          >
            {CHANNEL_HE[c]}
          </button>
        ))}
      </div>
      {e.views != null && (
        <div className="mini num">
          {n(e.views)} צפיות · {pct(saveRate(e))} שמירות
        </div>
      )}
    </div>
  );
}
