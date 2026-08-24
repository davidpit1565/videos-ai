"use client";

import { useState } from "react";

/** Copy for pasting straight in; download for the file itself. The download builds a
 *  blob URL client-side — there's no server storage to keep in sync with lib/skills.ts,
 *  the text on screen and the file downloaded are provably the same string. */
export default function CopyOrDownload({ text, filename }: { text: string; filename: string }) {
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
        <button
          className="btn ghost"
          onClick={() => {
            const blob = new Blob([text], { type: "text/markdown" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
          }}
        >
          Download {filename}
        </button>
      </div>
      <pre className="promptbox">{text}</pre>
    </>
  );
}
