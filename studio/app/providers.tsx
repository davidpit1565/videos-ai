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
  /** which environment variable the database was found under, for diagnosis */
  dbVar: string | null;
  /** what the server said when there is no database, or when connecting failed */
  hint: string | null;
  /** Mutate a copy of the state; the copy is what gets saved. */
  update: (fn: (s: State) => void) => void;
  /** Pull Instagram and Beehiiv now and take whatever changed. */
  refresh: () => Promise<{ ok: boolean; reason?: string; newEvents?: number }>;
  refreshing: boolean;
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
  const [dbVar, setDbVar] = useState<string | null>(null);
  const [hint, setHint] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const ref = useRef<State | null>(null);
  const modeRef = useRef<Mode>("loading");
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
/** A stored state outlives the shape it was written in. Twenty places in the studio
 *  do `state.episodes.map(...)` and `state.ideas.map(...)` directly, so a row saved
 *  before one of those arrays existed took the whole page down with "Application
 *  error: a client-side exception has occurred" — the server was fine, the browser
 *  crashed on a missing array. Guarding here means the pages can keep reading plainly. */
function whole(s: State): State {
  return {
    ...s,
    episodes: s.episodes ?? [],
    ideas: s.ideas ?? [],
    snapshots: s.snapshots ?? [],
    activity: s.activity ?? [],
  };
}

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
        const j = (await r.json()) as {
          mode: Mode; state: State | null; dbVar?: string | null; hint?: string; error?: string;
        };
        if (!live) return;
        setDbVar(j.dbVar ?? null);
        setHint(j.error ? `${j.hint ?? ""} ${j.error}`.trim() : j.hint ?? null);
        if (j.mode === "cloud") {
          modeRef.current = "cloud";
          setMode("cloud");
          setState(whole(j.state ?? local ?? seed()));
          return;
        }
      } catch {
        /* fall through to local */
      }
      if (!live) return;
      modeRef.current = "local";
      setMode("local");
      setState(whole(local ?? seed()));
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

  const refresh = useCallback(async () => {
    setRefreshing(true);
    try {
      const r = await fetch("/api/track", { cache: "no-store" });
      const j = (await r.json()) as { ok: boolean; reason?: string; newEvents?: number };
      if (j.ok) {
        // the tracker writes to the database, so take the saved copy back rather than
        // guessing locally what it changed
        const s = await fetch("/api/state", { cache: "no-store" }).then((x) => x.json());
        if (s.mode === "cloud" && s.state) {
          ref.current = s.state as State;
          setState(s.state as State);
        }
      }
      return j;
    } catch (e) {
      return { ok: false, reason: (e as Error).message };
    } finally {
      setRefreshing(false);
    }
  }, []);

  return (
    <C.Provider value={{ state, mode, saving, dbVar, hint, update, refresh, refreshing }}>
      {children}
    </C.Provider>
  );
}
