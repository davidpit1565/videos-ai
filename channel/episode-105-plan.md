# Episode 105 plan — "Claude Ultra free for 6 months" (ref reel Df5C8OFvMxo), VIRAL-MAX version (18.11.2026)

Publish mode: REGULAR (default; ask David before publishing)
Funnel: TOP. Status: PLAN ONLY. David approves, then builds in the new session. Do not publish or merge.
Source facts and what is NOT verified: `channel/ref-2026-11-18-Df5C8OFvMxo.md` (read it first).

## Why this plan scores higher than the first draft (my judgement, labels, not measurements)
First draft: HOOK 78 / VIRALITY 70 / OVERALL 72. This version: HOOK 90 / VIRALITY 86 / OVERALL 88, predicted views about 2,000-6,000 (ASSUMPTION). Five levers:
1. WIDER AUDIENCE: Anthropic's own page says "Don't quite fit? Apply anyway and tell us about it." That line is the twist: it turns "only maintainers" into "you can still try", so non-maintainers have a stake too.
2. SELF-CHECK MECHANIC: the viewer checks themselves against 5 criteria while watching (a reason to stay, rewatch and comment "I qualify / I do not").
3. ONE NUMBER NOBODY KNOWS: criterion 5 is an "OpenSSF criticality score 0.4". Gets the stage as the surprise, with a "check yours in 10 seconds" step ONLY if the real tool is verified live first.
4. SAVEABLE CARD: the five criteria as one screenshot-able card near the end.
5. NAMED PERSON: "Send this to the friend who codes."

## Verify live BEFORE writing the script (CLAUDE.md rule), in this order
a. Re-open https://claude.com/contact-sales/claude-for-oss (maxAge 0): plan name, criteria, "apply anyway" line, any deadline or cap.
b. Read https://www.anthropic.com/claude-for-oss-terms: card needed or not, term length, anything about stacking with a paid plan, end date.
c. OpenSSF criticality score: find the real tool/page and the real way to check a repo; if no simple way is confirmed, drop the "check yours" step and keep the card.
d. Price: show "$200" ONLY if claude.com pricing shows it the same day; otherwise say "the top plan".
e. Duplicate check: grep `channel/topics-covered.txt` (none found 18.11; repeat).

## Hook options (statement, not a question, about 6 words, surprise in the first 3 words; blind-reader test on frame 0)
- A: "Anthropic gives away Claude's top plan." (subject at once; frame 0: real Claude logo + "6 MONTHS FREE" + struck price if verified)
- B: "Claude's top plan. Free. Check yours." 
- C: "Free Claude, six months. Most can't claim." only if "most" is dropped or proven: use "Not everyone can claim it."
Pick by two blind agents (what is this about / would you stop). Hook is visual first: logo + 3 words max, no code, no long text.

