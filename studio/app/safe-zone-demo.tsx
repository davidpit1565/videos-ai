"use client";

import { useState } from "react";

/** A real frame from a real shipped episode (reel-05, the one this exact fact is about),
 *  not a mockup — dragging the slider shows what Instagram's own interface actually covers
 *  on a 1080x1920 video: 14% off the top, 35% off the bottom, 6% off each side. Those
 *  numbers are Meta's own published safe-area spec for 9:16 (see CLAUDE.md's frame-layout
 *  section) — export/safe_check.js enforces the same box on every episode before it ships.
 *  This is the one thing on the site that's interactive instead of read, because "the
 *  bottom third of your video is covered by the app" is exactly the kind of claim nobody
 *  believes until they see it drawn on a real frame. */
export default function SafeZoneDemo() {
  const [reveal, setReveal] = useState(0); // 0..100

  return (
    <div className="szdemo">
      <div className="szframe">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/site/safe-zone-frame.jpg" alt="A real frame from one of our episodes" />
        <div className="szmask szmask-top" style={{ opacity: reveal / 100 }}>
          <span>Instagram covers this — 14%</span>
        </div>
        <div className="szmask szmask-bottom" style={{ opacity: reveal / 100 }}>
          <span>Username, caption, buttons — 35%</span>
        </div>
        <div className="szmask szmask-left" style={{ opacity: reveal / 100 }} />
        <div className="szmask szmask-right" style={{ opacity: reveal / 100 }} />
      </div>
      <div className="szcontrol">
        <label htmlFor="szslider">Drag to see what Instagram covers on your video</label>
        <input
          id="szslider"
          type="range"
          min={0}
          max={100}
          value={reveal}
          onChange={(e) => setReveal(Number(e.target.value))}
        />
        <p className="szcaption">
          This is a real frame from one of our own episodes. The shaded parts are covered
          by Instagram&apos;s own interface — the username, caption, audio label and
          buttons at the bottom, the header at the top. Text placed there is hidden behind
          the app, not behind us. Every episode we publish is checked against this exact
          box before it ships.
        </p>
      </div>
    </div>
  );
}
