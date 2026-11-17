# Episode 103 plan: the Replica skill (Q4), written 17.11.2026
Publish mode: REGULAR (default; David has not said otherwise). Status: PLAN. Not built. Needs David's own test run (below).
Numbering: 101 free alternatives, 102 LinkedIn skills (both built, in branch ep86-build, not merged), 103 = this.

## Reference reel, re-downloaded and re-read 17.11.2026 (DfQDKhNzXtm, @auraguy.ai, 2.11.2026)
Real numbers today (yt-dlp metadata): 3,277 likes, 2,763 comments (16.11: 3,247 / 2,722, so +30 / +41 in a day). Views/plays: NOT exposed to us (view_count empty). Do not estimate views from likes. Comment to like ratio 0.84: the "comment CLONE for the setup" call to action is doing the work, so the audience is asking for the thing.
Same account, same template, real likes: Instagram skills reel 28,148; Day Trader 13,258; Replica 3,277; LinkedIn 481. Reading (hypothesis, one account): for this creator the SUBJECT moved the numbers far more than the template. The two big ones are a huge-audience victim (Instagram) and money plus odds (trading). Replica is mid (money you pay every month). LinkedIn, the one we just built, is the weakest of the four.
Description structure copied in our own words (see 102's caption): hook line, plain promise, what each skill does, how to install, one CTA.

## What the repo is (read from a local clone 17.11.2026, nothing executed)
Jakeschincariol/replica-skill, MIT, v1.0 commit 3.10.2026, 11 skills (recon, architect, design, build, backend, test, diff, entrepreneur, brand, launch, deploy) plus six small Python tools (contrast.py, imgdiff.py, parity.py, reviews.py, sweep.py, listing.py): file reads/writes only, no network calls, no keys (grep, not a full audit). README: rebuilds features and flows clean-room, never code/logo/copy; backend and deploy skills never type a password or live key, the user creates the accounts; forces a rebrand; "talk to a lawyer before launch". Stars (9.5K on 16.11) and a single-commit history: do not use the star count as proof.

## TOPIC verdict
Why a stranger cares: they pay monthly for an app and the video shows an AI rebuilding it, with a real score. Better than LinkedIn on audience size; riskier on honesty (the reel overclaims "never pay again"; the README says some apps are weeks of work).
Honest version = OUR OWN test. David runs it; we show what really happened (time, cost, parity score, what is missing). If the result is weak, the video says so or we drop it.

## What David runs (he does this by himself, steps in chat in Hebrew)
1. Make an empty test folder, open Claude Code there.
2. `/plugin marketplace add Jakeschincariol/replica-skill` then `/plugin install replica-skill@replica-skill` (plugin, local to the test folder).
3. Pick ONE small paid app with a public site and help center (a booking page, a link-in-bio page, a habit tracker). Not a big brand.
4. Run in order: recon, architect, design, build, then diff (parity score). Stop there; do not run backend/deploy.
5. Screen-record the run and keep the files `replica/diff` and the parity score. Write down: minutes spent, what it cost, what was missing.
6. Send me: the recording, the score, the folder name. Secrets never in chat.

## Video skeleton (fill from the real result; same Miki style, GSAP, 25-30 s)
Hook rule: NOT the cut gag again (hook type rotation: 102 used the cut). Candidates: "Claude rebuilt a paid app. Here's the score." with the app's real logo, a price tag struck, the tile duplicating into a clone that lands with a real number. Beats: promise (11 skills) / the app and its price / recon (what it found, real) / build (real screen of the clone) / the parity score reveal (withheld to two thirds) / what is missing (honest, said in one plain line) / setup in three steps / link in bio / follow.
Caption: reference's shape in our own words; limits (paid Claude plan, hosting costs, legal check) in caption and /e/103, not in the voice.

## Needs
David's test results (not yet), which app he picks, and his go on the hook idea. Until then nothing is built.
