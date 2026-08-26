"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { Skill } from "@/lib/skills";

export default function SkillsBrowser({ skills }: { skills: Skill[] }) {
  const [q, setQ] = useState("");
  const hits = useMemo(() => {
    const t = q.trim().toLowerCase();
    if (!t) return skills;
    return skills.filter((s) => (s.title + " " + s.blurb).toLowerCase().includes(t));
  }, [q, skills]);

  return (
    <div className="ebrowse">
      {skills.length > 4 && (
        <input
          className="esearch"
          type="search"
          placeholder="Search skills…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          aria-label="Search skills"
        />
      )}
      {hits.length === 0 ? (
        <p className="empty">No skill matches that yet.</p>
      ) : (
        <ul className="prompts">
          {hits.map((s) => (
            <li key={s.slug}>
              <Link href={`/s/${s.slug}`}>
                <b>{s.title}</b>
                <span>{s.blurb}</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
