# Episode 69 — iPhone notification summaries (first "pause-frame" test of the 13.10 growth plan)

Drafted 13.10.2026. NOT built, NOT approved: needs David's OK on topic and lines, then photos, voice, render, gate.
Context: `channel/growth-research-13-10.md` (diagnosis + plan). Episode 68's draft already promises 69 = iPhone
notification summaries, so the promise chain holds if 68 ships first.

## Why this topic (data, not taste)
- YouTube Shorts scan (13.10, 36 Shorts, search-biased): the biggest were concrete "turn off/hide/fix X on iPhone/WhatsApp"
  (hundreds of thousands to 1.7M views); fear-style "your phone is listening" sat at ~5-50. HYPOTHESIS: a specific
  problem + exact fix beats an alarming claim. Not yet shown for Instagram.
- Everyday product (iPhone), AI is the substance (Apple Intelligence rewrites notifications), concrete fix (3 taps).
- Not a repeat: 58 WhatsApp touch-up, 60 Meta AI ads, 61/65/67 Google, 62 ChatGPT, 66 Amazon. Apple is new to the run.

## The built-in device (the new part)
One **pause frame**: the 3-tap path sits on screen, held ~2 seconds with "Pause here", so it can be frozen, screenshotted
and sent. Purpose: replay/save/send, the signals our Reels have at ~0. Same idea as the reference reel (a hidden frame
that needs a pause), but our own content and our own payoff. No discount, no DM bait, nothing sold.
Test target: sends, saves, skip rate, average watch time vs length. Not "views alone".

## Claims verified live (13.10.2026)
- Apple Support, iPhone User Guide (iOS 27 page, support.apple.com/en-za/guide/iphone/iph1fbe7d2b9/ios): "Your iPhone can
  summarize long or stacked notifications." Steps: Settings > Notifications > Summarize Notifications, then turn it on or
  off; "Choose Notifications to Summarize" lets you pick apps. Needs an Apple Intelligence-enabled iPhone 15 Pro, 15 Pro Max
  or any iPhone 16 or later; "not available in all languages or regions".
- Engadget, 4.10.2026 (secondary): on iOS 27 there is no longer one master switch for all of Apple Intelligence, but the
  path above still works (iOS 26 still has the master switch).
- Real error, widely reported (BBC complaint Dec 2024; Apple paused news-app summaries Jan 2025): a summary declared
  Luke Littler the darts winner before the final was played; another falsely said Luigi Mangione had shot himself.
  Use the darts one only (lighter, same fact pattern). Sources: Jersey Evening Post, Irish News, Mediaite, LBC (secondary press
  repeating the BBC/Apple statements).

## UNCONFIRMED, must NOT be said
- That news summaries are back and with what warning text (only one secondary source said iOS 26 returned them with a
  "may change the meaning" warning; re-check on Apple's own page before any line mentions it).
- Which countries/languages get it beyond Apple's own sentence; how often summaries are wrong today; Belgium-specific
  availability (say "on iPhone 15 Pro or newer").
- Any claim that a summary of the viewer's own messages was wrong.

## Spoken script — FINAL (as built and shipped through the gate, 13.10.2026)
Changes from the approved draft, all forced by the voice gate or the pause frame: line 1 now says "...and it has gotten them wrong" (the draft's "before you read them" was flagged by script_lint), line 2 "That's the AI built into your iPhone." (no brand word that the voice swallows), line 3 "...won the darts final, and the match hadn't started.", line 4 passive ("it was paused"), line 5 "in seconds" ("three" bursts on this voice on every roll, and "a few taps" was heard as "tabs"), line 8 "It works on iPhone 15 Pro and up.", closing "keeps" (not "saves").
1. Your iPhone rewrites your notifications, and it has gotten them wrong.
2. That's the AI built into your iPhone.
3. Once, it said someone had won the darts final, and the match hadn't started.
4. After the BBC complained, it was paused for news apps.
5. You can check it in seconds. Pause here.
6. [PAUSE FRAME ~4s, three lines] Settings. / Notifications. / Summarize Notifications.
7. Switch it off, or pick which apps it can touch.
8. It works on iPhone 15 Pro and up.
9. Send this to someone who only reads the preview.
10. The setup's in the link in bio. (locked)
11. Follow for the setup that actually works. (locked canonical clip; David chose the standard ending for 69, so no promise about episode 70 is made)

Build facts: 37.4s, accent #FB923C, mood 'confident', photos ep69-scene-a..d (Unsplash), Apple logo from Wikimedia Commons (ep69-apple-logo.svg), ChatGPT logo reused from ep63. Gate: ALL CHECKS PASSED; two watches (frames + transcript) done; one pause-frame layout defect found and fixed (4 lines -> 3). Known soft warning: picture nearly still 2.5s at 1.4-3.9s (hook).

Hook type: Direct Address / stakes. Check `hooks-guide.md` log (rows 64-68) for the previous type before building, and read
lines 1-2 cold for the dry-sentence test. Feel-it-in-3-seconds check: every iPhone owner with the feature on has read a
stacked summary; the darts line is the proof beat.

## Production notes
- Real logos icon-only: Apple (and Settings icon), sourced from Apple's own marketing/press page, not redrawn.
- No face. Real photo backgrounds per standing rule; face-detection pre-check on any photo with a person.
- The pause frame must be a real full-bleed card with the path in large text, inside the safe area (y 269-1248), static 2s.
- Music from the real library; `produce.sh` with a mood different from the last shipped episode.
- Setup guide (`/e/69` steps[]) is mandatory: numbered taps with Hebrew-irrelevant English labels as shown on the phone.
