"use client";

import Image from "next/image";
import { useState } from "react";

/** Same click-to-zoom pattern as TemplateThumb, sized for the avatar wardrobe's square
 *  crops instead of a 9:16 template frame — using TemplateThumb's fixed 270x480 box would
 *  stretch every one of these. */
export default function AvatarThumb({ src, alt, num }: { src: string; alt: string; num: number }) {
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
        <Image src={src} alt={alt} width={220} height={220} style={{ objectFit: "cover", width: "100%", height: "auto", aspectRatio: "1 / 1" }} />
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
            width={600}
            height={600}
            style={{ width: "min(88vw, 600px)", height: "auto", borderRadius: 14 }}
          />
        </div>
      )}
    </>
  );
}
