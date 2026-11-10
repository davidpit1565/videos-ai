# Graphify research, 2026-11-10 (for the @duncanrogoff reference reel)

Method: Exa web search/fetch only. I did NOT read the source code, install anything, or run anything. I did not open the reel itself.

## 1. What it is
- FACT: open-source "/graphify" skill + CLI that turns a codebase (plus docs, PDFs, images) into a queryable knowledge graph for Claude Code, Cursor, Codex, Gemini CLI and others. Code is parsed locally with tree-sitter. https://github.com/Graphify-Labs/graphify
- FACT: repo (moved from safishamsi/graphify), Apache-2.0, about 145k stars, 13.9k forks, 1,637 open issues, created 2026-04-03, top contributor safishamsi. Same URL.
- FACT: PyPI package is `graphifyy` (double y), v0.9.105; the project says other graphify* packages are not affiliated. https://pypi.org/project/graphifyy/
- FACT: the company also sells "Graphify Cloud" (14-day trial, hosted MCP) at graphify.com. The open-source repo is the funnel for it.
- Maintained: FACT the commits page showed commits dated 12 Oct 2026 as the newest (https://github.com/Graphify-Labs/graphify/commits/v8). UNCONFIRMED whether anything is newer; PyPI is at 0.9.105, higher than the 0.9.88 on that page, so the page was probably cached. Check live before filming.

## 2. The "70x" number
- FACT: README says "71.5x fewer tokens per query" on one corpus: 52 files (Karpathy repos + 5 papers + 4 images), about 123k tokens read naively vs about 1.7k per graph query. The README's own table shows 5.4x on a 4-file corpus and about 1x on a 6-file one. https://github.com/safishamsi/graphify/blob/main/README.md
- FACT: the baseline is "read every raw file", an estimate, not a measured Claude session. Graphify's own docs say so: "an estimate, not a measurement of a real Claude session" https://docs.graphify.com/cookbooks/claude-code-monorepo and "The naive side is an estimate" https://docs.graphify.com/open-source/features/token-benchmark
- FACT: independent checks do not support 70x for real work. A reviewer found no external reproduction (https://blog.stackademic.com/does-graphify-cut-claude-code-costs-the-token-math-a-skeptic-should-run-first-fdfc989d3bce). A video test showed 120k vs 113k tokens (under 8%) on 10 questions (https://www.smorster.org/research/bkhps04qggc/, a third-party summary of a video, not the video). A blog benchmark with 180 trials per agent found the old hook used MORE tokens than plain grep with Claude (ratio 1.17) and 0.95 with Codex (https://srijansriv.com/graphify-benchmark-results).
- FACT: Graphify's own comparison page admits users found Claude Code alone used the same or fewer tokens (issues #580, #985), and a 1,500-file monorepo test was parity at 30,000 tokens. It claims better accuracy instead (70.8% to 82.0% on 6 questions). https://graphify.com/vs/claude-code
- Verdict: the number is the author's own, from a favourable baseline. The reel's "70x fewer tokens" is not a supported claim for normal Claude Code use. The caption's honest part ("won't fix messy architecture") is fine.

## 3. What it needs and touches
- FACT (project docs): Python 3.10+, `uv tool install graphifyy`, `graphify install` registers a skill and edits `~/.claude/CLAUDE.md`; `graphify claude install` adds a CLAUDE.md section and PreToolUse hooks that fire before search/Read calls. https://pypi.org/project/graphifyy/ , https://graphify.com/integrations/claude-code
- FACT (project docs): code pass is offline; docs/PDFs/images go to your configured model (your Claude session or an API key you set); the project states no telemetry. It writes a query log to `~/.cache/graphify-queries.log` (opt out with GRAPHIFY_QUERY_LOG_DISABLE=1). Local `--transport http` MCP is opt-in. https://github.com/Graphify-Labs/graphify/security/policy
- FACT (third party): StrideNote read part of the source (9 of 65 files) and monitored sockets during a code-only run: no remote connections, no analytics vendors. https://stridenote.net/graphify-local-model-test/ (July 2026, older version).
- Risks to note: the hook rewrites how Claude Code behaves in your project; one fixed bug made it read a 12k-25k token report before every search. Typosquat risk with the double-y name. The semantic pass sends doc content to a model provider.
- NOT READ by me: the source code, the installer, the hooks' scripts, the current version's network calls. I cannot call it safe; I can only say the project claims and one third party found no telemetry.

## 4. Episode worth, faceless version
- Worth it as a debunk/test, not as a promo: a huge, fast-growing tool, and "70x" is a number the audience will repeat. Funnel: TOP/MID. Duplicate check against topics-covered.txt not done in this task.
- Faceless version is possible only as a real test. We would run (in a sandbox, not the studio repo): the same 5-10 questions on one public repo with Claude Code alone vs with Graphify installed, a fresh session each, and read the real token totals from Claude Code's own usage output (`/cost` or the session usage), plus the build time. Also run `graphify benchmark` to show the "estimate" next to the real number. Cannot promise the result; the evidence above suggests a small saving, so the honest hook is "70x? We measured." and the on-screen proof is two real token totals.
- Do not copy the 70x line, and do not give the install steps without a live re-check of the current README.
