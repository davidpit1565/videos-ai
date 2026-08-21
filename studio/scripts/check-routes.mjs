/** Every route under app/ must be classified in lib/routes.ts as site or studio.
 *
 *  Three times now a page was added and one of the places that needed to know about it was
 *  not updated: /api/subscribe answered 401 to every visitor, /prompts and /search
 *  redirected to the PIN gate, and then /prompts and /search rendered inside the studio's
 *  Hebrew tab bar. Each time the page existed and worked; what was missing was a line in a
 *  list, and nothing failed until a person opened it in production.
 *
 *  So the lists are now one list, and this refuses to build without a decision about every
 *  route the filesystem actually has. It fails closed: an unclassified route is an error,
 *  not a default. */
import { readdirSync, statSync, readFileSync } from "node:fs";
import { join } from "node:path";

const APP = new URL("../app/", import.meta.url).pathname;
const ROUTES = new URL("../lib/routes.ts", import.meta.url).pathname;

/** the route paths the filesystem defines, with dynamic segments given a sample value so
 *  the same matcher the app uses can be applied to them */
function walk(dir, base = "") {
  const out = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (!statSync(full).isDirectory()) {
      if (/^(page|route)\.tsx?$/.test(name)) out.push(base || "/");
      continue;
    }
    // (groups) do not appear in the URL; @slots and _private folders are not routes
    if (name.startsWith("_") || name.startsWith("@")) continue;
    const seg = name.startsWith("(") && name.endsWith(")") ? "" : "/" + name;
    out.push(...walk(full, base + seg));
  }
  return out;
}

const src = readFileSync(ROUTES, "utf8");
function list(name) {
  const m = src.match(new RegExp(`export const ${name} = \\[([^\\]]*)\\]`, "s"));
  if (!m) throw new Error(`lib/routes.ts no longer exports ${name}`);
  return [...m[1].matchAll(/"([^"]+)"/g)].map((x) => x[1]);
}
const SITE = list("SITE"), STUDIO = list("STUDIO"), CRON = list("CRON");

// the matcher, kept identical to lib/routes.ts by the test below rather than by hope
const under = (path, l) => l.some((p) =>
  p === "/" ? path === "/" : p.endsWith("-") ? path.startsWith(p) : path === p || path.startsWith(p + "/"));

const sample = (r) => r.replace(/\[\[?\.\.\.[^\]]+\]\]?/g, "x").replace(/\[[^\]]+\]/g, "x");

const routes = [...new Set(walk(APP))].sort();
const unclassified = routes.filter((r) => {
  const s = sample(r);
  return !under(s, SITE) && !under(s, STUDIO) && !under(s, CRON);
});
const both = routes.filter((r) => {
  const s = sample(r);
  return [SITE, STUDIO, CRON].filter((l) => under(s, l)).length > 1;
});

if (unclassified.length || both.length) {
  console.error("\nlib/routes.ts does not account for every route:\n");
  for (const r of unclassified)
    console.error(`  unclassified  ${r}   → add it to SITE (public) or STUDIO (private)`);
  for (const r of both)
    console.error(`  in both lists ${r}   → a route cannot be public and private`);
  console.error("\nA page that is not in either list loads for nobody, or loads wearing the");
  console.error("wrong chrome. That has reached production three times; this is why.\n");
  process.exit(1);
}
console.log(`routes: ${routes.length} classified · site ${SITE.length} · studio ${STUDIO.length} · cron ${CRON.length}`);
