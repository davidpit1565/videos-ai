import Link from "next/link";
import { notFound } from "next/navigation";
import { reelByFile } from "@/lib/reels";
import Copy from "../copy";
import IgStats from "../igstats";
import PublishButtons from "./publish-buttons";
import { localDT } from "@/lib/fmt";

export const dynamic = "force-dynamic";

export async function generateMetadata({ params }: { params: Promise<{ file: string }> }) {
  const { file } = await params;
  const r = reelByFile(decodeURIComponent(file));
  return { title: r ? (r.episode !== null ? `ריל ${r.episode}` : r.file) : "רנדר" };
}

/** One reel, full screen. Split out of the /renders list so the list can stay a list once
 *  there are twenty of these instead of two — he asked for exactly this, before it became
 *  the reason he could not find last week's approval. */
export default async function RenderDetail({ params }: { params: Promise<{ file: string }> }) {
  const { file } = await params;
  const r = reelByFile(decodeURIComponent(file));
  if (!r) notFound();

  return (
    <main>
      <p className="back">
        <Link href="/renders">← כל הרנדרים</Link>
      </p>

      <section className="render">
        <div className="rhead">
          <b>
            {r.kind === "audio"
              ? r.file.replace(/\.[^.]+$/, "")
              : r.episode !== null
                ? `ריל ${r.episode}`
                : r.file}
          </b>
          {r.gate === null ? (
            <span className="pill unknown">השער לא רץ</span>
          ) : r.gate.passed ? (
            <span className="pill pass">עבר את השער</span>
          ) : (
            <span className="pill fail">נפל בשער — לא לפרסם</span>
          )}
        </div>

        {r.kind === "video" ? (
          <video className="player" src={r.src} controls preload="metadata" playsInline />
        ) : (
          <audio className="aplayer" src={r.src} controls preload="metadata" />
        )}

        <div className="meta">
          <span className="num">{(r.bytes / 1e6).toFixed(1)} MB</span>
          <span className="num">{localDT(r.builtAt)}</span>
          <a href={r.src} download>
            הורדה
          </a>
        </div>

        {/* Right after the player, before anything else — this used to sit at the very
            bottom of the page, past the gate output and both copy-paste blocks, and he
            couldn't find it. The button he's looking for belongs where his eyes land
            right after watching, not after two unrelated sections. */}
        {r.kind === "video" && r.gate?.passed && (
          <PublishButtons file={r.file} caption={r.caption} youtube={r.youtube} />
        )}

        {r.gate && (
          <details className="gate" open={!r.gate.passed}>
            <summary>{r.gate.passed ? "פלט השער" : "מה נפל"}</summary>
            <pre>{r.gate.text}</pre>
          </details>
        )}

        {r.caption && (
          <>
            <p className="section-label">כיתוב לאינסטגרם</p>
            <Copy text={r.caption} />
          </>
        )}

        {r.youtube && (
          <>
            <p className="section-label">כותרת + תיאור ל-YouTube Shorts</p>
            <Copy text={r.youtube} />
          </>
        )}
      </section>
    </main>
  );
}
