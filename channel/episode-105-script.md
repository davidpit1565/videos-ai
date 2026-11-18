# Episode 105 — Claude Ultra free for open-source people (script v1, 18.11.2026)

Publish mode: REGULAR (David's call; ask before publishing)
Funnel: TOP. Status: SCRIPT ONLY, not built. Plan: `channel/episode-105-plan.md` (live verification block at its end). Internal folder for the build: `video/ep105/`.
Hook chosen by David (18.11.2026): "Claude Ultra now for free! Here's how." (blind reader earlier ranked short hooks; "Claude Ultra. Free. Six months." won among the four tested).

## Facts used (all verified live 18.11.2026, claude.com/contact-sales/claude-for-oss, anthropic.com/claude-for-oss-terms, claude.com/pricing)
- Ultra = $200 per month (pricing page). Six months = $1,200 at list price. Only for approved people.
- Cap: up to 10,000 approved recipients; Anthropic can close the program any time.
- Any one criterion: 500+ dependent repos / 100+ dependent packages / 200,000+ monthly downloads; listed committer/maintainer of a recognized foundation or language project; 100+ pull requests merged into repos you do not own in 12 months; a repo with 20+ external contributors with merged PRs in 12 months; a repo with OpenSSF criticality score 0.4+.
- Everyone also needs: GitHub account 2+ years old, public open-source activity in the last 90 days, a project under an OSI-approved license, 18+.
- "Apply anyway" line is on the page (Ecosystem Impact Track, discretionary). Anthropic contacts only approved applicants.
- NOT claimed anywhere: that everyone gets it, a review time, a person reading each form.

## Spoken lines (English, present tense, plain; "Anthropic" kept off the audio, say "the company")
1. HOOK: "Claude Ultra, now for free! Here's how."
2. PROMISE: "Thirty seconds. See if you get it."
3. PRICE: "Normally, two hundred dollars a month."
4. "One: lots of projects depend on your code. Two: you help run a big open-source project."
5. "Three: a hundred of your changes got accepted into other people's projects. Four: twenty outsiders helped build yours." 
6. LOOP LINE (true, paid by line 7): "The last one, almost nobody knows."
7. "Five: a score called OpenSSF. Point four or higher. It shows how much other software relies on your project."
8. TWIST: "Not on the list? The company says apply anyway, and explain why your project matters."
9. CARD: "Also: a GitHub account two years old, active this season, and an open license. Only ten thousand spots."
10. VALUE: "Six months free. That's twelve hundred dollars."
11. SEND: "Send this to the friend who codes."
12. "The setup's in the link in bio."
13. "Want the next one? Follow."

## Beat list (about 28 s) — what is NEW in each beat (build-up check)
| # | time | picture (Miki + GSAP, light base, real logos, no code) | NEW here |
|---|---|---|---|
| 1 | 0-2.5 | Real Claude logo, $200 struck through to $0, "6 MONTHS", GitHub logo small. Max 3 text lines. | the offer + the number |
| 2 | 2.5-4.5 | Checklist outline appears, five empty boxes | a task for the viewer |
| 3 | 4.5-6 | Price tag $200/month crossed | what it normally costs |
| 4 | 6-10 | Boxes 1-2 tick, real project logos (Linux, Python, Node) as proof of "big project" | first two bars, high |
| 5 | 10-14 | Boxes 3-4 tick, numbers 100 and 20 count up | bars get reachable |
| 6 | 14-15.5 | Box 5 hidden, a lock/"?" | stake: the one nobody knows |
| 7 | 15.5-19.5 | Box 5 opens: OpenSSF 0.4 meter | the surprise number |
| 8 | 19.5-23 | "Not on the list? Apply anyway" lines, hope beat | twist: non-qualifiers can try |
| 9 | 23-26.5 | One saveable card: the 5 + the 3 general requirements + "10,000 spots" | what to screenshot |
| 10 | 26.5-30 | Loop: back to the Claude logo + FREE (frame 0); send line, setup line, follow line | reason to rewatch and send |

Build-up check: stake ("do I get it?") opened in line 1-2, closer every beat; beat 6 is a withheld reveal; twist (8) comes after; no explanation-only stretch over 2.5 s between 4 and 15 s (counters and ticks move); every line pulls.

## Concept checklist (virality gate, 4.11.2026) — judgement, not measurement
1. Something specific to the viewer: "see if YOU get it" — partial (only for coders).
2. Curiosity gap only the video closes: the fifth criterion — yes.
3. Saveable card: the five + general requirements — yes.
4. Named person: "the friend who codes" — yes.
5. Reason to watch twice: loop to frame 0, card to screenshot — yes.
6. Checkable in 30 s: the real page, link in bio — yes.
Scores (labels): HOOK 89, VIRALITY 86, OVERALL 88, PREDICTED VIEWS 2,000-6,000 (ASSUMPTION). Log real 48 h / 72 h numbers in `channel/score-calibration.md`.

## Blind reader log (CLAUDE.md first-second rule)
- Earlier rounds (18.11): on screen Claude + GitHub logos, big "FREE · 6 MONTHS" — readers understood "free premium Claude for coders" and would stop; "Ultra" and "open source" were unclear to a non-user. Fix: line 3 gives the price, line 4 names open source. 
- TODO on the first rendered frame: fresh agent sees ONLY frame 0 + the first spoken second, answers "what is it about / would you stop". Write the answer here.

## Build checklist (from the plan, unchanged)
Miki style + `.claude/skills/gsap-*`; `channel/miki-style-checklist-2026-11-16.md`; whole safe box, key text x 108-972 and right edge <= 864 in the 55-85% band; nothing still over 2.5 s; real logos only (Claude, GitHub, OpenSSF, project logos), icon only; no code on screen; voice: `audio/script_lint.py --cues`, `--gap 0.06 --long 0.15 --max-speedup 1.45`, one TTS render at a time under `flock /tmp/tts.lock`, voice_doctor, check_accent, voice_quality; "Claude Ultra" one name (Whisper gap under 0.12 s); music from the real library, log in `channel/music-notes.md`; `export/check_hf.sh`; watch the render twice; caption under 2,200 chars (`wc -m`), no `<` `>` in YouTube text; setup guide entry in `studio/lib/articles.ts` (6 steps, English only) and `export/check_setup_guide.py`; `studio/public/reels/reel-105.approval.txt`; review as ONE playable Artifact; merge once, batched; verify deploy by file size; phone notification when ready.

## Setup guide for the site page /e/105 (draft, English labels only)
1. Open claude.com/contact-sales/claude-for-oss.
2. Check you meet one criterion on the page (list above).
3. Check the general requirements: GitHub account 2+ years old, public activity in the last 90 days, an open-source license.
4. Sign in with GitHub in the form and fill in your project's link and how it is used.
5. Not on the list? Write in "Tell us about the project's reach" why the ecosystem depends on it, and apply anyway.
6. Wait for an email: only approved people hear back. Activate the link within 90 days.
