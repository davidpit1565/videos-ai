"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { Entry } from "@/lib/site";

/** Which real tool an episode is about, read straight out of its own title — never a
 *  separate category someone has to remember to set. Order matters: first match wins,
 *  so a title naming two tools still gets one clear tag instead of picking arbitrarily. */
const TOOLS = ["ChatGPT", "Claude", "n8n", "Instagram", "Whisper", "YouTube"];
function toolFor(title: string): string {
  const hit = TOOLS.find((t) => title.toLowerCase().includes(t.toLowerCase()));
  return hit ?? "General";
}

export default function EpisodesBrowser({ eps }: { eps: Entry[] }) {
  const [tool, setTool] = useState("All");
  const [q, setQ] = useState("");

  const tagged = useMemo(() => eps.map((e) => ({ ...e, tool: toolFor(e.title) })), [eps]);
  const tools = useMemo(
    () => ["All", ...TOOLS.filter((t) => tagged.some((e) => e.tool === t))],
    [tagged],
  );
  const filtered = tagged.filter((e) => {
    if (tool !== "All" && e.tool !== tool) return false;
    if (q && !(e.title + " " + e.blurb).toLowerCase().includes(q.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="ebrowse">
      {tools.length > 2 && (
        <div className="echips" role="group" aria-label="Filter by AI tool">
          {tools.map((t) => (
            <button
              key={t}
              className={t === tool ? "on" : ""}
              onClick={() => setTool(t)}
              aria-pressed={t === tool}
            >
              {t}
            </button>
          ))}
        </div>
      )}
      <input
        className="esearch"
        type="search"
        placeholder="Search episodes…"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        aria-label="Search episodes"
      />
      {filtered.length === 0 ? (
        <p className="empty">No episode matches that yet.</p>
      ) : (
        <ol className="eps">
          {filtered.map((e) => (
            <li key={e.n}>
              <Link href={`/e/${e.n}`}>
                <span className="n">{String(e.n).padStart(2, "0")}</span>
                <span className="tag">{e.tool}</span>
                <span className="t">{e.title}</span>
                <span className="tp">{e.blurb}</span>
              </Link>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
