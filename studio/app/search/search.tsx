"use client";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
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
  const router = useRouter();
  const params = useSearchParams();
  // Deep-linkable: a search someone actually did is now a URL worth sharing, and the
  // browser's own back button steps through it — neither worked when the query lived
  // only in useState. replace (not push) so typing a letter at a time doesn't fill the
  // back-button history with one entry per keystroke; scroll:false keeps the page from
  // jumping to the top on every character.
  const [q, setQ] = useState(() => params.get("q") ?? "");
  const setSearch = (v: string) => {
    setQ(v);
    router.replace(v ? `/search?q=${encodeURIComponent(v)}` : "/search", { scroll: false });
  };
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
        onChange={(e) => setSearch(e.target.value)}
        autoFocus
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
