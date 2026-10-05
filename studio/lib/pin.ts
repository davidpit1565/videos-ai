/** The studio PIN gate used to store the raw STUDIO_PIN value itself as the cookie —
 *  anything that captured that cookie (a proxy log, a support screenshot, a future edit
 *  that drops httpOnly/secure by accident) handed over the actual secret, not just a
 *  session token. Hashing it here means the cookie is useless on its own: recovering the
 *  real PIN from this digest needs a SHA-256 preimage, not a copy-paste. Works unchanged
 *  in both the Edge middleware and the Node API route — Web Crypto's `crypto.subtle` is
 *  global in both runtimes on Vercel. */
export async function hashPin(pin: string): Promise<string> {
  const data = new TextEncoder().encode(pin);
  const digest = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}
