"use client";

import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { State } from "@/lib/types";
import { whole } from "@/lib/whole";
import { seed } from "@/lib/seed";

const KEY = "aw-studio-v1";

export type Mode = "loading" | "cloud" | "local";

type Ctx = {
  state: State | null;
  mode: Mode;
  saving: boolean;
  /** Set when the last save to the database failed after a retry — the edit is still
   *  only in this browser's copy. Cleared by the next successful save. */
  saveError: string | null;
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
  const [saveError, setSaveError] = useState<string | null>(null);
  const [dbVar, setDbVar] = useState<string | null>(null);
  const [hint, setHint] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
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
        if (r.status === 401) {
          // Locked out, not offline. Falling through to the browser copy silently is
          // what made a stale studio look like a working one — say it instead.
          if (!live) return;
          modeRef.current = "local";
          setMode("local");
          setHint("הקוד פג. הנתונים כאן מהדפדפן ולא מהמסד — צריך להזין קוד מחדש.");
          setState(whole(local ?? seed()));
          return;
        }
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

  // The PUT below used to fire and forget: any failure — a dropped connection, the
  // database briefly unreachable, a 500 — was swallowed by `.catch(() => undefined)`
  // with nothing shown anywhere. The optimistic update() already changed what's on
  // screen, so the click looked like it worked; the database just never got it. The
  // next periodic refresh() (every 3 minutes) or the next page load pulls the
  // database's real, unchanged copy and silently reverts the edit — which is exactly
  // what "I clicked it and nothing happened" looks like from someone who checked back
  // a minute later, even though something DID happen, it just didn't stick. One retry
  // covers a genuine one-off network blip; a real, persistent failure now sets
  // saveError so the badge in shell.tsx can say so instead of quietly lying "מסד
  // נתונים" (saved) once `saving` goes back to false regardless of outcome.
  const putState = useCallback(async (next: State): Promise<boolean> => {
    try {
      const r = await fetch("/api/state", {
        method: "PUT",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(next),
      });
      const j = (await r.json().catch(() => null)) as { ok?: boolean; error?: string } | null;
      return r.ok && j?.ok === true;
    } catch {
      return false;
    }
  }, []);

  const persist = useCallback(
    (next: State) => {
      try {
        localStorage.setItem(KEY, JSON.stringify(next));
      } catch {
        /* private mode or a full quota — the in-memory copy still works */
      }
      if (modeRef.current !== "cloud") return;
      if (timer.current) clearTimeout(timer.current);
      setSaving(true);
      timer.current = setTimeout(async () => {
        let ok = await putState(next);
        if (!ok) ok = await putState(next); // one retry — covers a one-off network blip
        setSaving(false);
        setSaveError(ok ? null : "השמירה למסד הנתונים נכשלה — השינוי האחרון עלול לא להישמר. נסה שוב.");
      }, 700);
    },
    [putState],
  );

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
          // through whole() like every other entry point. This one was missed, and it
          // is the reachable one: /api/track returns early without saving when a pull
          // ran in the last 20 minutes, so the full path repairs the row as a side
          // effect and hides the bug, while the skipped path hands back the raw row.
          const fixed = whole(s.state as State);
          ref.current = fixed;
          setState(fixed);
        }
      }
      return j;
    } catch (e) {
      return { ok: false, reason: (e as Error).message };
    } finally {
      setRefreshing(false);
    }
  }, []);

  /** Pull the numbers when the studio is opened, not only when a button is pressed — and
   *  keep pulling while it stays open, not just once.
   *
   *  He asked for it to update by itself, and the first version of this only half did: the
   *  guard below fired once per app session (a ref, not reset by client-side navigation
   *  between tabs — Next.js keeps the same Provider mounted the whole time he's in the
   *  studio), so anyone who opened it and just tapped between pages, the normal way to use
   *  it, got exactly one pull, ever, no matter how many hours passed — indistinguishable
   *  from a system that never updates on its own, which is exactly what he reported: numbers
   *  stuck until he manually pressed a button. /api/track already returns early without
   *  spending an API call when a pull ran in the last 3 minutes (shortened from 20 — see
   *  that file), so calling it on an interval costs nothing when there is nothing new to
   *  fetch — the server-side cooldown does the actual rate-limiting, this just stops
   *  requiring a human to remember to ask.
   *  Also re-pulls when the tab/app comes back into view, for the common case of switching
   *  away and back rather than leaving it open and idle. Cloud mode only: with no database
   *  the tracker has nowhere to write. */
  useEffect(() => {
    if (mode !== "cloud") return;
    void refresh();
    const interval = setInterval(() => void refresh(), 3 * 60 * 1000);
    const onVisible = () => {
      if (document.visibilityState === "visible") void refresh();
    };
    document.addEventListener("visibilitychange", onVisible);
    return () => {
      clearInterval(interval);
      document.removeEventListener("visibilitychange", onVisible);
    };
  }, [mode, refresh]);

  return (
    <C.Provider value={{ state, mode, saving, saveError, dbVar, hint, update, refresh, refreshing }}>
      {children}
    </C.Provider>
  );
}
