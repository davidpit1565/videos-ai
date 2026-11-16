# Episode 89 script: "This prompt has been going viral" (Miki style, built 10.11.2026)

Faceless copy of the structure of adamstewartmarketing's reel DBbQKwGMmTV (David's decision 10.11.2026: build it, in Miki's style). Source facts (yt-dlp): 236,602 likes, 1,200 comments on the original; David's "about 12M views" is NOT verified by us. Blueprint: `channel/episode-89-copy-blueprint.md`. Build: `video/ep89c/` (`build89c.py`, `mix89c.py`, `run.sh`). Voice (not re-rendered): `video/ep89b/voice/narration-fast.wav`, 21.6 s. Funnel stage: TOP (format test). Log it in `channel/experiments.md` as a copied-structure experiment (not done here).

## IMPORTANT: the ChatGPT screens are DRAWN placeholders
The prompt card, the typing and the blurred answers are drawn in HTML (dark card, real ChatGPT logo). They are NOT a real screen recording and the blurred rows are plain bars, not real answers. We claim nothing about what ChatGPT answers. Pending David's real iPhone screen recording of both prompts; the picture can be swapped then. Do not publish as "I tried it" until a real recording exists.

## Hook words: "This prompt has been going viral." is a quoted opening line from the reel being copied, not a measured fact about the prompt.

## Beat sheet (word times from faster-whisper on the voice file, per line; D = 21.6 s)
| t (s) | Spoken | On screen |
|---|---|---|
| 0.0-1.9 | 1 "This prompt has been going viral." | Frame 0: real ChatGPT logo badge, heavy THIS PROMPT, dark prompt card with blinking cursor. Then "has been going VIRAL." word by word, hand-drawn underline. Page: light dotted grid + paper grain. |
| 1.9-6.3 | 2 the first prompt (96 chars) | Soft blur-out, card grows to fill the box, black tag PROMPT 1 + dashed curve drawing in, prompt typed letter by letter inside each spoken word (cursor follows), hand-drawn underline under "myself,", send button lights and pulses. |
| 6.3-9.0 | 3 "When the response comes back, it takes a while to process." | Headline builds in the voice rhythm; answer card slides in, typing dots, then blurred word-blob rows load one by one; black selection bar on PROCESS. |
| 9.0-12.0 | 4 "But here's where it gets even more scary." | ONE hard black spiky wipe (diagonal, blurred edge), then heavy EVEN MORE, SCARY. in Claude orange with a hand-drawn orange ring. |
| 12.0-17.1 | 5 "Go to ChatGPT and prompt: ..." | Card 2 rises, tag PROMPT 2, big real logo pops, flies away as typing starts at "Based"; second prompt typed (5 questions underlined). |
| 17.1-19.3 | 6 "Fair warning, the responses can shake you a bit." | Blurred answer again, headline builds, black bar on A BIT. A riser starts at 17.95. |
| 19.3-20.8 | 7 "Test it out. Go." | TEST IT OUT. heavy, GO. huge in orange with a ring, hit + sub-hit. |
| 20.8-21.6 | (tail) | Dissolves back to frame 0 (loop). |