## Beat list (about 26-30 s, Miki + GSAP, light base, real logos, one idea per screen) — what is NEW in each beat
1 (0-2.5 s) HOOK on real Anthropic page / Claude logo: free top plan. NEW: the offer.
2 (2.5-5) Promise line: "Check in thirty seconds if you get it." NEW: a task for the viewer; value 1 lands by 6-8 s.
3 (5-9) Criteria 1-2 as tick cards (packages others depend on; foundation committer). NEW: the first two bars, high.
4 (9-13) Criteria 3-4 (100 merged pull requests in other people's repos; 20 outside contributors). NEW: bars get reachable. Spoken loop line, TRUE: "The last one is the one nobody knows."
5 (13-18) Criterion 5, the surprise: OpenSSF criticality score 0.4. NEW: a number most people never checked. (Check-yours step only if verified.)
6 (18-23) TWIST from Anthropic's own words: "Don't quite fit? Apply anyway and tell us." NEW: hope for non-qualifiers. A person reads each application (say only what the page/terms support).
7 (23-27) Saveable card with all five + where to apply. Closing: "The setup's in the link in bio." then "Want the next one? Follow." (no promise of tomorrow).
Loop: last frame returns to frame 0 (logo + FREE) so it rewatches.

## Build-up check (CLAUDE.md 15.11): stake opened in the hook ("do I get it?") gets closer each beat; no beat restates; no explanation-only stretch over 2.5 s between 4 and 15 s; reveal staged (criterion 5 last, twist after). Blind reader marks the first beat where they would scroll: write the answer here.

## Rules this build must follow (all from CLAUDE.md)
Miki style + adopted GSAP skills (`.claude/skills/gsap-*`), checklist `channel/miki-style-checklist-2026-11-16.md`; whole safe box filled (x 108-972 for key text, 864 right limit in the 55-85% band); alive picture, nothing still over 2.5 s, smooth easing; hook visual first, max 3 lines of text; present tense, plain words; real logos only (Claude, GitHub, OpenSSF if named), icon only, no caption under it; no code on screen; voice: avoid R clusters (say "Anthropic" as "the company" or keep on screen only), "free" must sound clear, product names one word, hook flows (--gap 0.06 --long 0.15 --max-speedup 1.45), one TTS render at a time under `flock /tmp/tts.lock`; run script_lint, voice_doctor, check_accent, voice_quality; music from the real library, log in `channel/music-notes.md`; gate `export/check_hf.sh` (last arg 1.0); watch the render twice; caption under 2,200 chars (`wc -m`), no `<` `>` in YouTube text; setup guide entry in `studio/lib/articles.ts` (6 steps, English labels only, `export/check_setup_guide.py` passes); `studio/public/reels/reel-105.approval.txt`; score labels logged in `channel/score-calibration.md`. Review as ONE playable Artifact page (video as data URI under 16 MB). Merge only once, batched; verify deploy by file size. Phone notification when ready.

## Honest limit (one line, not to be repeated to David): the topic's audience is developers, so sends are the weak number; the twist and the card are how this plan fights that.

---
## LIVE VERIFICATION, 18.11.2026 (Firecrawl, maxAge 0) — overrides the assumptions above
- Page name is "Claude Ultra" (not "top plan"): "6 months of Claude Ultra on us". Say "Claude Ultra". NO price shown on either page: do not show "$200" or any price.
- Criteria on the page (any one): maintainers 500+ dependent repos / 100+ dependent packages / 200,000+ monthly downloads; core contributor of a recognized foundation or language project; 100+ merged PRs into repos you don't own in 12 months; a repo with 20+ external contributors with merged PRs in 12 months; a repo with OpenSSF criticality score 0.4+. "Don't quite fit? If you maintain something the ecosystem quietly depends on, apply anyway and tell us about it." (real twist, but see terms: it is the "Ecosystem Impact Track", discretionary).
- Terms (anthropic.com/claude-for-oss-terms): cap 10,000 recipients, Anthropic can close any time; ALSO required for everyone: 18+, GitHub account 2+ years old, public open-source activity in the last 90 days, a project under an OSI-approved license; one subscription per person; review is rolling and Anthropic contacts ONLY approved applicants; selection is discretionary, meeting a bar is no promise; fake/inflated metrics = disqualified; 6 months from activation (activate within 90 days); paid plan pauses and resumes after; overage charges possible; not transferable.
- So the honest hook/twist: "free Claude Ultra for open-source people" + "no qualifying number? you can still apply" — NOT "anyone". The GENERAL requirements (2-year-old GitHub, active in last 90 days, OSI license) go on the saveable card.
- OpenSSF criticality score: real, but it is a command-line tool from ossf/criticality_score (github.com/ossf/criticality_score), not a 10-second web check. DROP the "check yours" step. Criterion 5 stays as the surprise number; say only what it is ("a score for how many projects depend on yours").
- Duplicate check 18.11: no match in topics-covered.txt (only "open-sourced our own video pipeline", unrelated).
