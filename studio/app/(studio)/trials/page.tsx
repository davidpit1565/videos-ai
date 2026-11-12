import Link from "next/link";
import { reels, canPublish } from "@/lib/reels";
import { n } from "@/lib/fmt";
import { loadState } from "@/lib/db";
import { PUBLISHED_MANUALLY } from "@/lib/publish-order";
import type { Episode } from "@/lib/types";
import { parseTrial, type Trial } from "@/lib/trials";

export const dynamic = "force-dynamic";
export const metadata = { title: "טריילס" };

/** Trial Reels, per episode. A trial is a way of publishing an episode, not a separate
 *  series: the episode number stays the episode number. Read-only on purpose; publishing a
 *  trial goes through /renders (the API) or the Instagram app, graduating only in the app.
 *
 *  Where the status comes from, all of it from the episode row's `notes`:
 *    TRIAL <MANUAL|SS_PERFORMANCE> <mediaId> <permalink> <YYYY-MM-DD>  written by lib/publish.ts
 *    TRIAL-MANUAL <YYYY-MM-DD HH:MM>   a trial posted by hand in the app (no API line exists)
 *    TRIAL-GRADUATED <YYYY-MM-DD>      graduated to everyone by hand in the app */

type Row = { number: number; title: string; ep: Episode | null; trial: Trial | null; status: "ready" | "trial" | "graduated" };

export default async function Trials() {
  // best-effort, the same as /renders: no database just means no trial rows, not a failed page
  const state = await loadState().catch(() => null);
  const episodes = state?.episodes ?? [];
  const byNumber = new Map(episodes.map((e) => [e.number, e]));

  const rows: Row[] = [];
  for (const e of episodes) {
    const trial = parseTrial(e.notes);
    if (trial) rows.push({ number: e.number, title: e.title, ep: e, trial, status: trial.graduated ? "graduated" : "trial" });
  }
  // Ready: a reel that passed the gate (or was approved by hand), not live and not already a trial.
  // Unlike /renders this does not ask Instagram whether a "live" post was deleted by hand.
  const seen = new Set(rows.map((r) => r.number));
  for (const r of reels()) {
    if (r.kind !== "video" || r.episode === null || !canPublish(r) || seen.has(r.episode)) continue;
    const ep = byNumber.get(r.episode) ?? null;
    if (ep?.status === "live" || PUBLISHED_MANUALLY.includes(r.episode)) continue;
    seen.add(r.episode);
    rows.push({ number: r.episode, title: ep?.title || r.title || "", ep, trial: null, status: "ready" });
  }
  const order = { trial: 0, ready: 1, graduated: 2 } as const;
  rows.sort((a, b) => order[a.status] - order[b.status] || b.number - a.number);

  return (
    <main>
      <h1>טריילס</h1>
      <p className="lede">
        טרייל הוא דרך לפרסם פרק, באותו מספר פרק. טרייל שפורסם ידנית באפליקציה מסמנים בהערות הפרק
        בשורה <code>TRIAL-MANUAL YYYY-MM-DD HH:MM</code>, וקידום לכולם בשורה{" "}
        <code>TRIAL-GRADUATED YYYY-MM-DD</code>.
      </p>

      {rows.length === 0 && (
        <div className="empty">
          <b>אין טריילס ואין פרקים שמוכנים לפרסום כרגע.</b>
          <p>{state ? "אף פרק לא מסומן כטרייל בהערות שלו." : "המסד לא נטען, אז אין נתונים להציג."}</p>
        </div>
      )}

      <div className="rlist">
        {rows.map((r) => {
          const t = r.trial;
          const e = r.ep;
          return (
            <div key={r.number} className="rrow">
              <b className="rname">{`ריל ${r.number}${r.title ? ` — ${r.title}` : ""}`}</b>
              <span className="rbadges">
                {r.status === "ready" && <span className="pill unknown">מוכן לפרסום</span>}
                {r.status === "trial" && (
                  <span className="pill" style={{ borderColor: "var(--brass)", color: "var(--brass)" }}>פורסם כטרייל</span>
                )}
                {r.status === "graduated" && <span className="pill pass">הוקדם לכולם</span>}
                {t && <span className="pill unknown">{t.kind === "api" ? `API · ${t.mode}` : "ידני"}</span>}
                {t?.permalink && (
                  <a className="pill unknown" href={t.permalink} target="_blank" rel="noreferrer">
                    פתיחה באינסטגרם
                  </a>
                )}
              </span>
              <span className="rmetas" style={{ flexWrap: "wrap" }}>
                {t && <span className="num rmeta">טרייל: {t.date ?? "—"}</span>}
                {t?.graduated && <span className="num rmeta">הוקדם: {t.graduated}</span>}
                {e && t && (
                  <>
                    <span className="num rmeta">צפיות {n(e.views)}</span>
                    <span className="num rmeta">טווח הגעה {n(e.reach)}</span>
                    <span className="num rmeta">לייקים {n(e.likes)}</span>
                    <span className="num rmeta">שמירות {n(e.saves)}</span>
                    <span className="num rmeta">שיתופים {n(e.shares)}</span>
                  </>
                )}
                {r.status === "ready" && <Link className="rmeta" href="/renders">לרנדרים</Link>}
              </span>
            </div>
          );
        })}
      </div>
    </main>
  );
}
