"use client";

import EpRows from "./ep-rows";
import { useRouter, useSearchParams } from "next/navigation";
import { useMemo, useState } from "react";
import { Entry } from "@/lib/site";
import { publicMonth } from "@/lib/fmt";
import { TOOLS, toolFor } from "@/lib/tools";

export default function EpisodesBrowser({ eps }: { eps: Entry[] }) {
  const router = useRouter();
  const params = useSearchParams();
  // Reads ?tool= on load so the homepage's own "browse by tool" row can link straight
  // into a pre-filtered list — a visitor arriving from there for "n8n" and landing on
  // an unfiltered wall of every episode is the exact bait-and-switch a named vertical
  // is supposed to avoid.
  const [tool, setToolState] = useState(() => params.get("tool") ?? "All");
  const setTool = (t: string) => {
    setToolState(t);
    router.replace(t === "All" ? "/episodes" : `/episodes?tool=${encodeURIComponent(t)}`, { scroll: false });
  };
  const [q, setQ] = useState("");

  const tagged = useMemo(() => eps.map((e) => ({ ...e, tool: toolFor(e.title, e.blurb) })), [eps]);
  const tools = useMemo(() => {
    // toolFor() falls back to "General" for anything not in TOOLS, so a pill list built
    // only from TOOLS silently dropped every "General" episode's own filter — it still
    // got the tag on its card, just no way to filter by it. Any tag actually in use gets
    // a pill now, known tools in their fixed order first, then whatever else shows up.
    const present = new Set(tagged.map((e) => e.tool));
    const known = TOOLS.filter((t) => present.has(t));
    const extra = [...present].filter((t) => !TOOLS.includes(t)).sort();
    return ["All", ...known, ...extra];
  }, [tagged]);
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
      {tool === "General" && (
        <p className="efilter-note">
          Not tied to one tool: broader AI behavior, or the production process itself.
        </p>
      )}
      <input
        className="esearch"
        type="search"
        placeholder="Search episodes"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        aria-label="Search episodes"
      />
      <p className="ecount" aria-live="polite">
        {filtered.length === tagged.length
          ? `${tagged.length} episodes, newest first.`
          : `${filtered.length} of ${tagged.length} episodes.`}
      </p>
      {filtered.length === 0 ? (
        <p className="empty">No episode matches that yet.</p>
      ) : (
        <EpRows
          items={filtered.map((e) => ({
            n: e.n,
            title: e.title,
            blurb: e.blurb,
            meta: [`Episode ${e.n}`, publicMonth(e.publishedAt), e.tool !== "General" ? e.tool : null]
              .filter(Boolean)
              .join(", "),
          }))}
        />
      )}
    </div>
  );
}
