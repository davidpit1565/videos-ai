# Episode 90 - "ChatGPT begged me" (ghost test) - EXPERIMENT, not a promise

Built from David's REAL screen recording (iPhone, ChatGPT dark mode, 11.10.2026 21:32). No voice, music only.
Funnel stage: TOP. Format: "ChatGPT does something odd/emotional in a short test" (the pattern of the top-3 episodes).
Honest label: ONE run, results vary. Nothing here claims ChatGPT always answers like this.

## Duplicate check
`grep -i "second chance|ghost|47 days|number between" channel/topics-covered.txt` -> no hit before this episode.

## Hook (present tense, surprise in the first 3 words, 2 lines of text + logo)
- A (shipped): "ChatGPT / begged me."  (real ChatGPT mark badge, real reply on screen: "Wait... can I have a second chance?")
- B: "I ghosted ChatGPT."
- C: "ChatGPT. 47 days. Silence."
Hook type: stake / personal ("it begged ME"), curiosity gap = what did I do to make it beg.

## Structure (26.0 s)
0.0-2.4  payoff frame frozen (real reply on screen), slow push-in, hook text complete on frame 0
2.4-8.4  jump to the start: real typing played ~4.5x (eased ramps), "47" at natural speed
8.4-16.2 typing the ghost message ~4.5x (typo 'fot' passes at 9x, ~0.1 s), begging reply at natural speed, held ~2.6 s with push-in
16.2-21.5 "Yes" typed at natural speed, "100" at natural speed, hold 1.9 s
21.5-26.0 frozen last frame with slow push-in, CTA text, fade to black (0.7 s)
On-screen text only (92 px captions, <= 2 lines; CTA 70 px, 3 lines): "I ask ChatGPT for a number." / "It picks 47." / "I tell it: no talking for 47 days." / "It begs." / "I say yes." / "It picks a new number: 100." / "Try it: ask for a number, then ghost it that many days." / "Send this to someone who ghosts you."

## What was changed in the recording (all real pixels, nothing invented)
- Status bar (clock 21:32, battery) and header icons cropped out. No personal data visible. Recording audio is silent (-91 dB), not used.
- Chat area and input box are two crops of the same frame stacked (the empty black middle of the phone screen is removed); the keyboard is mostly cropped (only its top strip fades out). Source time and text are untouched.
- Speed: typing 1 (src 0.8-9.8 s) 4.5x; typing 2 (src 17.7-30.5 s) 4.5x, 9x around the typo (24.4-26.4 s); every ChatGPT reply, "Yes" typing and the number reveal at 1.0x (loading dots 1.5x). Cut: src 14.6-17.7, 36.3-40.1, everything after 45.9 (the recording continues: "Fahhhhh" and a longer punchline reply, see below).
- Soft dips (0.14 s) at the three jumps, no black wipes.

## Weak points (honest)
- "100" without context reads as love/emoji or as days; the caption "It picks a new number: 100." carries the joke. The recording continues with the real punchline ("HAHAHAHA You gave me a second chance and I STILL chose 100 skull") after a user message "Fahhhhh"; that is funnier but adds ~9 s and an off-topic message. Alternative cut if wanted.
- Bottom 570 px of the frame is empty (platform UI zone) and the chat is small text; whole-frame-alive rule only partly met.
- Dark UI: qa.py's black-frame check fires on the real pure-black screen, so the canvas base is lifted to (13,13,13). That is a deliberate change of the real black.
- Music "curious circuits" (curious mood) not heard by me.

## Blind reader (frame 0 + first second)
NOT RUN by me: this build session has no agent-spawn tool. Please run a fresh agent on `video/ep90/out/f0.png` with the two questions. My own (non-blind, so worth little) reading: it is about ChatGPT begging for a second chance after a 47-day silence; I would stop because the reply is odd and emotional, but the cause (the 47 days) is only half-readable on frame 0.

