"use client";

import { useEffect, useRef, useState } from "react";

/** A talking-head clip from a portrait + narration audio, via D-ID's Talks API. Chosen
 *  over Higgsfield (studio/lib/higgsfield.ts, the same submit/poll shape) because D-ID
 *  needs no paid credit balance and accepts up to 5 minutes of audio per talk, against
 *  Higgsfield's 15-second cap. Unlike the Higgsfield page, D-ID's request/response shape
 *  here is confirmed from D-ID's own docs (docs.d-id.com/reference/createtalk), not a
 *  best-effort guess — result_url is the documented field name, not a fallback chain. */
export default function DIdPage() {
  const [sourceUrl, setSourceUrl] = useState("");
  const [audioUrl, setAudioUrl] = useState("");

  const [talkId, setTalkId] = useState<string | null>(null);
  const [phase, setPhase] = useState<"idle" | "submitting" | "running" | "done" | "failed">("idle");
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [raw, setRaw] = useState<unknown>(null);
  const [err, setErr] = useState<string | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => () => { if (pollRef.current) clearInterval(pollRef.current); }, []);

  async function submit() {
    if (!sourceUrl.trim() || !audioUrl.trim()) {
      setErr("צריך תמונה ואודיו — שניהם, כתובות ציבוריות שה-API יכול לפתוח בעצמו");
      return;
    }
    setErr(null);
    setVideoUrl(null);
    setRaw(null);
    setPhase("submitting");
    try {
      const r = await fetch("/api/d-id/submit", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ sourceUrl, audioUrl }),
      });
      const j = await r.json();
      if (!j.ok) {
        setErr(j.error ?? `השרת החזיר ${r.status}`);
        setPhase("failed");
        return;
      }
      setTalkId(j.talkId);
      setPhase("running");
      // Polls every 5s, same interval the Higgsfield page uses — a talking-head render
      // is a several-minute job, not a fit for tighter polling.
      pollRef.current = setInterval(() => poll(j.talkId), 5000);
    } catch (e) {
      setErr((e as Error).message);
      setPhase("failed");
    }
  }

  async function poll(id: string) {
    try {
      const r = await fetch(`/api/d-id/status?id=${encodeURIComponent(id)}`);
      const j = await r.json();
      if (!j.ok) {
        setErr(j.error ?? `השרת החזיר ${r.status}`);
        setPhase("failed");
        if (pollRef.current) clearInterval(pollRef.current);
        return;
      }
      if (j.phase === "done") {
        setPhase("done");
        setVideoUrl(j.videoUrl ?? null);
        setRaw(j.raw ?? null);
        if (pollRef.current) clearInterval(pollRef.current);
      } else if (j.phase === "failed") {
        setPhase("failed");
        setErr("העבודה נכשלה בצד של D-ID");
        setRaw(j.raw ?? null);
        if (pollRef.current) clearInterval(pollRef.current);
      }
      // "running" — keep polling, nothing to update yet.
    } catch (e) {
      setErr((e as Error).message);
      setPhase("failed");
      if (pollRef.current) clearInterval(pollRef.current);
    }
  }

  return (
    <>
      <p className="eyebrow">D-ID</p>
      <h1>
        ראש מדבר, מ<em>תמונה + אודיו</em>
      </h1>
      <p className="sub">
        עוטף את ה-Talks API של D-ID — קליפ ראש מדבר מתמונת פורטרט ואודיו נרטיב, בלי
        לגעת באפליקציית הצרכן שלהם. תמונה ואודיו חייבים להיות בכתובות ציבוריות שה-API
        יכול לפתוח בעצמו — לא קבצים מקומיים. עד 5 דקות אודיו לקריאה אחת (לעומת 15 שניות
        אצל Higgsfield).
      </p>

      <form
        className="ask"
        style={{ flexDirection: "column", alignItems: "stretch", gap: 12 }}
        onSubmit={(e) => { e.preventDefault(); submit(); }}
      >
        <input
          value={sourceUrl}
          onChange={(e) => setSourceUrl(e.target.value)}
          placeholder="כתובת תמונת הפורטרט (URL ציבורי, jpg/png)"
        />
        <input
          value={audioUrl}
          onChange={(e) => setAudioUrl(e.target.value)}
          placeholder="כתובת קובץ האודיו (URL ציבורי, wav/mp3)"
        />
        <button className="btn" type="submit" disabled={phase === "submitting" || phase === "running"}>
          {phase === "submitting" || phase === "running" ? <span className="spin" /> : "שלח עבודה"}
        </button>
      </form>

      {phase === "running" && (
        <div className="note">
          <div className="t">רץ</div>
          talk {talkId} — בודק כל 5 שניות. עבודה כזאת יכולה לקחת כמה דקות.
        </div>
      )}

      {err && (
        <div className="note warn">
          <div className="t">לא עבד</div>
          {err}
        </div>
      )}

      {phase === "done" && (
        <div className="answer">
          {videoUrl ? (
            <>
              <b>נמצא URL של הווידאו:</b>
              <div>
                <a href={videoUrl} target="_blank" rel="noreferrer">{videoUrl}</a>
              </div>
            </>
          ) : (
            <>
              <b>העבודה הסתיימה, אבל אין result_url בתשובה.</b>
              <div>התשובה הגולמית מוצגת למטה.</div>
            </>
          )}
        </div>
      )}

      {raw != null && (
        <pre className="body" style={{ whiteSpace: "pre-wrap", wordBreak: "break-all" }}>
          {JSON.stringify(raw, null, 2)}
        </pre>
      )}
    </>
  );
}
