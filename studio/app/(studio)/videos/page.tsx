"use client";

import { useState } from "react";
import { useStudio } from "../../providers";
import { Episode, Format, Status, STATUS_HE, STATUS_ORDER, engagement, saveRate } from "@/lib/types";
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

type YtVideo = {
  id: string;
  title: string;
  description: string;
  publishedAt: string | null;
  views: number | null;
  likes: number | null;
  comments: number | null;
};
type YtResp = { connected: boolean; reason?: string; videos?: YtVideo[] };

/** Both linking dropdowns below extract the episode a post/video actually names from its
 *  own text, the same regex /api/track already uses server-side. Reused here to warn
 *  before a manual pick disagrees with it — see the linking selects further down. */
const epLinkIn = (text: string) => {
  const m = text.toLowerCase().match(/\/e\/(\d+)/);
  return m ? +m[1] : null;
};

/** Where this episode actually stands per platform, in one place — the thing he asked
 *  for by name. Instagram and YouTube link out to the real post/video when one is
 *  recorded; Facebook has no dash for "posted" because nothing here ever records a
 *  Facebook post against an episode — publishToFacebook() returns a postId but it's
 *  never written back to state, so showing anything but "not tracked" would be a
 *  number this page doesn't actually have. Doesn't touch views/likes/saves/comments/
 *  shares — those stay one shared set per episode, same as before; splitting them
 *  properly per platform is a real schema change, not a display tweak, and touches
 *  engagement()/saveRate() used across /analytics and /studio too. */
function PlatformBadges({ episode: e }: { episode: Episode }) {
  const badge = (label: string, href: string | null, title: string) =>
    href ? (
      <a href={href} target="_blank" rel="noreferrer" title={title} style={{ color: "var(--brass)", marginInlineEnd: 6 }}>
        {label}
      </a>
    ) : (
      <span className="faint" title={title} style={{ marginInlineEnd: 6 }}>
        {label}
      </span>
    );
  return (
    <>
      {badge("IG", e.igPermalink ?? null, e.igPermalink ? "פורסם באינסטגרם" : "לא קושר לפוסט באינסטגרם")}
      {badge("FB", null, "לא במעקב — פרסום לפייסבוק לא נשמר לפרק כרגע")}
      {badge("YT", e.ytVideoId ? `https://youtu.be/${e.ytVideoId}` : null, e.ytVideoId ? "פורסם ביוטיוב" : "לא קושר לסרטון יוטיוב")}
    </>
  );
}

const FORMAT_HE: Record<Format, string> = { reel: "ריל", long: "ארוך", both: "שניהם" };