## Scores (judgements, not measurements; scale of channel/score-calibration.md)
HOOK 72 | VIRALITY 66 | OVERALL 68 | PREDICTED VIEWS ~600 (about 64 on the scale; 200 = 50, 10,000 = 100). Reasoning: strong subject + emotional/funny reply on frame 0 and a sendable ghost-someone ending, but one run of a known meme-prompt, small UI text, no face, no on-screen proof of repeatability. Log real 48 h / 72 h views next to this.


---
# FINAL2 (28.30 s) - replaces final1's crop/titles (final1 files kept untouched)

David's changes applied: (1) the WHOLE phone screen (1206x2622 scaled by height to 884x1920, black side bars = the real black UI; only the iOS status-bar strip, top 128 px, is blacked out; no lifted base, colours are the real ones); (2) all per-step captions and CTA cards removed; ONE opening title only; (3) visual hook: zoomed readable frame 0, then one eased pull-back to the full screen while the real chat rewinds to the start; (4) funny ending kept; (5) new music + quiet sfx.

## Title (hook research: channel/hooks-ep90.md)
Default shipped: ChatGPT badge (real mark, icon alone) + "I ghost ChatGPT." / "It begs." (present tense, 2 lines, in the band above the chat, covers nothing). Alternatives: "Ghost your ChatGPT. Watch." ; fallback "I leave ChatGPT. It begs." ; older "ChatGPT begged me." (11th of 12 on the cropped frame).
Frame 0 (out/f0.png): the real "Now we won't be able to talk for 47 days" bubble and the real reply "Wait... can I have a second chance?" at x2 readability (zoom 1.17-1.22 on the real pixels, no empty-black-half above; the lower ~35% is empty because the platform UI covers it).

