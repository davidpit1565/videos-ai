# Channel setup guide (vendored, not live-fetched)

This is a reviewed, English copy of upstream's `docs/install.md`, frozen at
commit `06c202b03400a7d31886bf4399213706da1a0324`. The one thing removed is
upstream's own instruction to fetch this document live from
`raw.githubusercontent.com` and follow it — that live-fetch pattern is the
security issue this fork exists to remove. Everything else — every command,
every platform, every caveat — is preserved.

## Boundaries (apply to every step below)

- **Do not** run commands with `sudo` unless the user explicitly approved.
- **Do not** modify system files outside `~/.agent-reach/`.
- **Do not** install packages not listed in this guide.
- **Do not** disable firewalls, security settings, or system protections.
- **Do not** clone repos, create files, or run commands inside the agent
  workspace / working directory.
- If something requires elevated permissions, **tell the user** what's
  needed and let them decide.

## Directory rules

All Agent Reach files go in dedicated directories — **never in the agent
workspace**:

| Purpose | Directory | Example |
|---|---|---|
| Config & tokens | `~/.agent-reach/` | `~/.agent-reach/config.json` |
| Upstream tool repos | `~/.agent-reach/tools/` | `~/.agent-reach/tools/xiaoyuzhou/` |
| Temporary files | `/tmp/` | `/tmp/yt-dlp-output/` |
| Skills | wherever this skill is installed | `SKILL.md` |

**Why?** Cloning repos or creating files in the workspace pollutes the
user's project directory and can break their agent over time.

## Step 1: Install the basics

**Install the package pinned to the reviewed commit — not `main`:**

```bash
pipx install "git+https://github.com/Panniantong/agent-reach.git@06c202b03400a7d31886bf4399213706da1a0324"
agent-reach install --env=auto               # Read-only check (default)
# After the user explicitly approves system changes:
agent-reach install --env=auto --system
```

If Python is Homebrew-managed or you hit PEP 668
(`externally-managed-environment`), use a virtual environment instead:

```bash
python3 -m venv ~/.agent-reach-venv
source ~/.agent-reach-venv/bin/activate
pip install "git+https://github.com/Panniantong/agent-reach.git@06c202b03400a7d31886bf4399213706da1a0324"
agent-reach install --env=auto
agent-reach install --env=auto --system   # after explicit approval
```

