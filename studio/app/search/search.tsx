"use client";
import Link from "next/link";
import { useMemo, useState } from "react";

type Row = {
  kind: "episode" | "prompt";
  href: string;
  title: string;
  blurb: string;
  views: number | null;
  yt: string | null;
  ig: string | null;
  text: string;
};

export default function Search({ index }: { index: Row[] }) {
  const [q, setQ] = useState("");
  const hits = useMemo(() => {
    const t = q.trim().toLowerCase();
    if (!t) return index;
    // every word must appear somewhere, in any order — closer to how people type than
    // one substring match
    const words = t.split(/\s+/);
    return index.filter((r) => words.every((w) => r.text.includes(w)));
  }, [q, index]);

  return (
    <>
      <input
        className="find"
        type="search"
        placeholder="chatgpt, custom instructions, agents…"
        aria-label="Search"
        value={q}
        onChange={(e) => setQ(e.target.value)}
      />
      <p className="count">
        {hits.length} of {index.length}
        {q.trim() ? ` for “${q.trim()}”` : ""}
      </p>
      {hits.length === 0 ? (
        <p className="empty">
          Nothing matches that yet. The library is small — it grows one episode a week.
        </p>
      ) : (
        <ul className="hits">
          {hits.map((r) => (
            <li key={r.href}>
              <Link href={r.href}>
                <span className="kind">{r.kind}</span>
                <b>{r.title}</b>
                <span className="bl">{r.blurb}</span>
              </Link>
              {r.yt || r.ig ? (
                <p className="ext">
                  {r.ig ? (
                    <a href={r.ig} target="_blank" rel="noopener noreferrer">Instagram</a>
                  ) : null}
                  {r.yt ? (
                    <a href={r.yt} target="_blank" rel="noopener noreferrer">YouTube</a>
                  ) : null}
                </p>
              ) : null}
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
