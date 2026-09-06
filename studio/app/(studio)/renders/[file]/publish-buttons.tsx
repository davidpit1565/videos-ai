"use client";

import { useEffect, useState } from "react";

type Props = { file: string; caption: string | null; youtube: string | null };

/** Real publish buttons — not a preview of what publishing would look like. Each one is a
 *  single, real, irreversible HTTP call to a live public account, so nothing here fires on
 *  its own; a person presses it. */
export default function PublishButtons({ file, caption, youtube }: Props) {
  const [igBusy, setIgBusy] = useState(false);
  const [igMsg, setIgMsg] = useState<string | null>(null);
  const [fbBusy, setFbBusy] = useState(false);
  const [fbMsg, setFbMsg] = useState<string | null>(null);
  const [ytBusy, setYtBusy] = useState(false);
  const [ytMsg, setYtMsg] = useState<string | null>(null);
  const [ytConnected, setYtConnected] = useState<boolean | null>(null);
  const [ytUploadedToday, setYtUploadedToday] = useState(false);

  useEffect(() => {
    fetch("/api/youtube/status")
      .then((r) => r.json())
      .then((j) => {
        setYtConnected(!!j.connected);
        setYtUploadedToday(!!j.uploadedToday);
      })
      .catch(() => setYtConnected(false));
  }, []);

  async function doInstagram() {
    if (
      !confirm(
        "לפרסם עכשיו — ריל לאינסטגרם, ואם מחובר גם פייסבוק — פומבי, לכל העולם? אין דרך למחוק את זה מכאן.",
      )
    )
      return;
    setIgBusy(true);
    setIgMsg(null);
    try {
      const r = await fetch("/api/instagram/publish", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ file, caption: caption ?? "" }),
      }).then((x) => x.json());
      const lines = [
        r.reel?.ok ? `ריל ✓${r.reel.permalink ? ` — ${r.reel.permalink}` : ""}` : `ריל נכשל: ${r.reel?.reason}`,
        r.story
          ? r.story.ok
            ? "סטורי ✓"
            : `סטורי נכשל: ${r.story.reason}`
          : null,
        r.facebook
          ? r.facebook.ok
            ? "פייסבוק ✓"
            : `פייסבוק: ${r.facebook.reason}`
          : null,
      ].filter(Boolean);
      setIgMsg(lines.join(" · "));
    } catch (e) {
      setIgMsg(`שגיאה: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setIgBusy(false);
    }
  }

  /** A retry that touches only the Facebook Page post — for a file whose Reel already
   *  published (like episodes 21 and 22, where the Reel went out but Facebook didn't),
   *  so it never needs to re-publish a second, duplicate Reel just to try Facebook again. */
  async function doFacebook() {
    if (!confirm("לפרסם עכשיו לפייסבוק — פומבי, לכל העולם? אין דרך למחוק את זה מכאן.")) return;
    setFbBusy(true);
    setFbMsg(null);
    try {
      const r = await fetch("/api/facebook/publish", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ file, caption: caption ?? "" }),
      }).then((x) => x.json());
      setFbMsg(r.facebook?.ok ? "פייסבוק ✓" : `פייסבוק נכשל: ${r.facebook?.reason}`);
    } catch (e) {
      setFbMsg(`שגיאה: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setFbBusy(false);
    }
  }

  async function doYoutube() {
    const title = (youtube ?? "").split("\n")[0]?.trim();
    if (!title) {
      setYtMsg("אין קובץ כותרת ל-YouTube לריל הזה (episode-NN-youtube.txt)");
      return;
    }
    const warn = ytUploadedToday
      ? "כבר הועלה סרטון ל-YouTube היום — מכסת ההעלאות היומית שלהם קטנה במיוחד לערוצים חדשים, וסביר שההעלאה הזו תיכשל. "
      : "";
    if (!confirm(`${warn}להעלות עכשיו ל-YouTube, פומבי, לכל העולם? אין דרך למחוק את זה מכאן.`)) return;
    setYtBusy(true);
    setYtMsg(null);
    try {
      const description = (youtube ?? "").split("\n").slice(1).join("\n").trim();
      const r = await fetch("/api/youtube/publish", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ file, title, description }),
      }).then((x) => x.json());
      if (r.ok) setYtUploadedToday(true);
      setYtMsg(r.ok ? `הועלה ✓ — https://youtube.com/watch?v=${r.videoId}` : `נכשל: ${r.reason}`);
    } catch (e) {
      setYtMsg(`שגיאה: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setYtBusy(false);
    }
  }

  return (
    <div className="note" style={{ marginTop: 14 }}>
      <p className="section-label">פרסום</p>
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
        <button className="btn" onClick={doInstagram} disabled={igBusy}>
          {igBusy ? "מפרסם…" : "פרסם: ריל + פייסבוק"}
        </button>
        <button className="btn ghost" onClick={doFacebook} disabled={fbBusy}>
          {fbBusy ? "מפרסם…" : "פרסם: פייסבוק בלבד (נסיון חוזר)"}
        </button>
        {ytConnected === false ? (
          <a className="btn ghost" href="/api/youtube/auth">
            חבר את YouTube (פעם אחת)
          </a>
        ) : (
          <button className="btn" onClick={doYoutube} disabled={ytBusy || ytConnected === null}>
            {ytBusy ? "מעלה…" : "העלה ל-YouTube"}
          </button>
        )}
      </div>
      {ytUploadedToday && !ytMsg && (
        <p className="hint" style={{ marginTop: 8, color: "var(--clay)" }}>
          כבר הועלה סרטון ל-YouTube היום — סביר שהעלאה נוספת תיכשל בגלל המכסה היומית שלהם.
        </p>
      )}
      {igMsg && <p className="hint mono" style={{ marginTop: 8 }}>{igMsg}</p>}
      {fbMsg && <p className="hint mono" style={{ marginTop: 8 }}>{fbMsg}</p>}
      {ytMsg && <p className="hint mono" style={{ marginTop: 8 }}>{ytMsg}</p>}
    </div>
  );
}
