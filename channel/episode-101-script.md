# Episode 101 - silent scroll of a real chat ("47 days")

Publish mode: REGULAR (default, not yet confirmed with David; check he has not posted by hand before any publish)
Build: video/ep101/hf/index.html (HyperFrames, 1080x1920, 14.5 s, NO voice, music bed only). Final: video/ep101/out/ep101-v1.mp4 (review copy ep101-v1-review.mp4, 720 wide, crf 27).

## TOPIC verdict
Same real chat as episode 90 (ghost test, 13.11 trial), redesigned as a silent scroll reel: the AI is begged for a second chance, is told it can have one, and picks 100 again. A stranger gets it in one read: ChatGPT, a number, a punishment, a joke on the AI. Proof is the real screenshot, no invented line. Weakness: it is the "AI does something odd in a chat" class David is bored of; the change is the FORM (silent, one slow scroll, one held punchline), not the topic. Treat it as an experiment.

## Source and honesty
Two real iPhone dark-mode ChatGPT screenshots from David, stitched (overlap found by row matching, offset 506 px, mean seam diff under 1 grey level, cut in an empty gap row). Status bar, top buttons, share popup, composer and scrollbar column removed. Content not retouched. All chat lines are real: "Choose a number between 0 and 100" / "47" / "Now we won't be able to talk for 47 days" / "Wait... can I have a second chance?" / "Yes" / "100" / "Fahhhhh" / "HAHAHAHA You gave me a second chance and I STILL chose 100".
Hook text (ours, present tense): "ChatGPT picks a number." / "I cut it off." ("cut it off" = the user says they will not talk to it for 47 days).
Contrast (WCAG, measured on the stitched image): user bubble text 16.9:1, replies 21.0:1. High, so NO lift applied (unlike ep92).

## Timing
0-2.2 s hold on the opening exchange (first user message and "47" visible at frame 0). 2.2-12.0 s one scroll of 1180 px, sine in-out (one long eased curve). 12.0-14.5 s hold on the punchline (2.5 s). Hook stays, chat never covered (hook sits y 292-440, chat starts below).

## Build-up beats (what is new here)
1. 0 s: prompt and the answer 47 (the proof, the setup).
2. 2.2 s: "Now we won't be able to talk for 47 days" (new: the threat).
3. about 5 s: "Wait... can I have a second chance?" (new: the AI begs).
4. about 7 s: "Yes" then "100" (new: the number came back, the viewer sees the trap).
5. about 9 s: "Fahhhhh" (new: the user reacts).
6. 12 s: the AI laughs at itself, held 2.5 s (payoff).
Weak spot: beats 2 to 5 are slow (about 2 s each); a blind reader may scroll in the middle.

## Scores (judgements, labels only)
HOOK ~62 (stated subject at once, no stake in the words), VIRALITY ~60, OVERALL ~62. Predicted views 300-1,000 (guess; scale score 55-65). Log real 48 h / 72 h in channel/score-calibration.md.

## Not done / unchecked
Blind-reader test on frame 0 not run. Music measured, not heard. Safe-area check done by pixel measurement of the last frame (chat content x 108-967, punchline y 925-1030, so left of 972 and above the right-button band at y 1056); DOM safe_check.js not applicable (the text is an image).
