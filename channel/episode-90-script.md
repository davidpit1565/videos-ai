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
