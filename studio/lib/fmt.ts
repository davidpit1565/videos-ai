/** Formatting helpers. A missing number is shown as an em dash, never as a zero. */
export const n = (v: number | null | undefined) =>
  v == null ? "—" : v.toLocaleString("en-US");

export const pct = (v: number | null | undefined, digits = 1) =>
  v == null ? "—" : (v * 100).toFixed(digits) + "%";

export const eur = (v: number | null | undefined) =>
  v == null ? "—" : "€" + Math.round(v).toLocaleString("en-US");

export const today = () => new Date().toISOString().slice(0, 10);

/** Every timestamp in the studio is stored in UTC, and every place that showed one was
 *  slicing that UTC string directly — correct to store, wrong to read: he's in Israel
 *  (UTC+2/+3), so every date/time on screen sat 2-3 hours behind the real moment. This
 *  converts to his local time for display; storage stays UTC. */
export const localDT = (iso: string) => {
  const d = new Date(iso);
  if (isNaN(d.getTime())) return iso.slice(0, 16).replace("T", " ");
  return d.toLocaleString("sv-SE", { timeZone: "Asia/Jerusalem", hour12: false }).slice(0, 16);
};