> **Windows / Microsoft Store Python alias:** if `python3 --version` opens
> the Microsoft Store, or `where python3` points into
> `...\AppData\Local\Microsoft\WindowsApps\`, that `python3` is a Store
> alias, not a real install. Use the Python Launcher `py -3` instead:
> ```powershell
> py -3 -m venv $env:USERPROFILE\.agent-reach-venv
> $env:USERPROFILE\.agent-reach-venv\Scripts\Activate.ps1
> python -m pip install "git+https://github.com/Panniantong/agent-reach.git@06c202b03400a7d31886bf4399213706da1a0324"
> agent-reach install --env=auto
> ```

The default command checks core infrastructure (gh CLI, Node.js, mcporter,
Exa search, yt-dlp config) without changing the host. With explicit
`--system` approval it installs/configures the missing pieces and activates
these zero-config channels: **Web (Jina Reader), YouTube, GitHub, RSS, Exa
Search, V2EX, Bilibili (basic).**

**Install modes:**

```bash
agent-reach install --env=auto             # Check only; safe default
agent-reach install --env=auto --safe      # Same check-only behavior (compatibility)
agent-reach install --env=auto --system    # Explicitly allow external/system installs
agent-reach install --env=auto --dry-run   # Preview what --system would do
```

## Step 2: Ask the user which optional channels they want

Present this list and ask which they need:

- 🌟 **OpenCLI** (recommended for desktop) — one install unlocks Reddit /
  Facebook / Instagram / Bilibili subtitles / Twitter fallback, and serves
  as the XiaoHongShu desktop backend. XiaoHongShu only ever uses a Chrome
  session the user already has and explicitly controls.
- 🐦 **Twitter/X** — search tweets, read timelines (needs a login cookie)
- 📈 **Xueqiu** — stock quotes, trending posts (needs a login cookie)
- 🎙️ **Xiaoyuzhou Podcast** — audio-to-text (needs a free Groq key)
- 📕 **XiaoHongShu** — search, read, comment (OpenCLI uses an existing
  session; MCP/legacy tools use Cookie-Editor)
- 📖 **Reddit** — search and read posts (login required: desktop OpenCLI or
  `rdt-cli` + cookie)
- 📘 **Facebook** — search, pages, feed, group list (desktop via OpenCLI,
  reuses the existing Chrome login)
- 📷 **Instagram** — user search, profile, a user's recent posts, Explore
  (desktop via OpenCLI, reuses the existing Chrome login)
- 📺 **Bilibili (full)** — trending, rankings, search, video details
  (`bili-cli`, no login needed)
- 💼 **LinkedIn** — profile and job search

Based on the user's choice, run:

```bash
agent-reach install --env=auto --system --channels=opencli,xiaohongshu   # Desktop user chose XHS
agent-reach install --env=auto --system --channels=facebook,instagram    # Desktop Meta channels
agent-reach install --env=auto --system --channels=all                   # User approved everything
```

Supported channel names: `opencli`, `twitter`, `xiaoyuzhou`, `xueqiu`,
`xiaohongshu`, `reddit`, `facebook`, `instagram`, `bilibili`, `linkedin`,
`all`

## Step 3: Fix what's broken

Run `agent-reach doctor` and check the output. Try to get as many channels
to ✅ as possible. If something failed during install or shows ❌/⚠️,
diagnose and try to fix it — but stay within the boundaries above. Only ask
the user when you genuinely need their input (credentials, permissions,
etc.).

## Step 4: Configure things that need user input

Some channels need credentials only the user can provide.

> **Security tip:** for platforms needing cookies or browser sessions
> (Twitter, XiaoHongShu, Reddit, Facebook, Instagram), recommend a
> **dedicated/secondary account** rather than the user's main one.
> Cookie/browser-session auth carries two risks:
> 1. **Account ban** — platforms may detect non-browser API calls and
>    restrict or ban the account.
> 2. **Credential exposure** — cookies grant full account access; a
>    secondary account limits the blast radius if credentials are ever
>    compromised.

**Cookie / login state — general approach:** for platforms needing a cookie
(Twitter, Xueqiu, etc.), the simplest and most reliable path is the
Cookie-Editor extension: the user logs into the platform in their own
browser, installs [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm),
clicks the extension → Export → Header String, and sends that string to the
agent. Twitter only accepts a value the user explicitly exported this way.
Agent Reach never performs XiaoHongShu login on the user's behalf and never
reads XiaoHongShu's browser cookies directly — its OpenCLI backend only uses
a Chrome session the user already has and explicitly controls; with no
existing session, use the Cookie-Editor export instead. Xueqiu and Bilibili
can be imported explicitly per platform, e.g.
`agent-reach configure --from-browser chrome --platform xueqiu` — this
command does not scan or save any other platform's cookies.

**Twitter search & posting:**
> "To unlock Twitter search, I need your Twitter cookies. Install the
> Cookie-Editor Chrome extension, go to x.com/twitter.com, click the
> extension → Export → Header String, and paste it to me."

```bash
agent-reach configure twitter-cookies
```

This saves `twitter_auth_token` and `twitter_ct0` for Agent Reach's own
`doctor` check. `doctor` does not run the upstream `twitter status` command
live and does not modify the current shell. Before calling `twitter`
directly, set these explicitly in that process's environment:

```bash
export TWITTER_AUTH_TOKEN="..."
export TWITTER_CT0="..."
twitter search "query" -n 10
```

> **Proxy note (for networks that block Twitter/Reddit, e.g. mainland
> China):** `twitter-cli` and `rdt-cli` are Python tools and read a proxy
> from environment variables.
> 1. Confirm the user has a proxy configured: `agent-reach configure proxy`
>    (hidden input)
> 2. Set the environment variables: `export HTTP_PROXY="..." HTTPS_PROXY="..."`
> 3. Agent Reach handles the rest automatically — no further user action
>    needed
> 4. If the user reports "fetch failed", see `troubleshooting.md` in the
>    upstream repo's `docs/` folder.

**Reddit (login is mandatory — no zero-config path):** Reddit's anonymous
endpoints are blocked and the official API needs manual approval. Desktop
users should prefer OpenCLI (works once reddit.com is logged into in the
browser); server/legacy users use `rdt-cli`:

```bash
# PyPI lags behind; install from GitHub pinned to the exact version the code expects
pipx install 'git+https://github.com/public-clis/rdt-cli.git@5e4fb3720d5c174e976cd425ccc3b879d52cac66'
rdt login   # auto-extracts a browser cookie; on a headless server, follow doctor's prompt to set the cookie by hand
```

> Accessing Reddit from mainland China needs a proxy; if a server IP gets
> rate-limited, a residential proxy (e.g. https://webshare.io, about
> $1/month) can help: `agent-reach configure proxy`

**XiaoHongShu (multiple backends, pick by environment):**

> **Auth boundary:** Agent Reach never logs the user into XiaoHongShu and
> never reads the browser's XiaoHongShu cookies. OpenCLI only uses a Chrome
> session the user already has and explicitly controls;
> `agent-reach configure xhs-cookies` does not inject a cookie into OpenCLI
> or Chrome. With no existing session, don't auto-login — use a manual
> Cookie-Editor export instead, configured for xiaohongshu-mcp or a legacy
> tool:
> ```bash
> agent-reach configure xhs-cookies
> ```
> This explicit command saves/imports only the xiaohongshu.com-scoped
> cookies the user provides — confirm the cookie names/scope first. Cookies
> from any other domain are ignored.

**Desktop (OpenCLI recommended):**
```bash
agent-reach install --system --channels opencli
```
After install, the one manual step Chrome's own security model requires (no
way to automate this):
1. Open https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk
2. Click "Add to Chrome"
3. Run `opencli doctor` to verify (should show "Extension: connected")

If XiaoHongShu shows `AUTH_REQUIRED` and the user has no existing session,
don't auto-login on their behalf — use the Cookie-Editor / legacy-tool route
above instead.

**Server / no desktop (xiaohongshu-mcp):**
1. Download the matching binary from
   https://github.com/xpzouying/xiaohongshu-mcp/releases into
   `~/.agent-reach/tools/`
2. Start the service (first run auto-downloads a ~150MB headless browser —
   this takes a while)
3. Import cookies via the Cookie-Editor flow above
4. Connect it: `mcporter config add xiaohongshu http://localhost:18060/mcp --scope home`
5. Always call it with `--timeout 120000`