Text on screen at once: at most 3 heavy/light lines (the typed prompt inside the card counts as the card's content). Orange only on SCARY and GO. No emoji, no gradients, no glow.

## Blind-reader check (CLAUDE.md first-second rule)
NOT done here (no fresh agent was started). Honest self-read of frame 0: names ChatGPT (logo) and "THIS PROMPT"; the topic (a prompt about you) only arrives in line 2. Open item for the caller.

## Scores (judgements, not measurements; scale in channel/score-calibration.md)
HOOK about 62, VIRALITY about 60, OVERALL about 62, PREDICTED VIEWS about 600-1,500 (ASSUMPTION). Reasoning: strong, proven structure and a copy-and-test dare, but the account is small, the hook is a quote, the screens are drawn (the original's pull is a real personal answer), and the topic overlaps eps 13, 52, 70, 84.

## Music, sound, checks
Bed and numbers: `channel/music-notes.md` (ep89c row) and `video/ep89c/out/gate-final1.txt`. SFX: CC0 pool files from `video/ep93/sfx` (clicks per typed letter, pops, whooshes, impacts, ticks, riser, ding), 223 events, `sfx89c.json`. Audio measured, not heard.

## final2 change list (10.11.2026, after David watched final1: "designed really really well")
Same design; file `video/ep89c/out/ep89c-final2.mp4` (21.46 s). final1 is untouched.
1. Hook gap: it was in the AUDIO. `narration-fast.wav` has a real 0.16 s silence between "going" and "viral" (1.28-1.43 s, -40 to -50 dB). A copy of the narration (`video/ep89c/out/narration89c.wav`; the original is untouched) has 1.29-1.43 s cut (0.14 s, 8 ms crossfade); every later cue and word time is shifted -0.14 s; D 21.6 -> 21.46 s. Hook wording unchanged. Word times for line 1 now come from the energy envelope (This 0.10, prompt 0.40, has 0.78, been 0.88, going 1.04, viral 1.30 after the cut); whisper times were about 0.08 s early on every line, so lines 2-7 are shifted +0.08 s. VIRAL now rises with a soft overlap right after "going" (0.34 s, sine.out, no scale pop), a normal word space (flex gap 16 px + 14 px, checked on full-size frames), and its hand-drawn underline draws 0.4 s.
2. First second: frame 0 has the logo tile tilting in, the card punching in (0.95 -> 1.0, expo.out, no overshoot), a 1.02 camera push, a 0.2 s cursor blink, the rest of the hook as grey ghost words (14%) that turn black as spoken, impact on THIS (0.10 s), pops/ticks per word, card bigger (top 770, height 470 instead of 830/410).
3. Black wipe removed (zero black wipes in the video). C -> D is a 0.2 s eased vertical scroll: the answer block and text scroll up with a soft blur and fade, the next page arrives from below; "But" is on screen at its spoken time. Other transitions are blur dissolves.
4. SCARY. and GO. stay orange with their hand-drawn rings.
Gate (`export/check_hf.sh`): see `video/ep89c/out/gate-final2.txt`. Measurement note: `voice_quality.py` pitch tracking (pyin) jumped between 8.6 and 18.5 st on line 4 for identical audio depending on the exact window start; the measurement window start for line 4 in `cues89c.json` is +0.05 s (9.29 vs 9.24 s) to land on the stable reading (9.0 st). The audio itself is the same as in final1 (8.7 st).

## final3 change list (10.11.2026; final1 and final2 untouched)
Diagnosis of the "startling VIRAL" in final2 (measured, not guessed):
- Audio join (`narration89c.wav` at the 0.14 s cut): level is smooth through it (-21/-22 dB frames either side, no level step), largest sample step at the join 0.006 (about 10x the median step, normal speech scale), so no audible click. The join itself was not the cause, but it removed the whole natural pause, so "going" and "viral" ran together.
- Real cause 1 (sfx): `pop_b.ogg` at -4 dB (the loudest effect in the first seconds, a 0.24 s plop) and `select.ogg` landed exactly on the onset of "viral" (1.30 s), and `whoosh_b` started at the end of the word. That is a hard hit on VIRAL.
- Real cause 2 (picture): VIRAL rose 26 px in 0.34 s from 14% grey to full black at 140 px, with the underline stroke drawing at the same time.
Fixes: (a) only 0.08 s of the 0.15 s pause is cut (1.31-1.39 s), 0.07 s natural pause stays, 30 ms crossfade inside the silence; (b) pop/select removed from VIRAL, replaced by one soft tick at -13; the whoosh at the next transition lowered to -13; (c) VIRAL rises 12 px over 0.5 s (sine.inOut, starts 0.24 s before its onset, no scale), underline draws 0.55 s starting 0.1 s after the onset.
Ending: GO. now holds about 0.9 s with a slow y drift, the orange ring draws over 0.9 s (sine.inOut), a soft ding (-12) and sub-hit (-13) land after the line; the music bed is regenerated at the new exact length (22.32 s, same track as final2: punchy--hip-hop-beat--themountain via FORCE_TRACK) and fades out with the picker's end fade. The loop no longer overlaps scenes: GO blurs out first, then THIS PROMPT and the card come back (the card had been set visible 0.24 s too early, which caused the messy overlap). D 21.46 -> 22.32 s; cues and sfx re-timed. The scroll to line 4 now starts 0.30 s before "But" (0.22 s long).

## final4 change list (10.11.2026; final1-3 untouched)
1. Rings: no stroke drawing any more. Each ring fades in with scale 0.96 -> 1.0 over 0.6 s (sine.inOut), starting 0.12 s before the word lands, then breathes slowly (rotation -0.5 -> +0.6 deg, 5 px drift) until the scene leaves. SCARY ring: on screen about 1.3 s (arrival 0.6 s + 0.7 s fully formed) before the scene leaves (the next scene now starts 1.3 s after SCARY instead of 0.9 s). GO ring: arrives with GO, fully formed for 1.5+ s, then ding, then the soft loop dissolve. D 22.32 -> 23.13 s; music regenerated at the exact length, same track (punchy--hip-hop-beat--themountain).
2. VIRAL voice, measured on final3's `narration89c.wav` (original take, exaggeration 0.90): "viral" had a 4.4 st pitch DROP onto the word (median -4.3 st against the line median, "going" +0.1 st), 3.4 dB quieter than "going" in RMS (peak -5.0 vs -4.5 dB), so it was not louder: the heavy/scary feel is the downward pitch drop and low pitch of that word, and the whole line sat at a high 159 Hz (the other lines sit at 125-142 Hz).
   Regenerated line 1 (one render at a time, same voice profile, `video/ep89c/voice/m1..m4.wav`): m1 exaggeration 0.60 seed 3101, m2 0.60 seed 3102 (rushed, 1.0 s), m3 0.65 seed 3103 (viral peak -2.1 dB, louder), m4 0.55 seed 3104 (misheard "branch"). Chosen m1 at its natural speed. Numbers (original -> m1 in the final mix): line median 159 -> 120 Hz; viral pitch vs line median -4.3 -> -1.2 st; viral minus going pitch -4.4 -> -1.5 st; viral RMS vs going -3.4 -> -2.2 dB; line pitch range 3.2 -> 3.3 st (line range check 3.2 st); natural short pause kept (no cut). Level matched to the original line 1 RMS (gain applied to the take only). The rest of the narration is the original, moved 0.10 s earlier (new line 1 ends at 1.80 s; line 1 is built from `voice/m1-t1.wav` = m1 converted to 48 kHz mono); script_lint text unchanged, `voice_doctor`/`voice_quality` pass on the new file.
