# Episode 89 script: "PROMPT #1" (built 10.11.2026)

Experiment, not a gate-passer: copies the structure of a 7-second numbered prompt card (arising.ai "Banned Prompt #93") with our look and a short spoken hook. Plan: `channel/episode-89-plan.md`. Build: `video/ep89/` (`build89.py`, `run.sh`, `mix89.py`). File: `video/ep89/out/ep89-final1.mp4` (1080x1920, 13.77 s, audio measured, not heard). Funnel stage: TOP (format test).

## Live verification (10.11.2026, Exa; Firecrawl not used)
- OpenAI Academy page (academy.openai.com/en/public/clubs/small-business-ipf4m/resources/bellevue-small-business-jam-2026-03-02, published 2.3.2026, last updated 29.5.2026) still says under "Quick Tips", "Step 1 - Force clarification Paste this at the top of your chat: Before you answer, ask me 3 clarifying questions you need." The same sentence is on the Dublin SME AI Accelerator hub page (18.3.2026). Step 2 and Step 3 sentences also confirmed exactly (used in the caption).
- Product name: the page says "ChatGPT" throughout ("what you want ChatGPT to do"). Still the current name.
- Not claimed: that answers get better as a result we measured, that the prompt is banned or secret, any income. Only: OpenAI's own learning site tells you to paste it first. Third-party backing (Tom's Guide 30.4.2026 lists "Ask me 3 clarifying questions first" among 10 prompts; a Microsoft Copilot tips page has the same idea) is context, not on screen.