**Legacy users (xhs-cli):** an already-installed `xhs-cli` keeps working as
a fallback backend (upstream stopped updating it as of March 2026 — don't
newly install it); it still authenticates via the Cookie-Editor flow above.

**Facebook / Instagram (desktop OpenCLI):** both platforms go through
OpenCLI, reusing the user's own Chrome login — no password is stored and no
Meta Graph API approval flow is involved. Not recommended for
server/headless environments.

```bash
agent-reach install --system --channels facebook,instagram
```

After install:
1. Confirm Chrome has the OpenCLI extension and `opencli doctor` passes
2. Log into facebook.com / instagram.com in Chrome
3. The agent calls it directly:
   ```bash
   opencli facebook search "query" -f yaml
   opencli facebook profile zuck -f yaml
   opencli facebook groups -f yaml
   opencli instagram search "query" -f yaml     # user search
   opencli instagram profile nasa -f yaml
   opencli instagram user nasa -f yaml          # a specific user's recent posts
   ```

Facebook Groups currently only promises the list of groups/recent activity
visible to the logged-in user — not arbitrary group posts/comments via API.
Instagram's `search` is a user search, not a site-wide keyword search of
posts; on a 429 or login error, have the user re-log into Chrome and slow
down request frequency.

**Xueqiu (stock quotes + trending posts):** needs a logged-in cookie. Have
the user log into xueqiu.com in Chrome, then run:

```bash
agent-reach configure --from-browser chrome --platform xueqiu
```

Only the minimum cookies Xueqiu needs are read and saved — no other
platform's cookies are touched.

**Xiaoyuzhou Podcast (Groq Whisper transcription):** the transcription
script is installed automatically with Agent Reach — the user only needs to
provide a free Groq API key:

```bash
agent-reach configure groq-key
```

> **Getting a free Groq API key (no credit card, ~30 seconds):**
> 1. Open https://console.groq.com
> 2. Sign in with Google/GitHub (or register)
> 3. Left menu → API Keys → Create API Key
> 4. Copy the key (starts with `gsk_`) and send it to the agent

**Usage:** the user sends a Xiaoyuzhou episode link; the agent runs:
```bash
bash ~/.agent-reach/tools/xiaoyuzhou/transcribe.sh https://www.xiaoyuzhoufm.com/episode/xxxxx
```
This downloads the audio → transcodes/chunks it → transcribes with Groq
Whisper → outputs a full transcript.

