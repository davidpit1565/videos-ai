"use client";

import { useEffect, useState } from "react";

/** Turning notifications on, per device.
 *
 *  Per device is not a detail: a browser permission belongs to the browser it was granted in,
 *  so the iMac and the phone each have to be switched on once. The control says which one it
 *  is looking at, and how many are registered in total, so "did I do the phone?" is a
 *  question the screen answers.
 *
 *  On iPhone this only works when the studio has been added to the home screen — Safari
 *  refuses push to a tab. That is stated here rather than left as a mystery, because a switch
 *  that does nothing and explains nothing is worse than no switch. */

function deviceLabel(): string {
  const ua = navigator.userAgent;
  const mac = /Macintosh/.test(ua);
  const iphone = /iPhone|iPad/.test(ua);
  const standalone =
    window.matchMedia("(display-mode: standalone)").matches ||
    (window.navigator as { standalone?: boolean }).standalone === true;
  const where = iphone ? "iPhone" : mac ? "Mac" : "מכשיר";
  return standalone ? `${where} (אפליקציה)` : `${where} (דפדפן)`;
}

export default function Notify() {
  const [state, setState] = useState<"checking" | "unsupported" | "off" | "on" | "blocked">(
    "checking",
  );
  const [devices, setDevices] = useState<number | null>(null);
  const [note, setNote] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [label, setLabel] = useState("");

  useEffect(() => {
    setLabel(deviceLabel());
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
        const r = await fetch("/api/push/subscribe").then((x) => x.json());
        if (typeof r.devices === "number") setDevices(r.devices);
        if (!r.ok && r.error) setNote(r.error);
      } catch (e) {
        setNote(e instanceof Error ? e.message : String(e));
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
      const info = await fetch("/api/push/subscribe").then((x) => x.json());
      if (!info.ok) throw new Error(info.error || "no key");
      const reg = await navigator.serviceWorker.register("/sw.js");
      await navigator.serviceWorker.ready;
      const sub = await reg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: info.key,
      });
      const r = await fetch("/api/push/subscribe", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ sub: sub.toJSON(), label: deviceLabel() }),
      }).then((x) => x.json());
      if (!r.ok) throw new Error(r.error || "could not save it");
      setDevices(r.devices ?? null);
      setState("on");
    } catch (e) {
      setNote(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  async function test() {
    setBusy(true);
    setNote(null);
    try {
      const r = await fetch("/api/push/test", { method: "POST" }).then((x) => x.json());
      setNote(
        r.sent > 0
          ? `נשלח ל-${r.sent} מכשירים${r.gone ? `, ${r.gone} כבר לא קיימים` : ""}`
          : "לא נשלח לאף מכשיר",
      );
    } catch (e) {
      setNote(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  if (state === "checking") return null;

  return (
    <section className="notify">
      <div className="nhead">
        <b>התראות</b>
        <span className="num">{label}</span>
        {devices !== null && <span className="num">{devices} מכשירים רשומים</span>}
      </div>

      {state === "unsupported" && (
        <p className="hint">
          הדפדפן הזה לא תומך בהתראות. באייפון זה עובד <b>רק</b> כשהסטודיו מותקן במסך הבית
          (שיתוף → הוספה למסך הבית) — בלשונית רגילה ספארי חוסם את זה.
        </p>
      )}

      {state === "blocked" && (
        <p className="hint">
          ההרשאה נדחתה במכשיר הזה, ואי אפשר לבקש אותה שוב מהדף. צריך להחזיר אותה בהגדרות
          האתר בדפדפן, ואז לרענן.
        </p>
      )}

      {state === "off" && (
        <>
          <p className="hint">
            כל רנדר חדש, כל נרשם, כל שינוי בסטודיו — הודעה למכשיר הזה. צריך להדליק פעם אחת
            בכל מכשיר בנפרד.
          </p>
          <button className="btn" onClick={enable} disabled={busy}>
            {busy ? "…" : "הדלק במכשיר הזה"}
          </button>
        </>
      )}

      {state === "on" && (
        <>
          <p className="hint">המכשיר הזה מקבל התראות.</p>
          <button className="btn small" onClick={test} disabled={busy}>
            {busy ? "…" : "שלח התראת בדיקה"}
          </button>
        </>
      )}

      {note && <p className="hint mono">{note}</p>}
    </section>
  );
}
