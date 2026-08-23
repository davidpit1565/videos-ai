/** He asked, directly: he cannot tell whether the studio he's looking at is the current
 *  deploy or a stale one, without pinging Claude to check. The reel list already showed a
 *  timestamp, but that's each video's own ship time, not "is this page itself current."
 *
 *  Writes the real commit this build was made from, at build time, so the page can show it
 *  without guessing. Vercel sets VERCEL_GIT_COMMIT_SHA automatically; a local build falls
 *  back to git directly so `npm run build` still works outside Vercel. */
import { execSync } from "node:child_process";
import { writeFileSync } from "node:fs";

function commitSha() {
  if (process.env.VERCEL_GIT_COMMIT_SHA) return process.env.VERCEL_GIT_COMMIT_SHA;
  try {
    return execSync("git rev-parse HEAD", { cwd: new URL("..", import.meta.url) }).toString().trim();
  } catch {
    return null;
  }
}

const sha = commitSha();
const info = {
  sha,
  shortSha: sha ? sha.slice(0, 7) : null,
  builtAt: new Date().toISOString(),
};

writeFileSync(new URL("../public/build-info.json", import.meta.url), JSON.stringify(info, null, 1) + "\n");
console.log(`build-info.json -> ${info.shortSha ?? "unknown"} @ ${info.builtAt}`);
