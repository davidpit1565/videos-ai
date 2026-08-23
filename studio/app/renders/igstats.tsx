"use client";

import { useStudio } from "../providers";
import { n } from "@/lib/fmt";

/** Live Instagram performance for this reel, read straight from the same episode state
 *  the dashboard's "מה עבד" table already uses. He asked for this next to every video,
 *  not just on the main dashboard — the numbers already existed, they just were not
 *  shown here. Nothing new is fetched: this only reads state that /api/track already
 *  keeps current every morning. */
export default function IgStats({ episode }: { episode: number | null }) {
  const { state } = useStudio();
  if (episode === null || !state) return null;

  const ep = state.episodes.find((e) => e.number === episode);
  if (!ep) return null;

  if (!ep.igMediaId) {
    return (
      <div className="ig-stats ig-stats-empty">
        עוד לא מקושר לפוסט באינסטגרם — קישור נעשה ב<a href="/videos">/videos</a>, ואז המספרים
        כאן מתעדכנים לבד בכל בוקר.
      </div>
    );
  }

  const rows: [string, number | null][] = [
    ["צפיות", ep.views],
    ["לייקים", ep.likes],
    ["שמירות", ep.saves],
    ["תגובות", ep.comments],
    ["שיתופים", ep.shares],
  ];

  return (
    <div className="ig-stats">
      {rows.map(([label, val]) => (
        <div key={label} className="ig-stat">
          <span className="num">{n(val)}</span>
          <span className="lbl">{label}</span>
        </div>
      ))}
    </div>
  );
}
