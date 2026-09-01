# agent-reach (hardened fork)

A hardened version of [Panniantong/Agent-Reach](https://github.com/Panniantong/agent-reach)'s
Claude Code skill, pinned to commit `06c202b03400a7d31886bf4399213706da1a0324`
(2026-08-25). Same 15-platform internet access, same commands, same
credentials model — one thing removed.

## What was removed, and why

An independent security audit ([Oathe.ai](https://oathe.ai/report/Panniantong/Agent-Reach),
score 78/100, "CAUTION") flagged a HIGH-severity issue, which I confirmed
directly in the source at the pinned commit: the upstream skill instructs
the agent to fetch a live document from `raw.githubusercontent.com` and
execute whatever is in it, at three points:

1. **`SKILL.md` standing rule 5** — after a multi-platform task, if a new
   version exists, suggest the user paste a message that makes the agent
   fetch `docs/update.md` live and follow it.
2. **`SKILL.md`'s "Configure a channel" section** — whenever a platform
   needs setup (a common, ordinary occurrence), fetch `docs/install.md`
   live from GitHub and follow it.
3. **`docs/install.md`'s own "Step 5: daily monitoring"** — sets up a
   recurring cron job whose task text includes the same "paste this to
   fetch update.md" instruction.

Because that document lives on a branch (`main`) the user has no control
over, anyone who can edit it — the maintainer, or anyone who compromises
their GitHub account — can change what the agent does *after* the user
already reviewed and approved the original code, with no corresponding code
change to review. That's a live remote-instruction-injection vector, not a
theoretical one.

## What this fork does instead

- **`SKILL.md`**: rule 5 now only reports a version *number* — no fetch, no
  follow. The "configure a channel" section points to a **vendored, local**
  setup guide instead of a live URL.
- **`references/channel-setup.md`**: a full English copy of upstream's
  `docs/install.md` — every platform, every command, every security caveat
  (secondary-account recommendation, cookie boundaries, no-auto-login rules)
  preserved verbatim in meaning — with the "fetch this file live" framing
  removed, since it's already included locally.
- **Everything else is untouched**: the entire routing table, all
  zero-config commands, all login-backed platform commands, and all seven
  `references/*.md` files (`search.md`, `social.md`, `career.md`, `dev.md`,
  `web.md`, `video.md`, `finance.md`) are copied verbatim from the pinned
  commit — I checked each one and none of them contain the live-fetch
  pattern, only this one.

**Nothing about the actual internet-access functionality changed.** Every
platform Agent Reach supports (Twitter/X, Reddit, YouTube, GitHub, Bilibili,
XiaoHongShu, Facebook, Instagram, LinkedIn, V2EX, Xueqiu, Xiaoyuzhou,
RSS, general web) works exactly the same way it did upstream.

## Installing it

```bash
pipx install "git+https://github.com/Panniantong/agent-reach.git@06c202b03400a7d31886bf4399213706da1a0324"
agent-reach install --env=auto
```

Then copy this fork's `SKILL.md` and `references/` into your skills
directory (e.g. `.claude/skills/agent-reach/` for Claude Code) — not
upstream's own `SKILL.md`.

## What updating safely looks like

Because this fork intentionally has no live-update mechanism, getting a
newer upstream version means: pull the new commit, **re-run the same
grep check** below against it, and re-vendor by hand if it's still clean.
Never re-enable the live-fetch pattern to "simplify" future updates — that
convenience is exactly the vulnerability.

```bash
grep -rn "raw.githubusercontent" .        # must show nothing except explanatory prose like this README
grep -rn "archive/main.zip\|@main\b" .    # must show nothing — always pin to a commit SHA
```

## Remaining risk this fork does NOT remove

- **Platform Terms of Service.** Twitter/X, Reddit, and most other
  platforms this tool touches prohibit scraping in their own ToS. That's a
  fact about the platforms, not something a code change can fix. Using this
  on a real account — especially a business account — carries real
  account-suspension risk, independent of the security fix above. Consider
  a secondary/dedicated account per the setup guide's own recommendation.
- **Credential accumulation.** Real session cookies for whichever platforms
  you configure still get stored locally (`~/.agent-reach/`, `~/.config/`).
  That part of the design is unchanged — it's how the tool works, not a bug
  this fork introduced or could remove without breaking the feature.
- **External binary execution** (yt-dlp, ffmpeg, bili-cli, rdt-cli, git) —
  no malicious behavior found in any of them, but each is still a real
  dependency with its own update/security surface, upstream's or ours.

## Sources

- [Panniantong/Agent-Reach](https://github.com/Panniantong/agent-reach) — upstream repo
- [Is Panniantong/Agent-Reach safe? — Oathe.ai security audit](https://oathe.ai/report/Panniantong/Agent-Reach)
- Vendored at commit `06c202b03400a7d31886bf4399213706da1a0324` (2026-08-25, "fix(readme): use permanent Star History token")
