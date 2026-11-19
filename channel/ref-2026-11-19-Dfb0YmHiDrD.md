# Reference reel Dfb0YmHiDrD (seen 19.11.2026): "This Claude skill took me from 0 to 38,000 followers" (@jayantcreates.ai style account "Jayant")
Publish mode: not decided. Funnel: TOP/MID. Not built; waiting for David's go.

## Facts (downloaded 19.11 after one retry; transcript by faster-whisper, frames viewed)
- Account "Jayant", posted 7.11.2026, 52 s, 1080x1920, 878 likes, 2,321 comments (the comments are the "comment SETUP and I DM you the skill" mechanic, not organic interest). Views not exposed.
- Spoken script: "This Claude skill helped me get from 0 to 38,000 followers and 8 million views in just 4 months ... Everybody is creating videos with Claude, but the people who are winning follow a system with 5 content pillars and the 5th is the most effective ... 1 Connect it to your Instagram so Claude sees your real numbers; 2 Content research: what is going viral in your niche and why; 3 Hooks skill: 10 openings ranked by what stops the scroll; 4 Humanizer: strips what sounds like AI, in your tone; 5 Trial Reels: post 5 versions to people who do not follow you, only the winner goes on your main page. Comment SETUP."
- Picture: dark blue blueprint grid, orange accent (Claude orange), a counter 3,389 to 38,000 followers and 1,827,150 views at the start, Greek-temple pillars 01-05 that fill one by one (pillar 5 orange "MOST EFFECTIVE"), a small drawn UI per pillar (Instagram connect, bar chart with median line, ten ranked hooks, a struck-out AI paragraph, A-E trial thumbnails), word-by-word caption in the lower third, a final "comment SETUP" DM mock-up.
- UNVERIFIED and inconsistent: "0 to 38,000 followers and 8 million views in 4 months" (the on-screen counter ends at 1,827,150 views). No proof shown, a course/skill is sold through the DM. We repeat none of it.

## Why it spreads (HYPOTHESIS, no per-second data)
A huge promise in the first 3 s (numbers counting up), a simple frame (five pillars, one skill = the whole system), a "secret" ranked last ("the 5th is the most effective, many people miss it") that keeps people to 46 s, a saveable order of steps, and the comment-for-DM bait that inflates comments. The audience (people who want to grow) is large and eager.

## Copy / not copy
- Copy structurally: "one system, five steps" with the best step saved for last, a progress element (pillars filling), a saveable card.
- Not copy: the account's claims, the comment-DM bait, their blueprint look/graphics, their voice or face. Our look stays Miki + GSAP.

## Which skills WE already have (verified in `.claude/skills/`)
| their pillar | ours |
|---|---|
| 1 Connect to Instagram | the studio reads our real Instagram numbers (`/api/track`, `/api/state`) and I read them with the PIN; `ig-audit` and `ig-profile` skills |
| 2 Content research | `ig-viral` (outlier multiple = views / that account's own median), the AI hot radar, our reference-reel analysis |
| 3 Hooks, 10 ranked | `viral-hook-lab`, `ig-reel` (hook formulas, `hookscore.py`), `channel/hooks-guide.md`. HONEST: our own test showed `hookscore.py` does NOT predict our views (Spearman -0.23, n=8): use as a checklist, not a ranking |
| 4 Humanizer | `ig-human` (strips AI wording), `remove-ai-marks` skill, our plain-language rules |
| 5 Trial reels, 5 versions | we ALREADY do it: ep106 five versions (posted 19.11), `video/ep106/make_variant.sh`, the studio `trial: MANUAL` API |
Missing and worth building: (a) a competitor-profile reader (the Instagram research tool David's friend promised), (b) a small "trial-test ledger" skill that records each version, posting time, 24/72 h numbers and names the winner (today: a table in `channel/experiments.md`), (c) packaging `make_variant.sh` as a reusable skill (everything we build becomes an episode).

## OUR version: topic verdict and faceless beat-by-beat
TOPIC: "I posted one video five times with five different openings. Here is the winner." It uses OUR OWN real data (the ep106 test, 24 h readings 20.11 at 20:45 and 72 h on 22.11 Belgium time), it is a contest (guess which hook won), and it is AI + growth, which fits the channel. Do not build before the numbers exist; without our own numbers it would only be the reel's claims again. Duplicate check (`topics-covered.txt`, 19.11): no hit for hook testing or trial reels (line 47 is a subscription trial, unrelated).
Draft beats (about 30-35 s, Miki + GSAP, real Instagram UI recreated as drawn UI, real logos): 1 hook: five thumbnails A-E fan out, "One video. Five openings. Which one won?" (no numbers until they are real); 2 promise: "I posted all five to people who do not follow me"; 3 the five hook lines appear one by one with a guess marker (comment A-E); 4 loop line TRUE of what follows: "One got X times more views" only with the real ratio; 5 reveal the winner last; 6 what the loser says about hooks (one real lesson, labelled a hypothesis); 7 the setup card (our real method: same video, only the first 3 seconds change, trial on, auto-share off) + "The setup's in the link in bio." + the closing line David chooses.
Scores (judgement, ASSUMPTION for views): HOOK 80, VIRALITY 78, OVERALL 78, predicted 800-3,000 views; depends on the real result being interesting.
Funnel: TOP (contest/guess) with MID value (a method creators can copy).

## Next step needing David
Go/no-go on this episode idea after the 22.11 numbers, and whether to build the "trial-test ledger" skill now (small).
