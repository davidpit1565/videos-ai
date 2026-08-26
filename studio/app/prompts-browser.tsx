"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { Prompt } from "@/lib/prompts";

export default function PromptsBrowser({ prompts }: { prompts: Prompt[] }) {
  const [q, setQ] = useState("");
  const hits = useMemo(() => {
    const t = q.trim().toLowerCase();
    if (!t) return prompts;
    return prompts.filter((p) =>
      (p.title + " " + p.blurb + " " + p.body).toLowerCase().includes(t)
    );
  }, [q, prompts]);

  return (
    <div className="ebrowse">
      {prompts.length > 4 && (
        <input
          className="esearch"
          type="search"
          placeholder="Search prompts…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          aria-label="Search prompts"
        />
      )}
      {hits.length === 0 ? (
        <p className="empty">No prompt matches that yet.</p>
      ) : (
        <ul className="prompts">
          {hits.map((p) => (
            <li key={p.slug}>
              <Link href={`/p/${p.slug}`}>
                <b>{p.title}</b>
                <span>{p.blurb}</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
