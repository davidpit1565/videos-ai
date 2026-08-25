"use client";

import { useEffect, useState } from "react";

/** The visitor-facing sibling of app/notify.tsx (the studio's own device switch) — same
 *  mechanism, a different audience and a different endpoint (/api/subscribe-push, not
 *  /api/push/subscribe), so a reader's device can only ever hear about new episodes,
 *  never a studio-internal alert. See lib/push.ts on why the two must never share a send.
 *
 *  A quieter alternative to the email signup right next to it — no address, one tap,
 *  works for anyone who'd rather not hand over an inbox for a weekly reel. */
export default function SiteNotify() {
  const [state, setState] = useState<"checking" | "unsupported" | "off" | "on" | "blocked">(
    "checking",
  );
  const [busy, setBusy] = useState(false);
  const [note, setNote] = useState<string | null>(null);

  useEffect(() => {
    if (!("serviceWorker" in navigator) || !("PushManager" in window)) {
      setState("unsupported");
      return;
    }
    if (Notification.permission === "denied") {
      setState("blocked");
      return;
    }
    (async () => {
      try {
        const reg = await navigator.serviceWorker.register("/sw.js");
        const sub = await reg.pushManager.getSubscription();
        setState(sub ? "on" : "off");
      } catch {
        setState("off");
      }
    })();
  }, []);

  async function enable() {
    setBusy(true);
    setNote(null);
    try {
      const perm = await Notification.requestPermission();
      if (perm !== "granted") {
        setState(perm === "denied" ? "blocked" : "off");
        return;
      }
      const info = await fetch("/api/subscribe-push").then((x) => x.json());
      if (!info.ok) throw new Error(info.error || "no key");
      const reg = await navigator.serviceWorker.register("/sw.js");
      await navigator.serviceWorker.ready;
      const sub = await reg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: info.key,
      });
      const r = await fetch("/api/subscribe-push", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ sub: sub.toJSON(), label: "visitor" }),
      }).then((x) => x.json());
      if (!r.ok) throw new Error(r.error || "could not save it");
      setState("on");
    } catch (e) {
      setNote(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  // Unsupported/blocked cases are silent here rather than an explanatory paragraph like
  // the studio's own switch has — this sits beside an email form that already works for
  // everyone, so a browser limitation is not worth a reader's attention on a public page.
  if (state === "checking" || state === "unsupported" || state === "blocked") return null;

  if (state === "on") {
    return <p className="pushnote">You&apos;ll get a notification when a new episode goes up.</p>;
  }

  return (
    <p className="pushnote">
      Prefer no inbox?{" "}
      <button type="button" className="linklike" onClick={enable} disabled={busy}>
        {busy ? "…" : "Get a notification instead"}
      </button>
      {note ? ` — ${note}` : ""}
    </p>
  );
}
