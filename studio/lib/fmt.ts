/** Formatting helpers. A missing number is shown as an em dash, never as a zero. */
export const n = (v: number | null | undefined) =>
  v == null ? "—" : v.toLocaleString("en-US");

export const pct = (v: number | null | undefined, digits = 1) =>
  v == null ? "—" : (v * 100).toFixed(digits) + "%";

export const eur = (v: number | null | undefined) =>
  v == null ? "—" : "€" + Math.round(v).toLocaleString("en-US");

export const today = () => new Date().toISOString().slice(0, 10);
