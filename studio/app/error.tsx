"use client";
import { useEffect } from "react";

/** Next's default crash screen says "a client-side exception has occurred" and nothing
 *  else — no message, no line, nothing to act on. This replaces it with the actual
 *  error, and reports it to the server so it lands in the runtime logs too. */
export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    fetch("/api/clientlog", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        message: error.message,
        stack: error.stack,
        digest: error.digest,
        path: typeof location === "undefined" ? "" : location.pathname,
      }),
    }).catch(() => {
      /* reporting a crash must never cause one */
    });
  }, [error]);

  return (
    <div className="crash">
      <h1>משהו נשבר בדף הזה</h1>
      <p>זו השגיאה עצמה, ולא הודעה כללית. היא נרשמה גם בשרת.</p>
      <pre>{error.message || "אין הודעה"}</pre>
      {error.digest ? <p className="dg">digest: {error.digest}</p> : null}
      <button onClick={reset}>לנסות שוב</button>
      <p className="dg">
        אם זה חוזר — הדף לא תקין, לא אתה. תשלח לי את השורה שבמסגרת.
      </p>
    </div>
  );
}
