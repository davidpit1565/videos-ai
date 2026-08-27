"use client";

import { useEffect, useState } from "react";

type Props = { file: string; caption: string | null; youtube: string | null };

/** Real publish buttons — not a preview of what publishing would look like. Each one is a
 *  single, real, irreversible HTTP call to a live public account, so nothing here fires on
 *  its own; a person presses it. */
export default function PublishButtons({ file, caption, youtube }: Props) {
  const [igBusy, setIgBusy] = useState(false);
  const [igMsg, setIgMsg] = useState<string | null>(null);
  const [ytBusy, setYtBusy] = useState(false);
  const [ytMsg, setYtMsg] = useState<string | null>(null);
  const [ytConnected, setYtConnected] = useState<boolean | null>(null);

  useEffect(() => {
    fetch("/api/youtube/status")
      .then((r) => r.json())
      .then((j) => setYtConnected(!!j.connected))
      .catch(() => setYtConnected(false));
  }, []);

  async function doInstagram() {
    if (
      !confirm(
        "לפרסם עכשיו — ריל לאינסטגרם, סטורי, ואם מחובר גם פייסבוק — פומבי, לכל העולם? אין דרך למחוק את זה מכאן.",
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

  async function doYoutube() {
    const title = (youtube ?? "").split("\n")[0]?.trim();
    if (!title) {
      setYtMsg("אין קובץ כותרת ל-YouTube לריל הזה (episode-NN-youtube.txt)");
      return;
    }
    if (!confirm("להעלות עכשיו ל-YouTube, פומבי, לכל העולם? אין דרך למחוק את זה מכאן.")) return;
    setYtBusy(true);
    setYtMsg(null);
    try {
      const description = (youtube ?? "").split("\n").slice(1).join("\n").trim();
      const r = await fetch("/api/youtube/publish", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ file, title, description }),
      }).then((x) => x.json());
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
          {igBusy ? "מפרסם…" : "פרסם: ריל + סטורי + פייסבוק"}
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
      {igMsg && <p className="hint mono" style={{ marginTop: 8 }}>{igMsg}</p>}
      {ytMsg && <p className="hint mono" style={{ marginTop: 8 }}>{ytMsg}</p>}
    </div>
  );
}
