"use client";

import { useEffect, useRef, useState } from "react";

/** A talking-head ad clip from a portrait + narration audio, via Higgsfield's Speak v2.
 *  The API wrapper (lib/higgsfield.ts, ported from higgsfield/generate_talking_ad.py in
 *  PR #235) has never actually been run against a real completed job — its own README
 *  says so directly. This page is the first real place that can run it end to end, not
 *  a claim that it already works. If the video URL doesn't come back automatically,
 *  the raw response is shown so the real field can be found by hand and the extraction
 *  logic fixed from a real answer instead of a second guess. */
export default function HiggsfieldPage() {
  const [imageUrl, setImageUrl] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [prompt, setPrompt] = useState("handheld selfie-style UGC ad, warm lighting");
  const [duration, setDuration] = useState<5 | 10 | 15>(5);
  const [quality, setQuality] = useState<"high" | "mid">("high");

  const [jobSetId, setJobSetId] = useState<string | null>(null);
  const [phase, setPhase] = useState<"idle" | "submitting" | "running" | "done" | "failed">("idle");
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [raw, setRaw] = useState<unknown>(null);
  const [err, setErr] = useState<string | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => () => { if (pollRef.current) clearInterval(pollRef.current); }, []);

  async function submit() {
    if (!imageUrl.trim() || !audioUrl.trim() || !prompt.trim()) {
      setErr("צריך תמונה, אודיו ותיאור — שלושתם, כתובות ציבוריות שה-API יכול לפתוח בעצמו");
      return;
    }
    setErr(null);
    setVideoUrl(null);
    setRaw(null);
    setPhase("submitting");
    try {
      const r = await fetch("/api/higgsfield/submit", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ imageUrl, audioUrl, prompt, duration, quality }),
      });
      const j = await r.json();
      if (!j.ok) {
        setErr(j.error ?? `השרת החזיר ${r.status}`);
        setPhase("failed");
        return;
      }
      setJobSetId(j.jobSetId);
      setPhase("running");
      // Polls every 5s, same interval the original Python script used — a talking-head
      // render is a several-minute job, not a fit for tighter polling.
      pollRef.current = setInterval(() => poll(j.jobSetId), 5000);
    } catch (e) {
      setErr((e as Error).message);
      setPhase("failed");
    }
  }

  async function poll(id: string) {
    try {
      const r = await fetch(`/api/higgsfield/status?id=${encodeURIComponent(id)}`);
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
        setErr("העבודה נכשלה בצד של Higgsfield");
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
      <p className="eyebrow">Higgsfield</p>
      <h1>
        ראש מדבר, מ<em>תמונה + אודיו</em>
      </h1>
      <p className="sub">
        עוטף את Speak v2 של Higgsfield — קליפ ראש מדבר מתמונת פורטרט ואודיו נרטיב, בלי
        לגעת באפליקציית הצרכן שלהם. תמונה ואודיו חייבים להיות בכתובות ציבוריות שה-API יכול
        לפתוח בעצמו — לא קבצים מקומיים.
      </p>
      <div className="note warn">
        <div className="t">עדיין לא אומת על ריצה אמיתית</div>
        חילוץ ה-URL של הווידאו הגמור (למטה) הוא ניחוש מבוסס-מקורות, לא מאומת מול תשובה
        אמיתית מה-API. אם הוא לא עובד בריצה הראשונה — התשובה הגולמית תוצג כאן, ומזה אפשר
        לתקן את הקוד בפעם הבאה.
      </div>

      <form
        className="ask"
        style={{ flexDirection: "column", alignItems: "stretch", gap: 12 }}
        onSubmit={(e) => { e.preventDefault(); submit(); }}
      >
        <input
          value={imageUrl}
          onChange={(e) => setImageUrl(e.target.value)}
          placeholder="כתובת תמונת הפורטרט (URL ציבורי)"
        />
        <input
          value={audioUrl}
          onChange={(e) => setAudioUrl(e.target.value)}
          placeholder="כתובת קובץ האודיו (URL ציבורי, wav/mp3)"
        />
        <input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="תיאור הסצנה/סגנון"
        />
        <div style={{ display: "flex", gap: 12 }}>
          <select value={quality} onChange={(e) => setQuality(e.target.value as "high" | "mid")}>
            <option value="high">איכות: high</option>
            <option value="mid">איכות: mid</option>
          </select>
          <select
            value={duration}
            onChange={(e) => setDuration(Number(e.target.value) as 5 | 10 | 15)}
          >
            <option value={5}>5 שניות</option>
            <option value={10}>10 שניות</option>
            <option value={15}>15 שניות</option>
          </select>
        </div>
        <button className="btn" type="submit" disabled={phase === "submitting" || phase === "running"}>
          {phase === "submitting" || phase === "running" ? <span className="spin" /> : "שלח עבודה"}
        </button>
      </form>

      {phase === "running" && (
        <div className="note">
          <div className="t">רץ</div>
          job-set {jobSetId} — בודק כל 5 שניות. עבודה כזאת יכולה לקחת כמה דקות.
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
              <b>העבודה הסתיימה, אבל חילוץ ה-URL האוטומטי לא מצא כלום.</b>
              <div>התשובה הגולמית מוצגת למטה — מצא את השדה הנכון ידנית ושלח אותו כדי לתקן את הקוד.</div>
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
