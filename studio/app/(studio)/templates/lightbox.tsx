"use client";

import Image from "next/image";
import { useState } from "react";

/** Click a template thumbnail to see it full-size — the 270x480 grid card is too small
 *  to actually judge a design from before committing an episode to it. */
export default function TemplateThumb({ src, alt, num }: { src: string; alt: string; num: number }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button
        type="button"
        className="tplthumb"
        onClick={() => setOpen(true)}
        style={{ border: 0, padding: 0, cursor: "zoom-in", background: "none" }}
        aria-label={`הגדל את ${alt}`}
      >
        <Image src={src} alt={alt} width={270} height={480} />
        <span className="tplnum">{num}</span>
      </button>
      {open && (
        <div
          role="dialog"
          aria-modal="true"
          onClick={() => setOpen(false)}
          style={{
            position: "fixed",
            inset: 0,
            zIndex: 1000,
            background: "rgba(6,9,7,.88)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: 24,
            cursor: "zoom-out",
          }}
        >
          <Image
            src={src}
            alt={alt}
            width={270}
            height={480}
            style={{ width: "auto", height: "min(88vh, 900px)", borderRadius: 14 }}
          />
        </div>
      )}
    </>
  );
}
