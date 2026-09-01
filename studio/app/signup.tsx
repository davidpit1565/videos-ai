"use client";
import { useState } from "react";

/** The form is the business. It posts to our own endpoint, which stores the address
 *  before it tries Beehiiv, so a provider problem cannot swallow a subscriber. Every
 *  state is visible: nothing here ever says "thanks" without a stored row behind it. */
export default function Signup({
  source = "site",
  episode,
}: {
  source?: string;
  /** Which episode page this form is rendered on, when it's an episode page — the
   *  one fact that lets a later signup be tied back to what actually caused it,
   *  instead of every episode's signups landing in one indistinguishable "episode"
   *  bucket. See subsAttributed in lib/types.ts for why this matters. */
  episode?: number;
}) {
  const [email, setEmail] = useState("");
  const [state, setState] = useState<"idle" | "sending" | "done" | "error">("idle");
  const [msg, setMsg] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (state === "sending") return;
    setState("sending");
    setMsg("");
    try {
      const r = await fetch("/api/subscribe", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ email, source, episode }),
      });
      const j = (await r.json()) as { ok?: boolean; error?: string; created?: boolean };
      if (j.ok) {
        setState("done");
        setMsg(j.created ? "You're on the list." : "You were already on the list.");
      } else {
        setState("error");
        setMsg(j.error ?? "Something went wrong.");
      }
    } catch {
      setState("error");
      setMsg("No connection. Try again in a moment.");
    }
  }

  if (state === "done") {
    return (
      <p className="signed" role="status">
        <b>{msg}</b> One email a week. Unsubscribe in one click.
      </p>
    );
  }

  return (
    <form className="signup" onSubmit={submit} noValidate>
      <input
        type="email"
        inputMode="email"
        autoComplete="email"
        required
        placeholder="you@email.com"
        aria-label="Email address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      {/* never disabled on an empty field: a greyed-out primary button on first paint
          reads as a broken page. The address is validated on submit, and again server
          side, which is where validation has to live anyway. */}
      <button type="submit" disabled={state === "sending"}>
        {state === "sending" ? "Adding…" : "Get the setups"}
      </button>
      {state === "error" ? (
        <p className="err" role="alert">
          {msg}
        </p>
      ) : (
        <p className="fine">Free. One email a week. Nothing is sold to anyone.</p>
      )}
    </form>
  );
}
