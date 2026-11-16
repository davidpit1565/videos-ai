# Graphify: product check for the reference reel DfatglrzjiV (@auraguy.ai, 6.11.2026)

Checked 15.11.2026 by web search and by reading pages. Nothing was installed or run. We have NOT tested Graphify ourselves, so every token figure below comes from someone else.

## 1. Is it real?
- **Yes.** The repo is `Graphify-Labs/graphify`: https://github.com/Graphify-Labs/graphify. The old URL `github.com/safishamsi/graphify` shows the same page, which looks like a transfer from the original author Safi Shamsi. That the transfer happened is UNCONFIRMED: the GitHub API was not reachable from this session.
- **Stars:** the repo page reads 148.2k on 15.11.2026, with 14.2k forks. The reel's "140,000+" was true when we checked.
- **Licence:** the repo has two licence files, LICENSE (Apache-2.0) and LICENSE-MIT. The open-source CLI is free. There is also a paid product, Graphify Cloud.
- **How it works:** it parses code locally with tree-sitter and writes `GRAPH_REPORT.md`. Its Claude Code setup adds lines to CLAUDE.md and installs a PreToolUse hook that points Claude's searches at the graph. Sources: README, https://claudelog.com/claude-code-mcps/graphify.

## 2. What the README says about token savings
- **The current README has no "70x" and no "71.5x".** The only token claim is about the paid Cloud product: "Cut agent token spend by 80%." and "80% fewer tokens". The README gives no method for that number.
- The README's benchmarks measure recall and QA accuracy (LOCOMO, LongMemEval-S, ERPNext key-fact coverage 70.8% -> 82.0%, n=6). None of them measures tokens. BENCHMARKS.md (https://github.com/Graphify-Labs/graphify/blob/v8/BENCHMARKS.md) reports "about 140K tokens per query" on ERPNext but gives no grep/read baseline to compare against.
- **Where "71.5x" comes from:** an earlier worked example by the project: about 52 files (Karpathy repos plus papers and images), tokens per query compared with reading every raw file. Second-hand sources describe it: https://pyshine.com/Graphify-AI-Knowledge-Graph-From-Any-Codebase/, https://themenonlab.blog/blog/graphify-knowledge-graph-claude-code-karpathy. It is a best case against a baseline that loads every file, and Claude Code does not work that way.
- Graphify's own blog, dated 29.10.2026 and updated 6.11.2026 (https://graphify.com/blog/reduce-claude-code-token-usage), says: "How much any tool saves depends on the repo, the kind of questions you ask and how it's set up." It ends with: "So the honest answer is to measure your own repo."

## 3. Setup today (README)
```
uv tool install graphifyy      # or pipx install graphifyy / pip install graphifyy
graphify install               # registers the skill with the assistant it finds
```
- The package is spelled `graphifyy`, with a double y. Inside Claude Code the command is `/graphify .`.
- So the reel's "one install command, then type /graphify" is close but not exact: it takes two shell commands, and `/graphify` takes a folder argument.

## 4. Claude plans (https://claude.com/pricing, read 15.11.2026)
| Plan | Price | Usage |
|---|---|---|
| Pro | $20/month billed monthly ($17/month billed yearly) | 1x. Claude Code is included |
| Max | $100/month | "5x Pro usage" every 5 hours and every week |
| Ultra | $200/month | "10x Pro usage" weekly, no 5-hour limit |

For "$20 does what $100 did" to be true, Graphify would have to cut usage by about 5x on every kind of work. The independent tests below do not show that.

## 5. Independent tests and criticism
- **FastAPI, 11 questions (Constantin Ponfick):** files inspected fell 14.6%, but input tokens ROSE 49.5% and cost rose 9.5%. Reported on Graphify's own blog, linked above.
- **One YouTube run (The Gray Cat):** about 18% fewer tokens ($5.16 -> $4.29), but the run was slower and 2 of 3 graph queries missed. Same source.
- **GitHub issue #985:** reports Claude Code alone using the same or fewer tokens on common queries. Still open according to Graphify's blog.
- **A 10-question test on the browser-use repo:** 113k tokens with Graphify against 120k without, about 7% less. We only have this from a search summary (https://levelup.gitconnected.com/everyone-says-graphify-cut-their-ai-coding-bill-70x-752fc1e1f0d9). The article returned 403, so this is UNCONFIRMED.
- **RoboRhythms, 28.5.2026 (https://www.roborhythms.com/graphify-review/):** the 71x is "1,700 input tokens versus 123,000 naive" on one benchmark. The reviewer's "honest range" of 6.8x-49x was compiled from other people's sources, not measured by them. The review also reports that the PreToolUse hook silently stops working on Claude Code v2.1.117+ (issue #578), that the graph goes stale, and that one tool can return about 33k tokens. Whether #578 has since been fixed is UNCONFIRMED.
- **Review roundup (https://codeconductor.ai/blog/graphify-review/, updated 15.10.2026):** on a mid-sized project the reviewer found Claude Code's own navigation good enough without Graphify, and in one test the generated report was blank.
- **Reddit:** reactions are split. The top comment on the launch thread warns about duplicate nodes and stale assumptions. We know this only from a search summary; the thread itself was not opened, so it is UNCONFIRMED.

## Claim / verdict / source
| Reel claim | Verdict | Source |
|---|---|---|
| Graphify is real, free, open source | TRUE (Apache-2.0 + MIT files; a paid Cloud also exists) | github.com/Graphify-Labs/graphify |
| 140,000+ GitHub stars | TRUE today (148.2k) | repo page, 15.11.2026 |
| Builds a knowledge graph of your codebase | TRUE | README |
| The next session uses the graph instead of re-reading files | PARTLY: through a hook plus a CLAUDE.md note. The hook was reported broken on Claude Code 2.1.117+ (status today UNCONFIRMED) | README; roborhythms |
| "Up to 70x fewer tokens" | MISLEADING: one best-case example against a "read every file" baseline; not in today's README; independent runs show 7-18% savings or MORE tokens | graphify.com blog; roborhythms |
| "$20 plan does what $100 plan used to" | FALSE as a general claim: Max is 5x Pro, and no independent test shows a steady 5x cut | claude.com/pricing |
| "One install command, then /graphify" | ROUGHLY: two commands (`uv tool install graphifyy`, `graphify install`), then `/graphify .` | README |
| People burn their plan "in two days" | UNCONFIRMED anecdote | none |

## What we may truthfully say in a reel
- Graphify is a free, open-source tool with about 148,000 GitHub stars (as of 15.11.2026). It maps your code once so Claude Code can look things up instead of re-reading files.
- Its best published example used about 70 times fewer tokens. Independent tests on real projects found much less, and one found more. Graphify's own blog says: measure your own repo.
- The setup is two terminal commands, then `/graphify .`. Show it on the site page.
- Better format: our own before/after test on a real repo, with token counts measured by us.

## What we must not say
- "70x fewer tokens", or "up to 70x", as what a viewer will get.
- "$20 does what $100 did", or "you won't need Max".
- "One command and you're done", or anything implying the hook always works.
- Any token saving we did not measure ourselves, presented as our result.