## Beat sheet (timings from the voice cues; D = 13.74 s)
| t (s) | Spoken line | On screen |
|---|---|---|
| 0.00-2.28 | 1 "OpenAI says: paste this first." (0.06-2.04) | Frame 0: yellow torn strip OPENAI SAYS:, black strip PASTE THIS FIRST, real ChatGPT/OpenAI mark on a round badge (icon alone), dark cardboard prompt card with an empty ChatGPT-style input, blinking cursor, red stamp PROMPT #1. Logo spins, strips and card drift, camera pushes. |
| 2.28-6.26 | 2 "Before you answer, ask me three clarifying questions you need." (2.40-6.02) | Strips slide out; source strip OPENAI ACADEMY (torn newsprint) beside the logo; the real sentence is typed word by word as read, the 3 on a lime highlight; send arrow is tapped at the end (red ring). |
| 6.26-9.29 | 3 "It makes ChatGPT ask, not guess." (6.38-9.03) | Strip ASK. NOT GUESS.; three paper bubbles with a red "?" and grey placeholder bars pop in (no invented answers shown). |
| 9.29-13.41 | 4 "Save it. Send it to someone who types short prompts." (9.39-13.19) | Strip SAVE IT, SAVED stamp on the card; strip SEND IT, the card shrinks into a sent message; a friend avatar with dots, then a short message "write email". |
| 13.41-13.74 | (silence, 0.55 s tail) | A paper sheet sweeps over; frame 0 is back (loop). First and last frame differ by 17/255 (qa.py loop seam). |
No "tomorrow" sign-off and no comment keyword on screen (David's 7-10 s experiment; the cut is 13.7 s because the typed prompt is read in full: honest note, it is over the 7-10 s target and under the 14 s cap).

Text on screen at once: at most 3 (two strips plus the stamp on frame 0; strip plus prompt later; strip plus prompt plus short message at the end). Safe box clean by `safe_check_hf.js` (tolerance 10 px; a 5 px overshoot at the top on the loop copy of the hook strip is inside tolerance).

## Voice
Line 1, 3, 4: take `a` (exaggeration 0.76/0.70/0.76, seeds 1001/1003/1004); line 2: take `c3` (exaggeration 0.84, seed 3003, 4 retries). The first full render's line 2 had a stray "One year?" before the sentence and ran 5.15 s (the TH of "three" is a known weakness of this voice: the build tool rerolled six times and the burst flag stays on every take). Chosen take c3 has the lowest "three" flag (frication +10.1 dB, the others a burst +21.5 dB or frication +12.5), 3.54 s.
Open: voice_doctor flags the ending of line 2 ("need." -38.9 dB against a median of -19.8): the same in all four candidates, so it is structural for the final D of this sentence. The sentence cannot be reworded (it is OpenAI's exact text). Needs David's ear. `script_lint` also flags "first", "Before", "answer" (R plus cluster / final R); not reworded: the hook is David's wording and line 2 is a quote.
Accent check (`check_accent.py`) did not run: needs `transformers`, not installed (SKIP in the gate, not PASS).

## Music and sound
Bed: `punchy--trending-instagram-reels-music--delosound.mp3` via `pick_real_track.py 13.74 ... --mood punchy` (exact length), mean -18.0 dB, no quiet stretch (`check_music_bed.py`), 17% of energy under 150 Hz, bed ducked -13.8 dB under the voice in 300-3500 Hz, -8.0 dB un-ducked at volume 0.43 (`voice_quality.py`: clean). Loudness -14.2 LUFS, peak -3.6 dBFS. SFX: CC0 pack files from `video/ep88/sfx/` (impact, whoosh, pop, tick, click, select, ding), 27 events placed from the voice cues (`sfx89.json`). Logged in `channel/music-notes.md`. Not heard.

## Look (what is real, what is not)
Torn-paper collage from ep88 round 7 (real CC0/public-domain paper, newsprint, ticket and map scans; torn edges measured from real torn paper; Big Shoulders, Inter Display and IBM Plex Mono, all SIL OFL). Logo: `channel/assets/ep70-chatgpt-logo.svg` (the OpenAI blossom, sourced for episodes 61-70; icon alone on a badge, nothing under it; the source strip sits beside it, not under it). The dark prompt card is drawn (cardboard with a ChatGPT-style input), not a screenshot. Credits for scraps: `channel/ep88-image-credits.md`.

## Check results (real output of `./export/check_hf.sh`, tag final1)
safe_check_hf: PASS (clean at tolerance 10 px). qa.py --hf: PASS (1080x1920, 30 fps, 13.77 s, -14.2 LUFS, peak -3.6 dBFS, visual change median 0.03 s, longest still 2.60 s; warns 13.8 s is outside the old 30-90 s band, which is intended here). voice_quality: PASS (line pitch ranges 6.2 / 5.8 / 4.9 / 6.8 st, ends -2.2 / +0.3 / -1.5 / -0.4 st). voice_doctor: PASS with the one fix note above. accent: SKIP.

## Scores (judgement, not measurement; scale in channel/score-calibration.md)
HOOK 66: authority in the first 3 words and the subject said and shown, but no felt personal problem and "paste what?" is open until line 2. VIRALITY 62: a saveable, checkable tip with a named authority and a named person to send it to, a loop and a rewatch reason (the card is read once, typed fast); no personal surprise. VALUE 72: a real, usable sentence plus two more in the caption. OVERALL 66. PREDICTED VIEWS 150-400 (ASSUMPTION), score about 43-58 on the scale. Below the 85-95 gates and below David's raised bar: built because David asked for this experiment. Our own validity test showed such self-scores do not predict views (ep 86 was scored 88-93 by agents and landed at 75 on the scale), so treat these as labels, not forecasts. Real 48 h / 72 h views go into score-calibration.md.

## Disclosures
This video was made with help from Claude. OpenAI and ChatGPT are OpenAI trademarks; this channel is not affiliated with OpenAI. The prompt text is quoted from OpenAI Academy.

## Blind reader: NOT run (no Agent tool in this session). What the blind reader should test
1. Show ONLY frame 0 (`video/ep89/out/f0.png`) and the first spoken second: "what is this about?" The answer must name OpenAI/ChatGPT and "a prompt to paste". Ask: does "PROMPT #1" read as a series label or as a mistake? Does the empty box make you ask "paste what?" (curiosity) or lose interest?
2. "Would you stop scrolling, and why?" at frame 0.
3. After the full watch: what was the prompt, in your words, and could you type it from memory? (Tests whether 3 s of typing is enough to read it, and whether people would screenshot or rewatch.)
4. Is "OpenAI Academy" understood as OpenAI's own site? Is the mark readable at phone size?
5. The tip needs a reason: does "It makes ChatGPT ask, not guess." land, or do people want to see an example answer? (This cut has none, deliberately: no output we did not test.)
6. Does the 13.7 s length feel long for a one-sentence tip? Where did attention drop?
7. Loop: did anyone notice the restart at 13.4 s?

## Weak spots (honest)
Frame 0 is clear but not gut-level; the hook is authority plus a gap, not a felt problem. Phase 2 is the longest stretch with a still-looking card (typed text is the motion). The ending hold (about 2.6 s, SEND IT and a static message) is the longest still run and sits right at the limit. The bubbles are placeholders (grey bars), which may read as empty. The collage is the ep88 look, which David's friend Roni already flagged as "too AI" for clean cards: this one is textured, but the dark card is a clean drawn UI.

## Blind reader, run 10.11.2026 (fresh agent, frame 0 + first spoken second)
- A) Official starting prompt from OpenAI to paste; cannot tell what it does. B) Probably would not stop: "PROMPT #1" with an empty box shows no payoff, looks like a tutorial or ad. C) Guessed a generic system prompt ("act as an expert"). D) Collage of old maps and newspaper has nothing to do with ChatGPT, feels like a template; empty text box; sticker logo reads like an ad. E) Show the prompt's actual result or the surprising thing it does, "OpenAI says paste this first" as a small tag.
- Verdict: do not publish as is; needs a real result on screen (David's 10 s screen recording).
