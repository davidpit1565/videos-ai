import Link from "next/link";
import { notFound } from "next/navigation";
import { reelByFile } from "@/lib/reels";
import Copy from "../copy";
import IgStats from "../igstats";

export const dynamic = "force-dynamic";

export async function generateMetadata({ params }: { params: Promise<{ file: string }> }) {
  const { file } = await params;
  const r = reelByFile(decodeURIComponent(file));
  return { title: r ? (r.episode !== null ? `פרק ${r.episode}` : r.file) : "רנדר" };
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
                ? `פרק ${r.episode}`
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
          <span className="num">{r.builtAt.slice(0, 16).replace("T", " ")}</span>
          <a href={r.src} download>
            הורדה
          </a>
        </div>

        {r.gate && (
          <details className="gate" open={!r.gate.passed}>
            <summary>{r.gate.passed ? "פלט השער" : "מה נפל"}</summary>
            <pre>{r.gate.text}</pre>
          </details>
        )}

        {r.caption && <Copy text={r.caption} />}
      </section>
    </main>
  );
}
