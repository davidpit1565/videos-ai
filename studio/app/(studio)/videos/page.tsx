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
      {badge("FB", null, "לא במעקב — פרסום לפייסבוק לא נשמר לריל כרגע")}
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
  // Which rows have their secondary fields open — closed by default, so the list reads
  // as one row per reel with its headline numbers, not a wall of inputs. Per-episode id,
  // not index, so an open row stays open across a re-sort or a row above it being deleted.
  const [open, setOpen] = useState<Set<string>>(new Set());
  const toggle = (id: string) =>
    setOpen((s) => {
      const next = new Set(s);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });

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
      <p className="eyebrow">רילים</p>
      <h1>
        כל ריל, עם <em>המספרים שלו</em>
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
        ריל חדש נוצר דרך <a href="/pipeline">הצינור</a> — רעיון שהוסכם וקיבל הערכה, לא כפתור
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

      {/* One row per reel, at every width — no separate phone/desktop implementations to
          keep in sync (that drift is exactly what let the mislink-correction pass exist
          server-side only for a while), and no wide table to scroll sideways through.
          The number is never an input: hand-editing it is what set off two real data
          incidents this same week (a stale-caption /e/N read as ground truth, and a
          manual "link to episode" pick landing one row off) — it comes only from the
          episode being created, and stays whatever it was created as. Everything a pull
          fills in by itself (views, likes, saves, comments, shares, engagement, save
          rate) is plain text, never an input, for the same reason. What's left editable
          is only what genuinely has no other source: title, topic, format, tested,
          published date, and subsAttributed (no API attributes a signup to a reel). */}
      <div className="reels">
        {state.episodes.map((e, i) => {
          const isOpen = open.has(e.id);
          return (
            <div className="reel" key={e.id}>
              <button
                type="button"
                className="reel-main"
                onClick={() => toggle(e.id)}
                aria-expanded={isOpen}
              >
                <span className="reel-no">{e.number}</span>
                <span className="reel-title" dir="auto" title={e.title}>{e.title}</span>
                <span className={"chip s-" + e.status}>{STATUS_HE[e.status]}</span>
                <span className="reel-platforms"><PlatformBadges episode={e} /></span>
                <span className="reel-views">
                  <b>{n(e.views)}</b>
                  {/* Just "צפיות" here read as the total, and the separate YouTube number
                      sits several rows down inside the expanded card — easy to miss
                      entirely on a phone, which is exactly what happened: 174 (Instagram)
                      was read as the whole story while YouTube's real, different number
                      sat unseen below the fold. */}
                  <span className="k">צפיות באינסטגרם</span>
                </span>
                {e.ytViews != null && (
                  <span className="reel-views reel-views-yt">
                    <b>{n(e.ytViews)}</b>
                    <span className="k">ביוטיוב</span>
                  </span>
                )}
                <span className="reel-chevron">{isOpen ? "▲" : "▼"}</span>
              </button>

              {isOpen && (
                <div className="reel-details">
                  <label className="fld">
                    <span className="k">כותרת</span>
                    <input className="cell" dir="auto" value={e.title} onChange={(ev) => set(i, "title", ev.target.value)} />
                  </label>
                  <label className="fld">
                    <span className="k">נושא</span>
                    <input className="cell" dir="auto" value={e.topic} onChange={(ev) => set(i, "topic", ev.target.value)} />
                  </label>
                  <label className="fld">
                    <span className="k">שלב</span>
                    <select className="cell" value={e.status} onChange={(ev) => set(i, "status", ev.target.value as Status)}>
                      {STATUS_ORDER.map((s) => (
                        <option key={s} value={s}>{STATUS_HE[s]}</option>
                      ))}
                    </select>
                  </label>
                  <label className="fld">
                    <span className="k">פורמט</span>
                    <select className="cell" value={e.format} onChange={(ev) => set(i, "format", ev.target.value as Format)}>
                      {(["reel", "long", "both"] as Format[]).map((f) => (
                        <option key={f} value={f}>{FORMAT_HE[f]}</option>
                      ))}
                    </select>
                  </label>
                  <label className="fld fld-check">
                    <input
                      type="checkbox"
                      checked={e.tested}
                      onChange={(ev) => set(i, "tested", ev.target.checked)}
                      style={{ accentColor: "var(--brass)" }}
                    />
                    <span className="k">נבדק</span>
                  </label>
                  <label className="fld">
                    <span className="k">פורסם</span>
                    <input className="cell num" type="date" value={e.publishedAt ?? ""} onChange={(ev) => set(i, "publishedAt", ev.target.value || null)} />
                  </label>

                  <div className="fld ro">
                    <span className="k">לייקים</span>
                    <span className="v">{n(e.likes)}</span>
                  </div>
                  <div className="fld ro">
                    <span className="k">שמירות</span>
                    <span className="v">{n(e.saves)}</span>
                  </div>
                  <div className="fld ro">
                    <span className="k">תגובות</span>
                    <span className="v">{n(e.comments)}</span>
                  </div>
                  <div className="fld ro">
                    <span className="k">שיתופים</span>
                    <span className="v">{n(e.shares)}</span>
                  </div>
                  <div className="fld ro">
                    <span className="k">מדידה</span>
                    <span className="v">{pct(engagement(e))}</span>
                  </div>
                  <div className="fld ro">
                    <span className="k">שמירות/צפייה</span>
                    <span className="v" style={{ color: "var(--brass)" }}>{pct(saveRate(e))}</span>
                  </div>
                  {e.ytViews != null && (
                    <div className="fld ro">
                      <span className="k">צפיות ביוטיוב</span>
                      <span className="v">{n(e.ytViews)}</span>
                    </div>
                  )}

                  <label className="fld">
                    <span className="k">נרשמים שיוחסו</span>
                    <input className="cell n" inputMode="numeric" value={e.subsAttributed ?? ""} onChange={(ev) => num(i, "subsAttributed", ev.target.value)} />
                  </label>

                  <button className="del del-labeled" onClick={() => update((d) => void d.episodes.splice(i, 1))}>
                    × מחק ריל
                  </button>
                </div>
              )}
            </div>
          );
        })}
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
        <p className="sub">כל הפוסטים בחשבון מקושרים לריל.</p>
      ) : (
        <div className="tw boxed">
          <table>
            <thead>
              <tr>
                <th>פוסט</th>
                <th>תאריך</th>
                <th>צפיות</th>
                <th>שמירות</th>
                <th>לקשר לריל</th>
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
                              `הכיתוב של הפוסט הזה מציין בעצמו ריל ${named}, לא ריל ${ep.number}. לקשר בכל זאת לריל ${ep.number}?`,
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
                        <option value="">בחר ריל…</option>
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
        <p className="sub">כל הסרטונים בערוץ מקושרים לריל.</p>
      ) : (
        <div className="tw boxed">
          <table>
            <thead>
              <tr>
                <th>סרטון</th>
                <th>תאריך</th>
                <th>צפיות</th>
                <th>לייקים</th>
                <th>לקשר לריל</th>
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
                      {/** The native <select> below is the original control — kept for the
                       *  case where the video's description doesn't name an episode at all.
                       *  He hit a real dead end with it once (2.9.2026): the dropdown opened,
                       *  a row highlighted, and nothing — no change event, no network
                       *  request, in Chrome and in the wrapped app alike, across mouse and
                       *  keyboard. Never root-caused (no console error either), so instead
                       *  of leaving the one linking control on this page a single point of
                       *  failure, the common case — the video's own description already
                       *  names the right episode — gets a plain button that does the exact
                       *  same update() with one click, no dropdown involved at all. */}
                      {(() => {
                        function linkTo(id: string) {
                          update((d) => {
                            const ep = d.episodes.find((x) => x.id === id);
                            if (!ep) return;
                            ep.ytVideoId = v.id;
                            // ytViews/ytLikes/ytComments, never views/likes/comments — those
                            // are Instagram's own fields (see the comment on Episode in
                            // types.ts). This same manual link used to write YouTube's
                            // numbers into Instagram's fields, which is the exact bug that
                            // silently erased six episodes' real view counts every pull.
                            if (v.views !== null) ep.ytViews = v.views;
                            if (v.likes !== null) ep.ytLikes = v.likes;
                            if (v.comments !== null) ep.ytComments = v.comments;
                            ep.publishedAt = v.publishedAt?.slice(0, 10) ?? ep.publishedAt;
                            ep.status = "live";
                          });
                        }
                        const namedEp = named !== null ? state.episodes.find((e) => e.number === named) : undefined;
                        return (
                          <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
                            {namedEp && (
                              <button type="button" className="btn small" onClick={() => linkTo(namedEp.id)}>
                                קשר לריל {named} (מה שהתיאור מציין)
                              </button>
                            )}
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
                                    `התיאור של הסרטון הזה מציין בעצמו ריל ${named}, לא ריל ${ep.number}. לקשר בכל זאת לריל ${ep.number}?`,
                                  )
                                ) {
                                  ev.target.value = "";
                                  return;
                                }
                                linkTo(id);
                              }}
                            >
                              <option value="">בחר ריל…</option>
                              {state.episodes.map((e) => (
                                <option key={e.id} value={e.id}>
                                  {e.number === named ? "→ " : ""}
                                  {e.number}. {e.title}
                                </option>
                              ))}
                            </select>
                          </div>
                        );
                      })()}
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
