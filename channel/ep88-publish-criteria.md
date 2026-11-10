# Episode 88: when may it be published without David watching first (David, 10.11.2026, ~03:00)
David sleeps and wakes at an unknown time. Rule he gave: improve it until I am CONVINCED he would approve; only then publish to Instagram AND YouTube (skipFacebook: true). If in doubt, do not publish: leave the playable review page for him.
"Convinced" means ALL of these hold on the final cut (checked several times, on frames across the whole video, not only frame 0):
1. REAL, NOT AI: in a blind side-by-side with the reference reel DeJ_gTHs-FB (3 fresh readers: teen, builder, parent), at least 2 of 3 say ours reads as a real handmade paper collage and give realism >= 70/100.
2. MOTION: measured scene-change rates reach at least 70% of the reference (reference: 7.4/s at >0.01, 4.1/s at >0.03, 2.4/s at >0.08).
3. READABLE: every text strip legible >= 0.6 s at 360 px wide, <= 3 lines, no strobing, no overlap (builder verdict plus my own look at frames).
4. CLEAR IN 3 s: blind readers say the subject is clear within 1-3 s and the hook scores >= 80.
5. TRUTH + GATES: only verified claims, check_hf all green, accent clean, captions/youtube/script/articles/credits match, photos CC0 with credits.
6. SHIP: merged to main, deploy status success, live content-length equals the file in git.
If any item fails after the round, iterate again (new round) until it passes or until David is awake. Never publish on a failed item.
Publication steps when criteria pass: unlock studio with the PIN from the chat (never written anywhere), POST /api/instagram/publish {episode:88, skipFacebook:true}, YouTube via /api/youtube/publish or /api/yt-backfill?episode=88&max=1, log in content-memory.md and score-calibration.md, schedule 48/72 h readings, PushNotification (Hebrew), report to David.
