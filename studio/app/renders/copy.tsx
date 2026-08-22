"use client";

import { useState } from "react";

/** The caption, with one button. Retyping a 1500-character caption on a phone is how a
 *  wrong caption gets posted, and the clipboard write can fail on iOS without a gesture —
 *  so this is a real button and it says what happened either way. */
export default function Copy({ text }: { text: string }) {
  const [state, setState] = useState<"idle" | "done" | "failed">("idle");

  return (
    <div className="cap">
      <div className="caphead">
        <b>קפשן</b>
        <button
          className="btn small"
          onClick={async () => {
            try {
              await navigator.clipboard.writeText(text);
              setState("done");
            } catch {
              setState("failed");
            }
          }}
        >
          {state === "done" ? "הועתק" : state === "failed" ? "סמן והעתק ידנית" : "העתק"}
        </button>
        <span className="num">{text.length} תווים</span>
      </div>
      <pre>{text}</pre>
    </div>
  );
}
