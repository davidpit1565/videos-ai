# Agency Agents: fact check of reel DfVPw9LTJEo (@auraguy.ai)

Checked 15.11.2026. Research only: GitHub pages and raw files read, nothing installed or run.
Reel: 4.11.2026, 3,992 likes, 1,735 comments (comment-to-DM bait "AGENCY"). Caption claims: "Claude Code can now run your whole business with 280 free AI employees", 160,000+ stars, an orchestrator that "runs the whole project, hands each task to the right specialist, and checks every step", "one install drops all 280 agents onto your laptop".

## The repo

- Real: https://github.com/msitarzewski/agency-agents (owner: msitarzewski). Name in the README: "The Agency".
- Stars today: **168.5k**, forks 27.3k (GitHub page, read 15.11.2026). Licence **MIT**. 864 commits on `main`; latest commits 7-9 Nov 2026 (https://github.com/msitarzewski/agency-agents/commits/main). Actively maintained.
- Earlier summaries quoted 147k stars, so it grows fast. Whether the stars are organic was not checked (UNCONFIRMED either way).

## What it actually is

- A library of **Markdown files**. Each is one "agent" = a role prompt with YAML frontmatter (`name`, `description`, `color`, `emoji`, `vibe`) and a long personality/process text. No code runs inside an agent. In Claude Code these become **subagents** (`~/.claude/agents/*.md`).
- **How many:** the README's own Stats section says "230+ Specialized Agents"; the README tables link **283** agent files across 18 divisions (counted from the raw README: engineering 66, specialized 59, marketing 37, game-dev 21, gis 13, security 12, design 10, sales 9, testing 9, paid-media 7, project-management 7, academic 6, product 6, spatial-computing 6, support 6, finance 5, healthcare 3, research 1). Flavio Copes counted 298 in October 2026. So "about 280" is roughly right; the exact on-disk count is UNCONFIRMED (GitHub API was not reachable from this session).
- **Orchestrator: exists** — `specialized/agents-orchestrator.md`. It is a *prompt* describing a **software-development** pipeline (PM → ArchitectUX → Dev ↔ QA loop → integration test), with lines like "Please spawn a project-manager-senior agent...". It is not a business manager, and it does nothing on its own: Claude has to be asked to use it, and it only works as well as the model follows the instructions.
- Sales/marketing agents exist (e.g. `sales/sales-outbound-strategist.md`: "designs multi-channel prospecting sequences"). They write text and plans. They **cannot send an email, make a call or post** unless the user's Claude Code already has a tool/connector for that.
- Also a separate desktop app (Homebrew cask `msitarzewski/agency-agents/agency-agents`) that installs agents for you. A compiled app; not inspected.

## Install: what the script really does

Read from https://raw.githubusercontent.com/msitarzewski/agency-agents/main/scripts/install.sh (1,801 lines):
- Command from the README: clone the repo, then `./scripts/install.sh --tool claude-code`. Or by hand: `cp engineering/*.md ~/.claude/agents/`.
- For Claude Code it **copies `.md` files from every division folder into `~/.claude/agents/`** (or `$CLAUDE_CONFIG_DIR/agents`, or `--path <dir>`). Bare `./scripts/install.sh` installs **every team to every detected tool** (Copilot, Gemini, Cursor, Codex, ...), interactive in a terminal.
- No `curl`/`wget`/`http` calls, no `sudo`, no edits to `settings.json`, no hooks found in the script (grep of the full text). It may run the repo's own `scripts/convert.sh` for other tools (not read). `cp` **overwrites** a same-named file already in `~/.claude/agents/`.
- Useful flags: `--dry-run` (print the plan, write nothing), `--agent <id>` (only that agent), `--division <name>`, `--list agents`.
- Agents installed in `~/.claude/agents/` are active in **all** projects. Claude Code delegates **automatically** by each agent's `description` (Claude Code docs, https://code.claude.com/docs/en/sub-agents).

## Claim / verdict / source

| Claim in the reel | Verdict | Source |
|---|---|---|
| Real free GitHub project | TRUE (MIT, free) | GitHub repo page |
| 160,000+ stars | TRUE (168.5k on 15.11.2026) | GitHub repo page |
| 280 specialists | ROUGHLY TRUE: README says 230+, its tables link 283, a reviewer counted 298; exact count UNCONFIRMED | raw README; flaviocopes.com/agency-agents |
| "AI employees" / "a whole company inside Claude" | MISLEADING: they are role prompts (Markdown), not workers that act on their own | agent files; legost.in summary ("a role guides the assistant; it does not make it an expert") |
| Orchestrator hands work out and checks each step | PARTLY: an orchestrator prompt exists and describes a Dev-QA loop for software projects; whether it reliably does so is untested by anyone we found | specialized/agents-orchestrator.md |
| "Runs your whole business" | FALSE / HYPE: README says "A complete AI agency at your fingertips"; no claim of autonomous business running; agents produce drafts, not actions | README; Flavio Copes ("the workflow is manual, step by step") |
| Writes cold emails, sales-call prep, proposals, social, support | TRUE as drafts/text; sending/posting needs other tools | sales/*, marketing/*, support/* files |
| "One install drops all 280 agents on your laptop" | TRUE (and that is the risky default; one agent can be installed alone) | install.sh |
| Results better than plain Claude | UNCONFIRMED: README says "battle-tested in production"; no benchmark found; Flavio's review shows none | README; flaviocopes.com |

No independent critical review or Reddit thread was found (one search); that absence is noted, not a verdict.

## What we may truthfully say in a reel

- "There is a free GitHub project with about 280 ready-made AI role prompts for Claude Code — sales, marketing, design, engineering. It has over 160,000 stars."
- "Each one is a text file that tells Claude how to act as that specialist."
- "One of them is an 'orchestrator' that tells Claude to hand a project step by step to the others and check each step."
- "You can install just one instead of all of them." (and show the exact steps)
- Anything about quality only after **we** test it, and say it was our test.

## What we must not say

- "Runs your whole business", "AI employees", "replace hiring" — they are prompts that draft text.
- "It sends your cold emails / handles your support" — not without other tools we have not set up.
- "Tested/battle-tested" — the repo says so; no evidence found.
- An exact agent count as fact ("exactly 280") — say "about 280" or "over 200".
- "Safe to install everything" — see below.

## Security and usefulness for David's Claude Code

- The two agent files read (orchestrator, outbound strategist) have **no `tools:` line**. Per Claude Code docs, a subagent without `tools` **inherits every tool** the session has (Bash, file edits, MCP connectors such as Gmail, GitHub, Vercel). A third-party prompt with full tools is a prompt-injection surface: a future update to the repo could change the text, and with `--link` (symlink) updates flow in silently.
- 280 descriptions in `~/.claude/agents` load into every session and invite automatic delegation; this costs context (exact amount UNCONFIRMED) and can route work to a generic persona instead of our own skills.
- In a cloud session `~/.claude` is not kept between sessions; agents that should persist go in the project folder `.claude/agents/` (committed).
- **Usefulness for us:** low to medium. We already have our own skills for hooks, captions, marketing and explain-steps. One or two agents (e.g. "Reality Checker" for QA) might be worth a test; the full 280 is not.

### If David wants to try ONE agent (safe path)

1. Open https://github.com/msitarzewski/agency-agents in the browser and pick one agent from the README table (for example `testing/testing-reality-checker.md`).
2. Click the file, then click **Raw**. Read the whole text: look for anything that asks to run commands, open links, send data or change settings.
3. Tell Claude: "Create `.claude/agents/reality-checker.md` with this text" and paste it (or ask Claude to fetch that one raw URL and show it to you first).
4. Ask Claude to add one line under `description:` in the top block: `tools: Read, Grep, Glob` — so the agent can read but cannot run commands, edit files or use connectors.
5. Use it by name: "Use the reality-checker agent to review X." Check the result yourself.
6. Optional: if it is not useful, ask Claude to delete that one file.

Never: run `./scripts/install.sh` with no flags, use `--link`, or install the Homebrew desktop app without reading what it does. If the script is ever used, run `./scripts/install.sh --tool claude-code --agent <id> --dry-run` first and read the plan.

## Sources

- Repo: https://github.com/msitarzewski/agency-agents ; commits: https://github.com/msitarzewski/agency-agents/commits/main
- Install script: https://raw.githubusercontent.com/msitarzewski/agency-agents/main/scripts/install.sh
- README (raw): https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md ; divisions.json (same path)
- Orchestrator: https://raw.githubusercontent.com/msitarzewski/agency-agents/main/specialized/agents-orchestrator.md
- Claude Code subagents docs: https://code.claude.com/docs/en/sub-agents
- Flavio Copes guide (updated 4.10.2026): https://flaviocopes.com/agency-agents/
- legost.in summary: https://legost.in/en/open-source/agency-agents
