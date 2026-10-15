# Episode 70 — first video of the "viral format" test (BUILT and gated 15.10.2026)

**Format (the test variable):** David's own real ChatGPT iPhone screen recording (no face), shown as a phone card over a blurred,
teal-tinted background; plain-language lines; a pause frame with a ring on the real "Memory" row; our own voice and captions.
See `channel/experiments.md` (viral-format test, video 1 of 10) and `channel/reference-reels-15-10.md`.

## Product check
Verified against the LIVE APP (David's recording, 15.10.2026), NOT against OpenAI's help page (it returned HTTP 403 to my fetch).
Real labels on screen: sidebar > gear > "Customize ChatGPT" list (Personalization, Memory, Plugins); Memory screen: "Enable memory"
switch ("Let ChatGPT personalize your experience based on your chats, files, and connected apps. Memory may include sensitive info
you provide."), "Memory summary" ("View an overview of what ChatGPT has learned about you. ... You can still manage your old saved
memories."), Your nickname, Your occupation, More about you. UNCONFIRMED and NOT said: how long switched-off/deleted memories are kept,
whether turning Enable memory off removes anything already saved, Android/web differences.

## Spoken lines (v3, 29.4s, after David's second round of feedback 15.10.2026)
1. Never tell ChatGPT anything personal until you check what it keeps. (hook in a white text bar, ChatGPT icon inline; "what it keeps" states the problem: ChatGPT saves things; basis: the screen's own text)
2. It keeps a summary of what it learns about you.
3. Open the menu, top left. (home screen, ring on the menu button)
4. Then press the gear at the bottom. (side menu, chats blurred, ring on the gear)
5. And open Memory. (Settings, ring on the Memory row; email and phone values blurred)
6. The screen even warns it may include sensitive info you provide. (ring on that text)
7. Switch it off if you don't like that. (ring on Enable memory)
8. Send this to someone who uses ChatGPT.
9. The setup's in the link in bio. (locked)
10. Follow for the setup that actually works. (locked)
Changes from v2: each step is its own scene on the real screen, no more sliding transitions; the pause frame was dropped; blur only on chat titles, email and phone values; "tap" was misheard as "top" by the transcript, so the steps use "press" and "open".

## Privacy
David's raw recording is NOT in git. Email, phone number and recent chat titles were blurred with a real Gaussian blur (v2; v1 used a mosaic) on every frame
where they appear, including the slide-in moment (whole frame masked 2.8-3.4s of the source); full name and "DP" initials are left
visible by David's decision (already public on his profile). Masked 303 frames live only in the working copy
(`channel/assets/ep70-screen/`, git-excluded), so `video/reel-70*.html` cannot be re-rendered from a fresh clone without the recording.
Checked by eye twice on the final MP4 (a 5 fps sheet of the whole file and a 10 fps crop of the sensitive seconds); there is no OCR here.

## Build facts
29.4s, accent #2DD4BF (teal), mood 'urgent', ChatGPT icon (white inverted version of ep63's real SVG), gate: ALL CHECKS PASSED.
Known soft warnings: length 24s is under the usual 30-90s band (deliberate for the test); picture nearly still ~2s in a few places.
The accent heuristic flagged lines 5 and 7 on many rolls; the shipped take cleared it.
Hook type: Direct address / curiosity ("learning about you" + "you can see it").