## Timeline (out seconds <- source seconds)
0-1.4 zoomed frozen payoff frame with slow push-in, title; title fades 0.95-1.4
1.4-2.3 ONE eased move: zoom out to the full screen while the real chat plays in reverse to the start (36.2 s -> 0.8 s of the recording, sampled; header/status strip fade in only at the end of the move)
2.3-8.5 <- src 0.8-14.6: typing 4.5x, "47" 1.0x
8.5-15.8 <- src 17.7-35.8: typing 4.5x (typo 'fot' at 9x), begging reply 1.0x with push-in to x1.10
15.8-21.2 <- src 40.1-45.9: "Yes" 1.0x, "100" 1.0x with push-in
21.2-27.0 <- src 47.9-57.9: typing "Fahhhhh" 3.5x, loading dots 4x, "HAHAHAHA You gave me a second chance and I STILL chose 100" (skull) 1.0x, push-in to x1.12
27.0-28.3 hold last frame, gentle fade to black (0.9 s). No text at the end.
Cut list (source): 0-0.8, 14.6-17.7, 35.8-40.1, 45.9-47.9 (and nothing after 57.9, the file's end). Soft 0.14 s dips at the three jumps, no black wipes.

## Music + sfx
Default A: vibraphone--alexmorgan.mp3 (EQ: high-pass 140 Hz + 3 dB at 1.8 kHz for phone speakers); B bright--feel-good-music--paulyudin.mp3; C curious--inquisitive-curiosity--musictown.mp3. Bed is shaped to the timeline: duck -7 dB under the begging reply, near silence (-28 dB) 0.7 s before the punchline reply, bed returns and fades with the picture. Quiet sfx from video/ep91/sfx: tick/click_b bursts per typing burst (-17 dB re bed), pop_a on incoming bubbles, select on "Yes", ding on the begging reply, pop_b on "100", impactsoft on the punchline. Not heard by me; I could not A/B sfx by ear, kept the minimal set from channel/music-research-ep90.md. If any sfx distracts, remove it in video/ep90/mix90.py.

## Gate (video/ep90/out/gate-final2.txt)
safe-area for the one title: clean, no overlaps. qa.py: 1080x1920, 30 fps, yuv420p, 48 kHz stereo, length ok, -14.1 LUFS, peak -4.5 dBFS. qa.py BLOCKERS that remain and are NOT fixed: "black frames" (mean luma < 8, the real pure-black ChatGPT UI), "first frame is blank" (luma 11.4, true black UI with a white-on-black title), and "picture frozen 6.1 s at 22-28 s" (the real waiting/reading screen with only a slow push-in; reply must stay readable). I did not lift the base or fake motion to pass; decide whether to accept or to shorten the final reading hold.

## Weak points (final2)
Lower third of the frame is empty on the zoomed frame 0 (safe-area), dark low-contrast grey text on black is hard to read on a phone in daylight, the rewind is sampled (about 27 frames) not motion-blurred, music and sfx not heard by me, no blind-reader check was run on the new f0. Honest label: one run, results vary.
Scores (judgements): HOOK 78 | VIRALITY 68 | OVERALL 71 | PREDICTED VIEWS ~700 (about 66 on the scale).

---
# FINAL3 (28.30 s) - David rejected the title and all three music beds; one version

- NO title words. Frame 0 = the zoomed real bubbles ("Now we won't be able to talk for 47 days" + "Wait... can I have a second chance?") with only the real ChatGPT badge (icon alone, 170 px, centred in the band above the chat) which fades before the pull-back. Same smooth pull-back + chat rewind, same cuts, funny ending, whole screen, no captions as final2. Build: video/ep90/build90c.py.
- NO music bed. Audio = sound design only (video/ep91/sfx), built by video/ep90/mix90c.py: tick/click_b per typing burst (about -19 dB re full scale before the peak is set), pop_a on incoming bubbles, select on "Yes", ding on the begging reply, pop_b on "100", about 1.3 s of true silence while the loading dots run, then impactsoft on the "HAHAHAHA" reply, 0.5 s fade at the end. Peak -6.0 dBFS and -26.8 LUFS integrated in the mp4 (deliberately light so David can add a trending audio inside Instagram; the file keeps its own audio track). Not heard by me.
- qa.py on final3: still reports the dark-UI blockers (black frames: mean luma < 8 on the real black UI; first frame luma 7.7; frozen 6.1 s at 22-28 s: reading hold of the last reply) and a loudness BLOCKER (-26.8 LUFS vs the -14 target) which is intended for a sfx-only file. Nothing was lifted or faked to pass. No text on screen, so the safe-area text check does not apply.
- Weak points: nothing in the first frame says what the video is about in words (the badge + the real reply must do it); lower third empty; sound is very sparse and may feel dry on a phone; no blind-reader check was run.
- Scores (judgements): HOOK 70 | VIRALITY 66 | OVERALL 68 | PREDICTED VIEWS ~600 (about 64 on the scale).

---
# FINAL4 (28.30 s) = final3 + ONE opening title (David via coordinator, second hook-research round)
Only change vs final3: the ChatGPT badge (icon alone, 100 px, left) plus the title "Does your ChatGPT" / "beg too?" in off-white (247,247,242), no box, no shadow, in the band above the zoomed bubbles on frame 0 (x 65-985, y 408-650, inside the safe area, covers nothing of the chat). It holds with the opening zoom (1.4 s), fades 0.95-1.4 s before the pull-back so it never overlaps the moving chat. Picture, sound design (sfx only, no music bed), cuts, funny ending are the final3 ones (audio track copied byte-for-byte from final3). Build: video/ep90/build90d.py. Framing mirrors the proven 'Does your ChatGPT cave when you push?' test. Caption first line: "Does your ChatGPT beg too? Mine did, on one run." (present tense, honest one-run wording, no promise).
Gate: safe-area check of the title clean (video/ep90/out/gate-final4.txt). qa.py still shows the same dark-UI blockers as final3 (black frames, first-frame luma, 6.1 s frozen reading hold, sfx-only loudness -26.8 LUFS); none fixed or faked.
Weak: question hook asks the viewer something the video only answers from 1.4 s on; same empty lower third; no blind-reader check; audio not heard by me.
Scores (judgements): HOOK 74 | VIRALITY 67 | OVERALL 70 | PREDICTED VIEWS ~650 (about 65 on the scale).

---
# FINAL5 (26.96 s) = final3 (no title words, badge only) + contrast + faster typing
The hook will be a separate pasted-in scene made elsewhere. Build: video/ep90/build90e.py, sfx: mix90e.py (same cues as final3, re-timed).
1. CONTRAST (edit only, same curve for R, G and B, blacks stay black, no tint/glow/sharpen): the recording is dimmed, its text peaks at only ~129/255. A monotone cubic curve through (0,0) (40,50) (80,104) (129,238) (140,255) lifts text to ~238 (the real iPhone dark-mode text value is about 236) and the purple bubble fill from (32,24,78) to (40,30,100). WCAG contrast ratios (measured on the real frames, before -> after): "Now we won't be able to talk for 47 days" bubble text on its bubble 3.82 -> 11.02; "Wait..." reply and the "HAHAHAHA..." reply (grey on black) 5.39 -> 18.10; typed text in the input box on the grey field 3.63 -> 10.42. Full-size frames checked: still reads as a real iPhone dark-mode recording.
2. TYPING: plateau 6x (was 4.5x) with the same eased ramps; typo section 12x (was 9x); "Fahhhhh" 4.5x (was 3.5x). Replies, "Yes" and the number reveal still 1.0x. Length 26.96 s (was 28.30 s). Letters still appear in 1-2 character steps per frame at 6x (typing, not a paste pop), but individual letters are hard to follow; if it reads too fast, go back to 5x.
Gate (video/ep90/out/gate-final5.txt): same dark-UI qa blockers as final3 (black frames on the real black UI, frozen reading hold at the end, sfx-only loudness about -26 LUFS), none faked away. No text, so no safe-area text check. Audio sfx-only, not heard by me.
Scores (judgements): HOOK 68 | VIRALITY 66 | OVERALL 68 | PREDICTED VIEWS ~600 (hook scene comes separately).

---
# FINAL6 (29.18 s) = hook scene (2.2 s) pasted in front of final5 (26.96 s)
Files: video/ep90/out/ep90-final6.mp4, ep90-final6-review720.mp4, hook-scene.mp4 (hook only), f0.png (frame 0 of the hook, before the text appears at 0.1 s), hook-1s.png. Builds: video/ep90/build90_hook.py (hook picture + text), the hook audio was made with a small numpy script (50/100/150 Hz swell + impactsoft, see below), final5 unchanged (contrast lift, 6x typing, sfx, funny ending, pull-back).
- Hook picture: David's ChatGPT image images/2.webp (941x1672) upscaled with Lanczos to 1080x1920; slow eased push-in 1.0 -> 1.3 aimed at the dark screen; very gentle indigo rim-glow pulse (sine 0.8 Hz, +-7%), light grain (sigma 3), shadows crushed to true 0, fade to pure black from 1.35 s to 2.05 s so the cut lands on the recording's pure black.
- Brand rule: the image's generated knot was an AI approximation. It is PAINTED OUT (diffusion inpaint) and the REAL ChatGPT mark (channel/assets/ep70-chatgpt-logo.svg, same file as the badge, rendered white) is warped onto the screen with an affine matched to the phone tilt, dim light grey (214,214,226) with a faint glow. The generated "Message ChatGPT..." placeholder text in the input pill is also painted out (the pill with its + and send icon stays, those are generic). Still approximations: the status bar (9:41, signal) and the send arrow of the generated image remain AI-drawn, they are generic iOS-like UI, not brand marks.
- Text (edit-time, Inter Display Black, #F5F5F5, centred, no box): line 1 "ChatGPT cannot handle rejection." (two lines, 88 px) fades in at 0.1 s, line 2 "47 days." (112 px) at 0.8 s, both fade out 1.45-1.8 s. SWAP THE WORDING: variables HOOK_LINE1 / HOOK_LINE2 at the top of video/ep90/build90_hook.py (David's earlier favourite: "Making ChatGPT crash out"). Safe area: measured bbox of the bright text pixels at 1.2 s is inside x 65-1015, y 269-1248.
- Hook sound (no voice): sub-bass swell 50 Hz + 100/150 Hz harmonics (so phone speakers can hear it) rising 0.3-1.8 s at about -18 dBFS, hard-cut (15 ms) at 1.8 s; one soft thud (impactsoft, about -8 dBFS) at 1.2 s; 0.4 s true silence 1.8-2.2 s; the recording's sfx start after the cut. Hook audio -27.2 LUFS, peak -10.2 dBFS. Not heard by me.
- Cut: last hook frames (2.1-2.15 s) are pure black (mean luma 0.00, min 0); first recording frame at 2.2 s has pure-black background (corners 0,0,0). Hard cut, no dip. Streams concatenated with -c copy (same codec settings), checked: h264 1080x1920 30 fps, aac 48 kHz stereo, 29.18 s.
- Weak: the push-in only reaches 1.3x so the hand dominates the lower half and the phone screen does not fill the frame; the real-logo warp is by eye (tilt matched approximately); the still has no real motion, only the push-in, pulse and grain; crushing the shadows also dimmed the generated input pill; the wording is David's call; audio not heard by me; qa.py dark-UI blockers as final3/5 still apply to the recording part.
Scores (judgements): HOOK 72 | VIRALITY 66 | OVERALL 69 | PREDICTED VIEWS ~650.

---
# FINAL7 (22.73 s) - renumbered ep90 (was ep92); fast hook + short cut (David: final6 hook too long, title bad, payoff too late)
Files: video/ep90/out/ep90-final7.mp4, ep90-final7-review720.mp4, f0.png, gate-final7.txt. Builds: video/ep90/build90_hook2.py (hook), build90f.py (recording), mix90f.py (sound). Contrast lift, real-recording pull-back, funny ending, sfx-only sound as final5/6.
- HOOK (1.1 s): the phone picture (real ChatGPT mark painted in, brief in FINAL6), darkened x0.82 plus a dark top gradient, quick push-in 1.0 -> 1.15, light grain, crushed blacks. TEXT FULLY VISIBLE FROM FRAME 0 (no fade-in), heavy Inter Display Black, tight tracking, widest line = 940 px (x 70-1009, y 329-579, inside the safe area), white, no box. Wording is two variables at the top of build90_hook2.py: HOOK_LINE1 = "ChatGPT", HOOK_LINE2 = "47-day timeout." (David's latest; earlier tried: "Ghosting ChatGPT / for 47 days." rejected as slang; "ChatGPT gets a / 47-day timeout." sizes 128 vs 117 px for the other wrap, shortened to the version above). Text soft-fades out 0.72-1.0 s, picture is pure black from 1.05 s.
- Hook sound: low 50/100/150 Hz swell 0.1-0.9 s (about -18 dBFS), one soft thud (impactsoft, about -8 dBFS) at 0.45 s, silence 0.9-1.1 s.
- Cut at 1.10 s: last hook frame mean luma 0.11, first recording frame background (0,0,0) in the corners: black level matches, hard cut.
- Recording intro: first recording frame = zoomed real bubble + reply, badge, held 2.2 s with a slow push-in (zoom 1.19 -> 1.235, as far as the reply's left edge allows without cropping), then 0.5 s pull-back + rewind.
- VIEWER TIMELINE (s): 0.0 hook text readable; 1.10 cut to the real chat; about 1.5 reply readable (7 words) and about 3.3 pull-back starts; 3.8 start of the sequence (number prompt typed about 10x, "47" shown); 10.6 begging reply streams in (second time, in sequence), held about 1.7 s; 15.45 "100"; 18.9 punchline reply ("HAHAHAHA ... STILL chose 100") starts, readable by about 20, held about 2 s, soft fade to black 21.8-22.7. Total 22.73 s (final6 29.2 s).
- CUT LIST (source recording seconds kept): 1.0-13.8 (typing 10x, bubble, dots 5x, "47" about 1 s), 17.8-36.2 (typing about 8x, typo section 14x, dots 4x, begging reply natural speed), 40.3-45.2 ("Yes" typed at 2x, dots 3x, "100" about 1.1 s), 47.9-57.9 ("Fahhhhh" typed 4x, dots 8x, laughing reply at 1x) + 0.9 s hold. Dropped: 0-1.0, 13.8-17.8, 36.2-40.3, 45.2-47.9.
- Gate: hook text bbox inside the safe area. qa.py: same dark-UI blockers as before (black-frame runs on the real black UI, loudness -25.4 LUFS for an sfx-only file); warnings: near-still reading holds (the 2.2 s opening hold, the laughing-reply hold). Nothing faked.
- Weak: the 2.2 s opening hold is a near-still stretch by design; typing at 8-10x is not followable letter by letter; the hook picture has no real motion; sound not heard by me; wording still David's call (swap in build90_hook2.py and re-concatenate).
Scores (judgements): HOOK 74 | VIRALITY 68 | OVERALL 71 | PREDICTED VIEWS ~700.

---
# FINAL8 (22.77 s) - LIGHT hook scene (David: final7 hook "just a dark image"); recording part, cut list and its sound identical to final7
Files: video/ep90/out/ep90-final8.mp4, ep90-final8-review720.mp4, hook-scene8.mp4 (hook only), f0.png, gate-final8.txt. Builder: video/ep90/build90_hook3.py (wording variables HOOK_LINE1 / HOOK_LINE2 at its top, same as before). The recording + its audio are copied from final7 (stream copy from 1.1 s), only the 1.2 s hook was replaced.
- Hook (1.2 s), episode-81/89 light look: off-white base #ecebe5, faint dotted grid (54 px) and grain; heavy black Inter Display Black text "ChatGPT" / "47-day timeout." big, fully visible from frame 0 (bbox x 74-1004, y 312-560, inside the safe area); under it a rounded card (x 65-1015, y 620-1530) with the phone picture BRIGHTENED (gamma 0.52, exposure x1.18, faint cool lift): room, marble, hand and phone body readable, indigo rim glow kept and pulsing gently, real ChatGPT mark as in final7; gentle push-in 1.0 -> 1.12 and a 7 px float from frame 0.
- Transition: text fades 0.6-0.82 s; the card expands to full bleed 0.82-1.08 s while the push-in goes through into the phone's dark screen (the real mark grows), then to pure black from 1.07 s. No white flash and no black wipe: frame mean luma 138 (0.9 s) -> 71 -> 41 -> 30 -> 0.4 (1.15 s). Cut at 1.2 s: last hook frames pure black, recording first frame has a (0,0,0) background.
- Hook sound: same low 50/100/150 Hz swell (-19 dBFS, 0.1-0.95 s) and one soft thud (about -9 dBFS) at 0.5 s; the recording's audio is final7's (decoded once more and re-encoded together, one extra AAC generation).
- Viewer timeline: hook text readable 0.0; picture starts expanding 0.82; cut to the real chat 1.2; reply readable about 1.6; pull-back about 3.4; begging reply in sequence 10.7; "100" 15.55; punchline reply 18.98; total 22.77 s.
- Judgement vs final7 (honest): BETTER for readability and first impression. In final7 the room, marble and hand were crushed to near-black, so the hook read as black text on a dark smear; in final8 black type on light plus a clearly lit phone/hand card reads instantly and moves from frame 0. WORSE or risky: the light hook is a style break against the dark recording (the transition goes light -> dark-blue picture -> black within 0.3 s; a viewer may feel one fast dimming), the lower ~300 px is empty light base, the picture is a 941 px still upscaled so the card is slightly soft/pixelated, and light-on-dark consistency with the rest of the video is lost. Not tested on a phone or with viewers.
- qa.py: same dark-UI blockers in the recording part as before; the hook itself is light so the first-frame luma blocker no longer fires.
Scores (judgements): HOOK 78 | VIRALITY 69 | OVERALL 73 | PREDICTED VIEWS ~800.

---
# FINAL9 (22.77 s) = final8 (light hook, recording, sfx, contrast lift) + background music bed
Files: video/ep90/out/ep90-final9.mp4 (default track B), ep90-final9-review720.mp4, ep90-final9-musicA-review720.mp4, ep90-final9-musicC-review720.mp4 (alternatives, A and C instead of the requested B/C names because the default is B), f0.png. Mix script: video/ep90/mixbed90g.py (decodes final8's sfx track, adds the shaped bed; one more AAC generation).
- Tracks (all real library, none of the three David rejected): B punchy--trending-instagram-reels-music--delosound (default), A punchy--hip-hop-beat--themountain, C cinematic--dramatic--themountain. Levels and numbers: channel/music-notes.md (90 final9 row).
- Bed shape: light under the hook, steady and a bit lower under the typing bursts, -7 dB under the begging reply, 0.5 s near silence before the punchline (impact lands on the return), groove back after it, soft fade with the picture. sfx kept (boosted so the bed does not bury them).
- Loudness: final9 -15.5 LUFS integrated, true peak -3.7 dBTP; the qa.py loudness blocker is gone for B (A would have been -16.4). Everything else (cut list, contrast lift, light hook) unchanged.
- Weak: music not heard by me (choice by measurements and by what David/Roni did not object to, which is exactly how the three rejected beds were chosen); hook scene audio is now bed + swell + thud, the swell is partly masked; the hip-hop and trending tracks are generic-stock family; alternatives are not level-matched to the final.

---
# FINAL10 (22.77 s) = final8 with the recording ENLARGED to the full frame, and NO music bed (David: bars at the sides; the bed does not fit, again)
Files: video/ep90/out/ep90-final10.mp4, ep90-final10-review720.mp4, f0.png. Builder: video/ep90/build90g.py (recording), hook scene = final8's (first 1.2 s stream-copied), audio = final8's sfx-only track (stream copy, -29.0 LUFS, peak -9.0 dBFS, no music). Cut list, typing speeds, funny ending, contrast lift, sfx unchanged.
- Framing: the 1206x2622 source is scaled to 1080 x 2348 (full width, no side bars, no letterbox; the old view was 884 wide). A 1920-px window is cut from it. The top 330 px of the scaled source (status strip, header icons and scrolled-away remnants) are always hidden, so the window can sit at offset 330 (replies, input pill still just inside the bottom) and eases to 350 while typing (small shift: 20 px over 0.45 s, smoothstep, at the typing bursts). No black or empty bars anywhere.
- The opening hold on the begging reply and the pull-back land on the SAME framing: because the full-width framing already spans the content edge to edge (reply text starts at x 22, the user bubble ends at x 1066), the old "1.2x zoom hold" is the same scale as the new fill (0.89 px per source px vs 0.88), so hold = filled framing, with only a 2% push-in. The pull-back is now only the rewind (chat scrolls back to the start); the zoom-out part is gone because there is nothing left to zoom out of.
- Push-ins during the replies, "100" and the laughing reply were reduced from 1.06-1.10x to 1.015-1.02x: anything more crops the bubble edge or the reply's left edge.
- Clipped content (honest): the keyboard's bottom row (globe and mic icons) and the bottom ~80-100 px below the space bar are cut off while the keyboard is up (needed to keep the first chat bubble and the input box in view); the idle input pill sits 3-10 px from the bottom edge, inside, but tight (and in the Instagram UI zone). Nothing with text is cut: bubbles, replies and typed text are fully visible in the frames checked (first 4 s, typing, replies, ending).
- Checked at full size/contact sheets: frame 0 (light hook), the cut at 1.2 s, the zoomed hold, rewind, a typing moment, the begging reply, "100", the laughing reply. Side columns black only where the real UI is black.
- Weak: the chat text is larger than before but the bottom third of every reply frame is empty black (the real UI has nothing there); keyboard bottom row cropped; the hold no longer has a real zoom (a hair of push-in only), so the "pull-back reveal" is gone; no music (by request) means the video is sfx-only and quiet (-29 LUFS), David adds the trending sound in Instagram; typing at 8-10x not followable letter by letter.
Scores (judgements): HOOK 78 | VIRALITY 69 | OVERALL 73 | PREDICTED VIEWS ~800.

---
# FINAL11 (23.03 s) = final10 WITHOUT the hook scene: frame 0 is the real recording (payoff on frame 0), real end card
Why (Meta AI read David's real account insights; its view numbers matched our studio data on 6 of 6 checks): reels that open on a real chat / screen recording with a specific first-person test and a visible result had skip rate 40-68% and about 13 s average watch; reels opened with a staged / illustrated / dark title frame had skip 80-91% and about 4 s. Its hook rules: specific person + action, a specific number, visual proof in the first 2 s, no AI-generated scene as the hook, a surprising result, a "send to" line. Our AI-generated phone-image hook scene (final7-final9) is exactly the type it warns about; our earlier blind panel also preferred the real zoomed chat frame. Evidence is from one account and an AI analysis: a hypothesis to test, not a proven law.
Files: video/ep90/out/ep90-final11.mp4, ep90-final11-review720.mp4, f0.png. Builder video/ep90/build90h.py (wording variables HOOK_LINE1/2 and END_L1/2 at the top). Full-screen recording, contrast lift, cut list, typing speeds, funny ending as final10; audio = final8's sfx-only track (recording part) + one small thud at frame 0 (-14 dBFS), -29.1 LUFS, peak -9.0 dBFS, no music.
- Frame 0 = the real begging reply "Wait... can I have a second chance?" and the user bubble "Now we won't be able to talk for 47 days", readable, held 2.2 s (slight push-in), then the 0.5 s rewind and the typing sequence.
- Hook text (heavy white Inter Display Black, tight, 117 px, two lines, fully visible from frame 0, soft fade 1.9-2.2 s): "I gave ChatGPT" / "a 47-day timeout." Position: x 68-1012, y 700-945, in the empty black area under the reply (the chat ends at y 440 in the hold). Real ChatGPT badge (icon alone, 110 px) kept at x 65-175, y 560-670, above the text, no collision with the chat or the text. Safe area x 65-1015, y 269-1248: both inside.
- End card: after the laughing reply has been held 2.0 s (reply readable from about 19.0 s, card from 21.03 s), "Send this to someone" / "who ghosts you." (96 px, same type, fade in 0.35 s) at x 68-1012, y 820-1000 in the empty black area; it fades with the video (last 0.5 s), card on screen about 2.0 s including the fade. No collision: the laughing reply and "Fahhhhh" bubble sit at y 30-460, the input pill at y 1790+.
- Checked: frame 0 full size, first-4-s contact sheet at 0.25 s, end card frame, text bboxes vs chat elements, no letterbox.
- Weak: the hook text still hides nothing but sits over a mostly black screen (as before); the opening hold is a near-still 2.2 s; wording "I gave ChatGPT a 47-day timeout" is plain but "timeout" may read as a child punishment to some viewers; typing at 8-10x not followable letter by letter; no music (by request), quiet file; keyboard bottom row cropped (final10 framing); first-frame black-level/qa blockers of the dark UI still apply; not tested with viewers.
Scores (judgements, now informed by the Meta AI evidence): HOOK 80 | VIRALITY 70 | OVERALL 75 | PREDICTED VIEWS ~900 (to be checked against the 48 h number).
- qa.py on final11 (honest): "picture frozen 4.53 s at 16.57-21.10 s" is a BLOCKER (the empty loading-dots wait before the laughing reply plus the 2 s reading hold of that reply, only the 1.02x push-in moves); the first-frame blank blocker is gone (frame 0 now carries the real chat). Not faked away; shorten the dots wait (8x already) or the hold if David wants it to pass.