**Free-tier limits:** roughly 2 hours of audio per hour (7200 seconds),
auto-resets after 15 minutes once exceeded — plenty for normal listening.
Quality is high (Whisper large-v3) but doesn't distinguish speakers;
episodes over 2 hours are best processed in batches.

**LinkedIn (optional — mcp-server-linkedin):** basic content is readable via
Jina Reader. Full features (profile details, people/job search) need
`mcp-server-linkedin`.

**Setup (stdio recommended):** install `uv` first (also provides `uvx`):
https://docs.astral.sh/uv/getting-started/installation/

```bash
mcporter config add linkedin --command uvx --arg mcp-server-linkedin==4.23.1 --env UV_HTTP_TIMEOUT=300 --scope home
```

Pin an exact version rather than `@latest` — `uvx` will otherwise fetch
whatever the maintainer just published, silently, on every run. Check
[PyPI](https://pypi.org/project/mcp-server-linkedin/) for the current
release before installing, and bump the pinned version deliberately when
you want to update, the same way `references/channel-setup.md`'s own
"What updating safely looks like" section handles this fork's main
package.

**First login (needs a visible browser):**
```bash
uvx mcp-server-linkedin==4.23.1 --login
```
A browser window opens for the user to log into LinkedIn manually; the
session is saved to `~/.linkedin-mcp/profile/`. On a headless server, run
this same login command inside a visible desktop session (e.g. VNC).

See https://github.com/stickerdaniel/linkedin-mcp-server for details.

## Step 5: Final check

Run `agent-reach doctor` once more and report the results to the user.

## Ongoing health checks (optional)

`agent-reach watch` and `agent-reach doctor` are safe to run periodically
(they only report channel health) — set up a recurring check if useful. **Do
not** wire a recurring task to suggest or perform a live update fetch;
report a new version as a one-line note per this skill's standing rule 5
instead.

## Quick reference

| Command | What it does |
|---|---|
| `agent-reach install --env=auto` | Read-only dependency and channel check (default) |
| `agent-reach install --env=auto --system` | Explicitly install/configure core external tools |
| `agent-reach install --env=auto --system --channels=twitter,xiaohongshu` | Install approved optional channels |
| `agent-reach install --env=auto --system --channels=all` | Install everything after explicit approval |
| `agent-reach install --env=auto --safe` | Compatibility alias for the safe default |
| `agent-reach install --env=auto --dry-run` | Preview what would be done |
| `agent-reach doctor` | Show channel status |
| `agent-reach watch` | Quick health + update check (for scheduled tasks) |
| `agent-reach check-update` | Check for new versions (reports a version number only) |
| `agent-reach configure twitter-cookies` | Save Twitter cookies via hidden input; direct calls still need explicit env vars |
| `agent-reach configure proxy` | Save a proxy address via hidden input; not an automatic unlock switch |
| `agent-reach configure groq-key` | Configure the Xiaoyuzhou transcription key |

After installation, use upstream tools directly:

| Platform | Upstream tool | Example |
|---|---|---|
| Twitter/X | `twitter` (fallback `opencli`) | Set `TWITTER_AUTH_TOKEN`/`TWITTER_CT0`, then `twitter search "query" -n 10` |
| YouTube | `yt-dlp` | `yt-dlp --dump-json URL` |
| Bilibili | `bili` (subtitles via `opencli`) | `bili search "query" --type video` / `opencli bilibili subtitle BVxxx` |
| Reddit | `opencli` (fallback `rdt`) | `opencli reddit search "query" -f yaml` / `rdt read POST_ID` |
| Facebook | `opencli` | `opencli facebook search "query" -f yaml` |
| Instagram | `opencli` | `opencli instagram user nasa -f yaml` |
| GitHub | `gh` | `gh search repos "query"` |
| Web | `curl` + Jina | `curl -s "https://r.jina.ai/URL"` |
| Exa Search | `mcporter` | `mcporter call exa.web_search_exa query="..." numResults=5` |
| XiaoHongShu | `opencli` (server: `mcporter`) | `opencli xiaohongshu search "query" -f yaml` |
| Xiaoyuzhou Podcast | `transcribe.sh` | `bash ~/.agent-reach/tools/xiaoyuzhou/transcribe.sh <URL>` |
| LinkedIn | `mcporter` | `mcporter call linkedin.get_person_profile linkedin_username="..."` |
| RSS | `feedparser` | `python3 -c "import feedparser; ..."` |

> For multi-backend platforms, trust `agent-reach doctor --json`'s
> `active_backend` field over any of the above.
