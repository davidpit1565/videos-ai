"use client";

import { useState } from "react";
import { useStudio } from "../providers";
import { Episode, Format, Status, STATUS_HE, STATUS_ORDER, engagement, saveRate, uid } from "@/lib/types";
import { n, pct } from "@/lib/fmt";

type IgMedia = {
  id: string;
  caption: string;
  permalink: string | null;
  timestamp: string | null;
  mediaType: string | null;
  views: number | null;
  reach: number | null;
  saves: number | null;
  shares: number | null;
  likes: number | null;
  comments: number | null;
};
type IgResp = { connected: boolean; reason?: string; media?: IgMedia[] };

type YtVideo = { id: string; title: string; publishedAt: string | null; views: number | null; likes: number | null; comments: number | null };
type YtResp = { connected: boolean; reason?: string; videos?: YtVideo[] };

const FORMAT_HE: Record<Format, string> = { reel: "ריל", long: "ארוך", both: "שניהם" };

export default function Videos() {
  const { state, update } = useStudio();
  const [ig, setIg] = useState<IgResp | null>(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const [yt, setYt] = useState<YtResp | null>(null);
  const [ytBusy, setYtBusy] = useState(false);
  const [ytMsg, setYtMsg] = useState<string | null>(null);

  if (!state) return <p className="sub">טוען…</p>;

  /** Pull the live numbers and copy them onto whichever episodes carry a media id. */
  async function sync() {
    setBusy(true);
    setMsg(null);
    try {
      const r = await fetch("/api/instagram", { cache: "no-store" });
      const j = (await r.json()) as IgResp;
      setIg(j);
      if (!j.connected) {
        setMsg(j.reason ?? "אינסטגרם לא מחובר");
        return;
      }
      const by = new Map((j.media ?? []).map((m) => [m.id, m]));
      let hit = 0, autoLinked = 0;
      update((d) => {
        for (const e of d.episodes) {
          const m = e.igMediaId ? by.get(e.igMediaId) : undefined;
          if (!m) continue;
          hit++;
          e.views = m.views ?? m.reach ?? e.views;
          e.likes = m.likes ?? e.likes;
          e.saves = m.saves ?? e.saves;
          e.comments = m.comments ?? e.comments;
          e.shares = m.shares ?? e.shares;
          if (!e.igPermalink && m.permalink) e.igPermalink = m.permalink;
          if (!e.publishedAt && m.timestamp) e.publishedAt = m.timestamp.slice(0, 10);
          if (e.status !== "live") e.status = "live";
        }
        // Every caption we write ends with "actually-works-studio.vercel.app/e/N" —
        // an exact, unambiguous episode number, so that's the first thing checked.
        // Title matching is the fallback, for older posts or a caption written by
        // hand without the link: a post whose caption plainly names an episode's own
        // title gets linked automatically instead of sitting in the "לקשר לפרק" list
        // forever — but only when exactly one unlinked episode's title matches, so an
        // ambiguous caption still falls through to the dropdown below.
        const linkedIds = new Set(d.episodes.map((e) => e.igMediaId).filter(Boolean));
        const unlinkedEps = d.episodes.filter((e) => !e.igMediaId);
        for (const m of j.media ?? []) {
          if (linkedIds.has(m.id)) continue;
          const caption = (m.caption || "").toLowerCase();
          const epLink = caption.match(/\/e\/(\d+)/);
          const byNumber = epLink ? unlinkedEps.filter((e) => e.number === +epLink[1]) : [];
          const matches =
            byNumber.length === 1
              ? byNumber
              : unlinkedEps.filter((e) => {
                  const title = e.title.trim().toLowerCase();
                  return title.length > 4 && title !== "פרק חדש" && caption.includes(title);
                });
          if (matches.length !== 1) continue;
          const e = matches[0];
          e.igMediaId = m.id;
          e.igPermalink = m.permalink;
          e.views = m.views ?? m.reach ?? e.views;
          e.likes = m.likes ?? e.likes;
          e.saves = m.saves ?? e.saves;
          e.comments = m.comments ?? e.comments;
          e.shares = m.shares ?? e.shares;
          if (!e.publishedAt && m.timestamp) e.publishedAt = m.timestamp.slice(0, 10);
          e.status = "live";
          linkedIds.add(m.id);
          autoLinked++;
        }
      });
      setMsg(
        hit === 0 && autoLinked === 0
          ? `אינסטגרם מחובר, ${(j.media ?? []).length} פוסטים נמצאו — אבל אף פרק לא מקושר לפוסט. לחבר למטה.`
          : autoLinked > 0
            ? `עודכנו ${hit} פרקים, וקושרו אוטומטית עוד ${autoLinked} לפי הכותרת בפוסט.`
            : `עודכנו ${hit} פרקים מהמספרים החיים.`,
      );
    } catch (e) {
      setMsg((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  /** Same idea as sync() above, for YouTube: pull the live numbers and copy them onto
   *  whichever episodes already carry a video id. */
  async function syncYoutube() {
    setYtBusy(true);
    setYtMsg(null);
    try {
      const r = await fetch("/api/youtube", { cache: "no-store" });
      const j = (await r.json()) as YtResp;
      setYt(j);
      if (!j.connected) {
        setYtMsg(j.reason ?? "יוטיוב לא מחובר");
        return;
      }
      const by = new Map((j.videos ?? []).map((v) => [v.id, v]));
      let hit = 0;
      update((d) => {
        for (const e of d.episodes) {
          const v = e.ytVideoId ? by.get(e.ytVideoId) : undefined;
          if (!v) continue;
          hit++;
          if (v.views !== null) e.views = v.views;
          if (v.likes !== null) e.likes = v.likes;
          if (v.comments !== null) e.comments = v.comments;
          if (!e.publishedAt && v.publishedAt) e.publishedAt = v.publishedAt.slice(0, 10);
          if (e.status !== "live") e.status = "live";
        }
      });
      setYtMsg(
        hit === 0
          ? `יוטיוב מחובר, ${(j.videos ?? []).length} סרטונים נמצאו — אבל אף פרק לא מקושר לסרטון. לחבר למטה.`
          : `עודכנו ${hit} פרקים מהמספרים החיים.`,
      );
    } catch (e) {
      setYtMsg((e as Error).message);
    } finally {
      setYtBusy(false);
    }
  }

  const set = <K extends keyof Episode>(i: number, k: K, v: Episode[K]) =>
    update((d) => void (d.episodes[i][k] = v));

  const num = (i: number, k: "views" | "likes" | "saves" | "comments" | "shares" | "subsAttributed", raw: string) =>
    update((d) => {
      const v = raw.trim();
      d.episodes[i][k] = v === "" ? null : Number(v.replace(/[^\d]/g, ""));
    });

  const linked = new Set(state.episodes.map((e) => e.igMediaId).filter(Boolean) as string[]);
  const unlinked = (ig?.media ?? []).filter((m) => !linked.has(m.id));

  const linkedYt = new Set(state.episodes.map((e) => e.ytVideoId).filter(Boolean) as string[]);
  const unlinkedYt = (yt?.videos ?? []).filter((v) => !linkedYt.has(v.id));

  return (
    <>
      <p className="eyebrow">פרקים</p>
      <h1>
        כל פרק, עם <em>המספרים שלו</em>
      </h1>
      <p className="sub">
        אחוז מדידה = כל האינטראקציות חלקי צפיות. <b>שמירות לצפייה</b> זה המדד שקובע האם התוכן
        עצמו עבד — הוק חזק מביא צפיות, רק תוכן שימושי מביא שמירות.
      </p>

      <div className="actions" style={{ marginBottom: 16 }}>
        <button className="btn" onClick={sync} disabled={busy}>
          {busy ? <span className="spin" /> : "משיכת מספרים מאינסטגרם"}
        </button>
        <button className="btn" onClick={syncYoutube} disabled={ytBusy}>
          {ytBusy ? <span className="spin" /> : "משיכת מספרים מיוטיוב"}
        </button>
        <button
          className="btn ghost"
          onClick={() =>
            update((d) =>
              void d.episodes.push({
                id: uid(),
                number: Math.max(0, ...d.episodes.map((e) => e.number)) + 1,
                title: "פרק חדש",
                format: "reel",
                status: "idea",
                topic: "",
                tested: false,
                publishedAt: null,
                igMediaId: null,
                ytVideoId: null,
                notes: "",
                views: null,
                likes: null,
                saves: null,
                comments: null,
                shares: null,
                subsAttributed: null,
              }),
            )
          }
        >
          + פרק
        </button>
      </div>

      {msg && (
        <div className={"note " + (ig?.connected ? "ok" : "warn")}>
          <div className="t">{ig?.connected ? "סנכרון" : "לא מחובר"}</div>
          {msg}
        </div>
      )}
      {ytMsg && (
        <div className={"note " + (yt?.connected ? "ok" : "warn")}>
          <div className="t">{yt?.connected ? "סנכרון יוטיוב" : "יוטיוב לא מחובר"}</div>
          {ytMsg}
        </div>
      )}

      {/* phone view — same data, one card per episode */}
      <div className="cards">
        {state.episodes.map((e, i) => (
          <div className="card" key={e.id}>
            <div className="hd">
              <span className="no">{e.number}</span>
              <input className="cell" dir="auto" value={e.title} onChange={(ev) => set(i, "title", ev.target.value)} />
              <span className={"chip s-" + e.status}>{STATUS_HE[e.status]}</span>
            </div>
            <div className="row">
              <select className="cell" value={e.status} onChange={(ev) => set(i, "status", ev.target.value as Status)}>
                {STATUS_ORDER.map((s) => (
                  <option key={s} value={s}>
                    {STATUS_HE[s]}
                  </option>
                ))}
              </select>
              <select className="cell" value={e.format} onChange={(ev) => set(i, "format", ev.target.value as Format)}>
                {(["reel", "long", "both"] as Format[]).map((f) => (
                  <option key={f} value={f}>
                    {FORMAT_HE[f]}
                  </option>
                ))}
              </select>
              <label>
                <input
                  type="checkbox"
                  checked={e.tested}
                  onChange={(ev) => set(i, "tested", ev.target.checked)}
                  style={{ accentColor: "var(--brass)" }}
                />
                נבדק
              </label>
              <button className="del del-labeled" onClick={() => update((d) => void d.episodes.splice(i, 1))}>
                × מחק פרק
              </button>
            </div>
            <div className="grid">
              {(
                [
                  ["views", "צפיות"],
                  ["likes", "לייקים"],
                  ["saves", "שמירות"],
                  ["comments", "תגובות"],
                  ["shares", "שיתופים"],
                  ["subsAttributed", "נרשמים"],
                ] as const
              ).map(([k, label]) => (
                <div className="g" key={k}>
                  <div className="k">{label}</div>
                  <input inputMode="numeric" value={e[k] ?? ""} onChange={(ev) => num(i, k, ev.target.value)} />
                </div>
              ))}
              <div className="g">
                <div className="k">מדידה</div>
                <div className="ro">{pct(engagement(e))}</div>
              </div>
              <div className="g">
                <div className="k">שמירות/צפייה</div>
                <div className="ro">{pct(saveRate(e))}</div>
              </div>
              <div className="g">
                <div className="k">פורסם</div>
                <input
                  type="date"
                  value={e.publishedAt ?? ""}
                  onChange={(ev) => set(i, "publishedAt", ev.target.value || null)}
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="tw eps">
        <table>
          <thead>
            {/* 16 columns in one flat row read as one undifferentiated wall once the
                table scrolled sideways — this row groups them by what they're for, so
                scrolling into the performance numbers still says so at the top. */}
            <tr className="grp">
              <th colSpan={7}>פרטי הפרק</th>
              <th colSpan={8}>ביצועים</th>
              <th />
            </tr>
            <tr>
              <th className="sticky c1">#</th>
              <th className="sticky c2">כותרת</th>
              <th>נושא</th>
              <th>פורמט</th>
              <th>שלב</th>
              <th>נבדק</th>
              <th>פורסם</th>
              <th>צפיות</th>
              <th>לייקים</th>
              <th>שמירות</th>
              <th>תגובות</th>
              <th>שיתופים</th>
              <th>מדידה</th>
              <th>שמירות/צפייה</th>
              <th>נרשמים</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {state.episodes.map((e, i) => (
              <tr key={e.id}>
                <td className="sticky c1">
                  <input
                    className="cell n"
                    style={{ width: 46 }}
                    value={e.number}
                    onChange={(ev) => set(i, "number", Number(ev.target.value.replace(/[^\d]/g, "") || 0))}
                  />
                </td>
                <td className="name sticky c2">
                  <input className="cell" dir="auto" value={e.title} onChange={(ev) => set(i, "title", ev.target.value)} />
                </td>
                <td>
                  <input className="cell" dir="auto" value={e.topic} onChange={(ev) => set(i, "topic", ev.target.value)} />
                </td>
                <td>
                  <select
                    className="cell"
                    value={e.format}
                    onChange={(ev) => set(i, "format", ev.target.value as Format)}
                  >
                    {(["reel", "long", "both"] as Format[]).map((f) => (
                      <option key={f} value={f}>
                        {FORMAT_HE[f]}
                      </option>
                    ))}
                  </select>
                </td>
                <td>
                  <select
                    className="cell"
                    value={e.status}
                    onChange={(ev) => set(i, "status", ev.target.value as Status)}
                  >
                    {STATUS_ORDER.map((s) => (
                      <option key={s} value={s}>
                        {STATUS_HE[s]}
                      </option>
                    ))}
                  </select>
                </td>
                <td style={{ textAlign: "center" }}>
                  <input
                    type="checkbox"
                    checked={e.tested}
                    onChange={(ev) => set(i, "tested", ev.target.checked)}
                    style={{ accentColor: "var(--brass)" }}
                  />
                </td>
                <td>
                  <input
                    className="cell num"
                    type="date"
                    value={e.publishedAt ?? ""}
                    onChange={(ev) => set(i, "publishedAt", ev.target.value || null)}
                  />
                </td>
                {(["views", "likes", "saves", "comments", "shares"] as const).map((k) => (
                  <td key={k}>
                    <input className="cell n" inputMode="numeric" value={e[k] ?? ""} onChange={(ev) => num(i, k, ev.target.value)} />
                  </td>
                ))}
                <td className="num">{pct(engagement(e))}</td>
                <td className="num" style={{ color: "var(--brass)" }}>
                  {pct(saveRate(e))}
                </td>
                <td>
                  <input className="cell n" inputMode="numeric" value={e.subsAttributed ?? ""} onChange={(ev) => num(i, "subsAttributed", ev.target.value)} />
                </td>
                <td>
                  <button className="del del-labeled" onClick={() => update((d) => void d.episodes.splice(i, 1))}>
                    × מחק
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2>קישור לפוסטים באינסטגרם</h2>
      {!ig ? (
        <p className="sub">לחץ על &quot;משיכת מספרים&quot; כדי לראות את הפוסטים בחשבון.</p>
      ) : !ig.connected ? (
        <p className="sub">
          אינסטגרם לא מחובר: {ig.reason}. עד אז אפשר להזין את המספרים ידנית בטבלה למעלה — הם נשמרים
          אותו דבר.
        </p>
      ) : unlinked.length === 0 ? (
        <p className="sub">כל הפוסטים בחשבון מקושרים לפרק.</p>
      ) : (
        <div className="tw boxed">
          <table>
            <thead>
              <tr>
                <th>פוסט</th>
                <th>תאריך</th>
                <th>צפיות</th>
                <th>שמירות</th>
                <th>לקשר לפרק</th>
              </tr>
            </thead>
            <tbody>
              {unlinked.map((m) => (
                <tr key={m.id}>
                  <td className="name">
                    {m.permalink ? (
                      <a href={m.permalink} target="_blank" rel="noreferrer" style={{ color: "var(--steel)" }}>
                        {m.caption || m.id}
                      </a>
                    ) : (
                      m.caption || m.id
                    )}
                  </td>
                  <td className="num">{m.timestamp?.slice(0, 10) ?? "—"}</td>
                  <td className="num">{n(m.views ?? m.reach)}</td>
                  <td className="num">{n(m.saves)}</td>
                  <td>
                    <select
                      className="cell"
                      defaultValue=""
                      onChange={(ev) => {
                        const id = ev.target.value;
                        if (!id) return;
                        update((d) => {
                          const ep = d.episodes.find((x) => x.id === id);
                          if (!ep) return;
                          ep.igMediaId = m.id;
                          ep.igPermalink = m.permalink;
                          ep.views = m.views ?? m.reach;
                          ep.likes = m.likes;
                          ep.saves = m.saves;
                          ep.comments = m.comments;
                          ep.shares = m.shares;
                          ep.publishedAt = m.timestamp?.slice(0, 10) ?? ep.publishedAt;
                          ep.status = "live";
                        });
                      }}
                    >
                      <option value="">בחר פרק…</option>
                      {state.episodes.map((e) => (
                        <option key={e.id} value={e.id}>
                          {e.number}. {e.title}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <h2>קישור לסרטוני יוטיוב</h2>
      {!yt ? (
        <p className="sub">לחץ על &quot;משיכת מספרים מיוטיוב&quot; כדי לראות את הסרטונים בערוץ.</p>
      ) : !yt.connected ? (
        <p className="sub">
          יוטיוב לא מחובר: {yt.reason}. עד אז אפשר להזין את המספרים ידנית בטבלה למעלה — הם נשמרים
          אותו דבר.
        </p>
      ) : unlinkedYt.length === 0 ? (
        <p className="sub">כל הסרטונים בערוץ מקושרים לפרק.</p>
      ) : (
        <div className="tw boxed">
          <table>
            <thead>
              <tr>
                <th>סרטון</th>
                <th>תאריך</th>
                <th>צפיות</th>
                <th>לייקים</th>
                <th>לקשר לפרק</th>
              </tr>
            </thead>
            <tbody>
              {unlinkedYt.map((v) => (
                <tr key={v.id}>
                  <td className="name">
                    <a href={`https://youtu.be/${v.id}`} target="_blank" rel="noreferrer" style={{ color: "var(--steel)" }}>
                      {v.title}
                    </a>
                  </td>
                  <td className="num">{v.publishedAt?.slice(0, 10) ?? "—"}</td>
                  <td className="num">{n(v.views)}</td>
                  <td className="num">{n(v.likes)}</td>
                  <td>
                    <select
                      className="cell"
                      defaultValue=""
                      onChange={(ev) => {
                        const id = ev.target.value;
                        if (!id) return;
                        update((d) => {
                          const ep = d.episodes.find((x) => x.id === id);
                          if (!ep) return;
                          ep.ytVideoId = v.id;
                          if (v.views !== null) ep.views = v.views;
                          if (v.likes !== null) ep.likes = v.likes;
                          if (v.comments !== null) ep.comments = v.comments;
                          ep.publishedAt = v.publishedAt?.slice(0, 10) ?? ep.publishedAt;
                          ep.status = "live";
                        });
                      }}
                    >
                      <option value="">בחר פרק…</option>
                      {state.episodes.map((e) => (
                        <option key={e.id} value={e.id}>
                          {e.number}. {e.title}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