export default function Videos() {
  const { state, update, refresh } = useStudio();
  const [ig, setIg] = useState<IgResp | null>(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const [yt, setYt] = useState<YtResp | null>(null);
  const [ytBusy, setYtBusy] = useState(false);
  const [ytMsg, setYtMsg] = useState<string | null>(null);

  if (!state) return <p className="sub">טוען…</p>;

  // Both buttons below used to re-derive the auto-link/status logic client-side, by
  // hand, as a second copy of what /api/track already does server-side — which is
  // exactly how a fix could land in one and not the other, and did (the mislink
  // correction pass existed only server-side until a real episode showed "already
  // published" while carrying a different episode's real post). refresh() runs the
  // one canonical implementation and writes back through it; the fetches here are only
  // to populate the "still needs a human to pick" tables further down the page.
  async function sync() {
    setBusy(true);
    setMsg(null);
    try {
      const j = (await fetch("/api/instagram", { cache: "no-store" }).then((r) => r.json())) as IgResp;
      setIg(j);
      const r = await refresh();
      setMsg(!j.connected ? j.reason ?? "אינסטגרם לא מחובר" : r.reason ?? `עודכן · ${r.newEvents ?? 0} שינויים`);
    } catch (e) {
      setMsg((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function syncYoutube() {
    setYtBusy(true);
    setYtMsg(null);
    try {
      const j = (await fetch("/api/youtube", { cache: "no-store" }).then((r) => r.json())) as YtResp;
      setYt(j);
      const r = await refresh();
      setYtMsg(!j.connected ? j.reason ?? "יוטיוב לא מחובר" : r.reason ?? `עודכן · ${r.newEvents ?? 0} שינויים`);
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
      </div>
      <p className="sub" style={{ marginTop: -8, marginBottom: 16 }}>
        פרק חדש נוצר דרך <a href="/pipeline">הצינור</a> — רעיון שהוסכם וקיבל הערכה, לא כפתור
        ריק כאן. הכפתור הידני הוסר: הוא היה יוצר רשומה בלי נושא, בלי הערכה, ובלי דרך קלה לזהות
        שהיא לא אמורה להיות שם.
      </p>

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
            <div className="row" style={{ fontSize: 13 }}>
              <PlatformBadges episode={e} />
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
                ] as const
              ).map(([k, label]) => (
                <div className="g" key={k}>
                  <div className="k">{label}</div>
                  <div className="ro">{n(e[k])}</div>
                </div>
              ))}
              <div className="g">
                <div className="k">נרשמים</div>
                <input inputMode="numeric" value={e.subsAttributed ?? ""} onChange={(ev) => num(i, "subsAttributed", ev.target.value)} />
              </div>
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

      <div className="tw eps boxed">
        <table>
          <thead>
            {/* 16 columns in one flat row read as one undifferentiated wall once the
                table scrolled sideways — this row groups them by what they're for, so
                scrolling into the performance numbers still says so at the top. */}
            <tr className="grp">
              <th colSpan={7}>פרטי הפרק</th>
              <th>פלטפורמות</th>
              <th colSpan={8}>ביצועים · צפיות עד שיתופים אוטומטי מ-Instagram/YouTube, לא לעריכה</th>
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
              <th>IG · FB · YT</th>
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
                <td style={{ whiteSpace: "nowrap" }}>
                  <PlatformBadges episode={e} />
                </td>
                {/* Read-only, not because typing a correction is hard, but because it's
                    exactly what produced a hand-entered row that never matched a real
                    post and threw off the homepage's own live count. These five come
                    from /api/track (Instagram/YouTube) — a platform that's disconnected
                    shows its real last-synced value, not an invented one. subsAttributed
                    stays editable below: no API attributes a signup to an episode. */}
                {(["views", "likes", "saves", "comments", "shares"] as const).map((k) => (
                  <td key={k} className="num">{n(e[k])}</td>
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
              {unlinked.map((m) => {
                // The post's own caption already names its episode when it has an /e/N —
                // that's the exact fact a manual mislink got wrong once (reel 13 picked
                // for what the caption itself named reel 11, one row apart in this same
                // list). Picking anything else now needs a deliberate second click, not
                // one that lands wherever the row happened to be.
                const named = epLinkIn(m.caption || "");
                return (
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
                          const ep = state.episodes.find((x) => x.id === id);
                          if (
                            ep &&
                            named !== null &&
                            named !== ep.number &&
                            !confirm(
                              `הכיתוב של הפוסט הזה מציין בעצמו פרק ${named}, לא פרק ${ep.number}. לקשר בכל זאת לפרק ${ep.number}?`,
                            )
                          ) {
                            ev.target.value = "";
                            return;
                          }
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
                            {e.number === named ? "→ " : ""}
                            {e.number}. {e.title}
                          </option>
                        ))}
                      </select>
                    </td>
                  </tr>
                );
              })}
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
              {unlinkedYt.map((v) => {
                const named = epLinkIn(v.description || "");
                return (
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
                          const ep = state.episodes.find((x) => x.id === id);
                          if (
                            ep &&
                            named !== null &&
                            named !== ep.number &&
                            !confirm(
                              `התיאור של הסרטון הזה מציין בעצמו פרק ${named}, לא פרק ${ep.number}. לקשר בכל זאת לפרק ${ep.number}?`,
                            )
                          ) {
                            ev.target.value = "";
                            return;
                          }
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
                            {e.number === named ? "→ " : ""}
                            {e.number}. {e.title}
                          </option>
                        ))}
                      </select>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
