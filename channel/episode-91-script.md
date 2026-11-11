# Episode 91 - "Me with Claude / Me with ChatGPT" (10.2 s, NOT published)

FORMAT: numbered joke-meme experiment, TOP of funnel. A JOKE about style and opinion, NOT a test result: we never tested Claude vs ChatGPT on this (we only tested that ChatGPT tends to agree, episodes 72, 73, 80). Related angle already covered: episode 93 (tone joke, dog vs cat); this one is the same family with a new subject (duplicate check: `channel/topics-covered.txt` has no "Claude vs ChatGPT" entry; episode 93 is the nearest neighbour, say so to David).

SOURCE ART: David's own images made with ChatGPT on 10.11.2026 (`channel/memes-2026-11-10/david-chatgpt/`, meme2-square.png 1254x1254 used; meme1-portrait.png not used in this cut). Original artwork by the channel owner, AI-generated: the caption must say so (Instagram AI label). The Claude and ChatGPT logos in the images are DRAWN BY THE IMAGE MODEL, not copied from the brand pages. We added no brand mark and redrew none. (Standing rule asks for real logos; here the logos are part of the artwork. David decides whether that is acceptable.)

## Voice (our cloned voice, one TTS render, build_voice.py, exaggeration 0.78, lines 0.80/0.74/0.74/0.74)
1. Me with Claude. It listens.
2. Me with ChatGPT. It's way more complex.   (reworded from "Actually, it's more complex": script_lint flags "actually")
3. Which one are you?
4. Tag someone who needs the Claude one.     (reworded from "...the first one": "first" flagged)
Present tense, plain words. Hook: the subject (Claude vs ChatGPT) lands in the first 3 words and is also big on frame 0 (both labels are in the artwork).

## Beat sheet (D = 10.18 s, build `video/ep91/build91.py`, composition `video/ep91/hf/index.html`)
- 0.0-0.6  Frame 0 = the whole artwork, uncropped, 950 px wide in the safe box (two windows onto one file, 6 px divider). Slow push-in. Impact sfx. Voice: "Me with Claude."
- 0.6-2.2  Windows crop, a headline strip opens between them, top window pushes onto man + checklist + robot. Headline "It listens." (orange) word by word as spoken.
- 2.2-5.5  ChatGPT beat: bottom window grows, Claude window shrinks and dims. Push on robot + bubble at "ChatGPT", then punch-in on the "Step 1..8" board at "way more", then slow scroll down the steps to "Step 8: ..." at "complex". Headline "It's way more complex." (teal on "complex.").
- 5.5-6.9  "Which one are you?": two equal windows, both faces; the windows pop on "Which" and "one".
- 6.9-9.6  Tag line (two lines, "Claude one." orange); windows settle, slow push.
- 9.6-10.2 Everything eases back to the full artwork of frame 0 (loop; first vs last frame differ by 0.6/255).
Only text we add: the headline in the strip (max 2 lines on screen). No decorations, no wipes, no gradients; background flat dark navy.

