"use client";

import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { State } from "@/lib/types";
import { seed } from "@/lib/seed";

const KEY = "aw-studio-v1";

export type Mode = "loading" | "cloud" | "local";

type Ctx = {
  state: State | null;
  mode: Mode;
  saving: boolean;
  /** Mutate a copy of the state; the copy is what gets saved. */
  update: (fn: (s: State) => void) => void;
};

const C = createContext<Ctx | null>(null);

export function useStudio(): Ctx {
  const v = useContext(C);
  if (!v) throw new Error("useStudio used outside the provider");
  return v;
}

export function Provider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<State | null>(null);
  const [mode, setMode] = useState<Mode>("loading");
  const [saving, setSaving] = useState(false);
  const ref = useRef<State | null>(null);
  const modeRef = useRef<Mode>("loading");
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  ref.current = state;

  // The browser copy is always written. The database copy is written too when
  // there is a database — so nothing is lost while DATABASE_URL is still missing.
  useEffect(() => {
    let live = true;
    (async () => {
      let local: State | null = null;
      try {
        const raw = localStorage.getItem(KEY);
        if (raw) {
          const p = JSON.parse(raw) as State;
          if (p && p.version === 1) local = p;
        }
      } catch {
        /* a corrupt copy is the same as no copy */
      }
      try {
        const r = await fetch("/api/state", { cache: "no-store" });
        const j = (await r.json()) as { mode: Mode; state: State | null };
        if (!live) return;
        if (j.mode === "cloud") {
          modeRef.current = "cloud";
          setMode("cloud");
          setState(j.state ?? local ?? seed());
          return;
        }
      } catch {
        /* fall through to local */
      }
      if (!live) return;
      modeRef.current = "local";
      setMode("local");
      setState(local ?? seed());
    })();
    return () => {
      live = false;
    };
  }, []);

  const persist = useCallback((next: State) => {
    try {
      localStorage.setItem(KEY, JSON.stringify(next));
    } catch {
      /* private mode or a full quota — the in-memory copy still works */
    }
    if (modeRef.current !== "cloud") return;
    if (timer.current) clearTimeout(timer.current);
    setSaving(true);
    timer.current = setTimeout(() => {
      fetch("/api/state", {
        method: "PUT",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(next),
      })
        .catch(() => undefined)
        .finally(() => setSaving(false));
    }, 700);
  }, []);

  const update = useCallback(
    (fn: (s: State) => void) => {
      const prev = ref.current;
      if (!prev) return;
      const next = structuredClone(prev);
      fn(next);
      next.updatedAt = new Date().toISOString();
      ref.current = next;
      setState(next);
      persist(next);
    },
    [persist],
  );

  return <C.Provider value={{ state, mode, saving, update }}>{children}</C.Provider>;
}
