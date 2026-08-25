"use client";

import { useEffect } from "react";

declare global {
  interface Window {
    instgrm?: { Embeds: { process: () => void } };
  }
}

/** Instagram's own documented embed (developers.facebook.com/docs/instagram-platform/oembed):
 *  a blockquote with the post's permalink, processed client-side by Instagram's embed.js
 *  into the real player. There is no API-free way to get a bare iframe src — the blockquote
 *  is the officially supported route, same as the "Embed" button on instagram.com itself.
 *
 *  A client component because embed.js only scans the DOM once, on its own load — a visitor
 *  who clicks between two episode pages (client-side nav, no full reload) needs the already-
 *  loaded script told to look again, which plain HTML in a server component can't trigger. */
export default function IgEmbed({ permalink }: { permalink: string }) {
  useEffect(() => {
    if (window.instgrm) {
      window.instgrm.Embeds.process();
      return;
    }
    const s = document.createElement("script");
    s.src = "https://www.instagram.com/embed.js";
    s.async = true;
    document.body.appendChild(s);
  }, [permalink]);

  return (
    <blockquote
      className="instagram-media"
      data-instgrm-permalink={permalink}
      data-instgrm-version="14"
      style={{ margin: "0 auto", width: "100%" }}
    />
  );
}