## Checks (real numbers, `video/ep91/out/gate-final1.txt`)
- safe_check_hf: clean, no overlaps over 10 px (after fixing a headline-fade overlap and the gap opening on "It").
- qa.py --hf: 1080x1920, 30 fps, 10.20 s, 1.9 MB, -14.4 LUFS, peak -3.4 dBFS, visual change median 0.03 s, longest still stretch 2.47 s, loop seam 0.6/255. qa warns "10.2 s outside 30-90 s band" (intended: brief by design, David's 10-13 s brief).
- voice_quality: clean. Pitch ranges 8.0 / 5.0 / 3.6 / 8.4 st, line ends +1.5 / -0.2 / -1.9 st. Bed minus voice in 300-3500 Hz = -8.9 dB at volume 0.47.
- voice_doctor: nothing flagged as BAD; one note: line 2 harsh S (-8.6 dB), de-esser under-doing it. Not repaired. Line 3 is fast (4.3 syl/s, 0.94 s).
- check_accent: SKIPPED (transformers not installed). Audio was measured, not heard.
- Music: real library, `pick_real_track.py --mood bright`; the track is picked per run: this render used `upbeat-energetic--ikoliksaj-2.mp3` (log in music-notes.md only after David's ear verdict).

## Blind reader
NOT run (no fresh agent was available in this session). Self-check only: frame 0 shows both product names in big type ("Me with Claude" / "Me with ChatGPT") and the two moods; what a stranger may miss is that it is a joke about AI style, which the caption states.

## Scores (judgements, not measurements; scale in `channel/score-calibration.md`; our own validity test, 24 episodes, Spearman -0.23, showed such scores do NOT predict views)
HOOK 70 (names both products at once, but the point is a mood, not a surprise or a stake). VIRALITY 60 (very sendable "which one are you" + a named person to tag; but no save-worthy artifact, nothing checkable, and a Claude-flattering joke from a channel that tested nothing). VALUE 25 (entertainment only). OVERALL 55.
PREDICTED VIEWS 200-600 (score 50-65). ASSUMPTION: relies on the image being funny to a viewer who uses both tools; the cut is a brief animation of a still, so it is a very low-effort experiment.
Funnel: TOP. Experiment question: does a pure opinion-joke image reel beat our median (about 200)?
After 48 h / 72 h put the real views next to the prediction in `score-calibration.md`.

## What is weak (honest)
- Both halves are a crop of ONE still: motion is camera moves only, nothing actually animates inside the picture.
- Top window in the ChatGPT beat is small and dimmed; the Claude half gets less screen time than the ChatGPT half (the joke reads as "ChatGPT bad", which is one-sided; caption says it is opinion).
- Large empty dark areas above y 285 and below y 1235 (platform UI zones, by rule).
- Drawn logos are not real brand marks (see above).

---
# FINAL2 (11.9 s) - NEW 9:16 art (Gemini), same voice lines, no music bed
Files: video/ep91/out/ep91-final2.mp4 (3.0 MB), ep91-final2-review720.mp4 (1.06 MB), cover-ep91.png (1080x1920), f0.png, gate-final2.txt. Builders: video/ep91/build91_final2.py (picture), mix91_final2.py (sound). Final1 files untouched. Source art: channel/memes-2026-11-10/david-chatgpt/meme3-9x16-gemini.jpg (1438x2576). No TTS was run: voice = existing out/narration91.wav (cues unchanged: lines at 0.06-1.92, 2.43-5.27, 5.78-6.72, 7.23-9.58 s), padded with silence to 11.9 s.
THE CLAIM STAYS WHAT IT WAS: a labelled JOKE about style, never a test result (a real test we ran showed no difference). The caption says so, says the image is AI-generated by the channel owner, that the logos are drawn by the image model and that the channel is not affiliated with OpenAI or Anthropic. No ChatGPT screen recording is used or mentioned.
- Safe area: the art is used as two stacked windows (Claude panel / ChatGPT panel) inside x 65-1015, y 285-1245, as in final1; nothing sits under the platform UI, the "Me with Claude" bar of the art is at y 340-410 on frame 0.
- Frame 0 shows both labels: Claude panel full at 950 px wide (y 285-1040, "Me with Claude" big), and a 170 px strip of the ChatGPT panel below it with the "Me with ChatGPT" bar readable.
- Camera (smooth PCHIP keyframes, never stopped; no frame still > 1.03 s per qa.py): 0-0.9 slow push; 1.0-1.5 Claude window zooms onto man + checklist, headline "It listens." in the gap; 2.2-2.9 ChatGPT window grows, Claude window shrinks and dims; 4.0 punch onto the Step board at "way more", 4.9-5.5 scroll down the steps to "Step 8" at "complex", headline "It's way more complex."; 6.1 two equal windows, "Which one are you?"; 7.6 two-line tag "Tag someone who / needs the Claude one." (Claude one. orange); 9.78-11.9 NEW send line "Send this to the friend who / overcomplicates everything." (soft 0.4 s fade-in, about 1.5 s hold, "overcomplicates" in orange), soft fade of everything in the last 0.4 s. No black wipes. sfx as final1 (quiet, same cues, -16.5 dB vs the voice RMS) plus one pop on the send line; no library bed (David adds a sound in Instagram).
- Cover: video/ep91/out/cover-ep91.png = the whole ChatGPT chaos panel ("Me with ChatGPT", stressed man, Step board) full width at y 426-1493, inside the central 4:5 area (y 285-1635).
- Gate (video/ep91/out/gate-final2.txt): safe_check_hf clean (text-only stand-in hf2/index.html, no overlaps over 10 px; widest text line 740 px of 950), qa.py --hf PASS (1080x1920, 30 fps, 11.9 s, -14.6 LUFS, peak -4.0 dBFS), voice_doctor PASS (flag: line 2 S residual, as in final1), voice_quality: the automatic `--mix` check FAILS only because it counts the sfx as "bed" (4.8 dB under the voice); run properly with the real sfx layer as the bed it is CLEAN (sfx -15.6 dB vs the voice in 300-3500 Hz); accent check skipped (transformers missing). Audio measured, not heard.
- Weak: everything is camera moves on a still (nothing animates inside the art); the empty navy below y 1245 and above y 285 is the platform zone by rule; the ChatGPT half still gets more screen time than the Claude half, so the joke reads one-sided (caption says it is a style joke); the drawn logos are not real brand marks (David's call); no blind-reader check; the new send line is a 2-line text, 56 px, smaller than the headlines.
Scores (judgements): HOOK 70 | VIRALITY 62 | OVERALL 58 | PREDICTED VIEWS 200-500 (unchanged low-effort joke experiment; log real views next to this).

---
# FINAL3 (10.1 s) - NO voice, Meta AI fixes applied (David: voice rejected; Meta AI scored final2 71/100, views guess 800-1,800); optional extra, final4 (with the new voice + bed) is the deliverable
Files: video/ep91/out/ep91-final3.mp4, ep91-final3-review720.mp4. Builders: video/ep91/build91_final3.py, mix91_final3.py.
- ONE call to action only: the "Tag someone who needs the Claude one." beat is removed (no on-screen text, no tie-in); the only CTA is "Send this to the friend who / overcomplicates everything." The caption already ends "Which one are you? / Send this to the friend who overcomplicates everything." (no "Tag someone" wording anywhere).
- The ChatGPT board is shown BIG: zoom 2.6 on the art (not redrawn or edited), window 950 x 648 px, so the step text is about 41 px high on a 1080 frame (27 px at 720 px width); scroll from Step 1 to Step 8 over about 2 s (4.5-6.4 s), "Step 8: ..." clearly visible and held about 0.5 s at the end of the scroll; headline "It's way more complex." stays up the whole beat (3.25-6.9 s).
- Shortened from 11.9 s to 10.1 s: "Which one are you?" is now an on-screen text beat only (7.4-8.2 s); the send line fades in at 8.25 s, the camera is STATIC from 8.4 s (no zoom at the end), the send line is fully visible about 1.05 s, then a soft 0.4 s fade.
- Legibility checked on 720 px frames: the "Me with Claude" / "Me with ChatGPT" labels (frame 0), the board text and the send line (56 px at 1080, about 37 px at 720) are readable.
- Sound: no voice, no bed, the quiet sfx re-timed to the new beats and one pop on the send line; -19.3 LUFS integrated, true peak -4.8 dBTP (sfx-only file in the asked -20..-16 range).
- Weak: still camera moves on a still; the ChatGPT half still gets more time; no blind reader; drawn logos not real brand marks.

---
# FINAL4 (10.9 s) = the Meta-fixed picture (final3) retimed to the voice (video/ep91/voice/narration91b.wav, 4 lines) + music bed + quiet sfx
Files: video/ep91/out/ep91-final4.mp4 (2.3 MB), ep91-final4-review720.mp4 (0.87 MB), ep91-final4-altsubclair-preview720.mp4 (alt bed preview, 0.76 MB), f0.png, gate-final4.txt; cover-ep91.png unchanged (same panel). Builders: video/ep91/build91_final4.py (cue-driven picture), mix91_final4.py (voice + bed + sfx). Caption unchanged.
- Picture follows the voice: headline "It listens." at the word "It" (1.48 s), "It's way more tangled." word by word (the headline now says "tangled" like the voice, final3 said "complex"), the board is punched in right after "ChatGPT" (3.7 s) and scrolled to "Step 8: ..." over 1.1 s (4.05-5.19 s) with a 0.55 s hold before the layout changes (the voice is faster than the earlier no-voice cut, so the scroll is quicker than in final3), "Which one are you?" as text at 5.29 s, the ONE send line "Send this to the friend who / overcomplicates everything." from 6.57 s, camera static from 6.9 s, soft fade; length 10.89 s.
- Bed (real library): MAIN punchy--punchy-brass-groovy-pop-track--moonpub.mp3 (cheeky brass groove; raw cut check_music_bed mean -14.8 dB, peak -0.2, no quiet stretch; 18% of the voice-mix bed energy under 150 Hz); ALT bright--upbeat--subclair.mp3 (raw mean -15.7 dB, peak -1.8, no quiet stretch; preview only, -16.7 LUFS not level-matched). Ducked bed vs voice in 300-3500 Hz: -17.4 dB (moonpub) / -17.2 dB (subclair); voice_quality at vol 0.25: bed minus voice -10.2 dB un-ducked. Not the rejected tracks (vibraphone, paulyudin, inquisitive-curiosity, curious-circuits). Bed 0.8 s fade-out; sfx quiet.
- Gate (gate-final4.txt): ALL CHECKS THAT RAN PASSED, accent check skipped (transformers missing): safe_check_hf PASS (text-only stand-in), qa.py --hf PASS (1080x1920, 30 fps, 10.89 s, -14.6 LUFS, peak -3.9 dBFS, longest still 1.1 s), voice_quality PASS (line ranges 9.7 / 6.8 / 3.3 / 5.9 st), voice_doctor PASS (flag: ending -51.5 dB, S residual -10.1 dB). Audio measured, not heard.
- Weak: still camera moves on a still art; the board scroll is fast (1.1 s); music not heard; the ChatGPT half gets more time than the Claude half; drawn logos are not real brand marks; no blind reader.
