"use client";

import { useState } from "react";

/** The whole point is that it gets pasted, so copying has to be one tap and has to
 *  confirm it worked. The textarea stays so it can be selected by hand if the
 *  clipboard is blocked. */
export default function Copy({ text }: { text: string }) {
  const [done, setDone] = useState(false);
  return (
    <>
      <div className="actions" style={{ marginBottom: 12 }}>
        <button
          className="btn"
          onClick={async () => {
            try {
              await navigator.clipboard.writeText(text);
              setDone(true);
              setTimeout(() => setDone(false), 2500);
            } catch {
              setDone(false);
            }
          }}
        >
          {done ? "Copied ✓" : "Copy the whole thing"}
        </button>
      </div>
      <pre className="promptbox">{text}</pre>
    </>
  );
}
