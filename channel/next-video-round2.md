# Next video, concept round 2 (9.11.2026)
Constraints: not ChatGPT, few screen recordings, not an existing topic (86 titles checked), hook/virality 95, value 90, overall 90. All scores are judgements; the panel is fresh agents playing three viewers (17-year-old iPhone user, 28-year-old AI builder, 40-year-old office worker with kids), not measurements.

## Panel result on 7 hooks
Best two: (1) 'Google can tell you if a photo is AI.' (works across all three viewers; send-to: mum or a friend who falls for fakes) and (7) 'Facebook asks to scan photos you never posted.' (best with older viewers; the word 'scan' over-promises: the verified fact is an opt-in 'Camera roll sharing suggestions', in the EU/UK, Meta says media is not used for AI or ads unless shared). (3) 'A screenshot erases the Made with AI label' had the best curiosity gap and was surprising to builders but gave nothing to act on. (2) TikTok less-AI slider only for TikTok users; (4)-(6) listicles/student topics rated old or narrow; (5) transcript hook weakest.

## Verified facts (live, 9.11.2026)
- Gemini can check whether an image was made or edited by Google AI (SynthID watermark): support.google.com/gemini/answer/16722517. No watermark does NOT prove a photo is real (other AIs are not detected). About 10 checks per 24 h; Android and web, iOS 'soon' (check the current status before scripting). We cannot run Gemini here: show the steps, never an invented result.
- Our own test (real, small): a signed C2PA sample image lost its Content Credentials in 4 of 4 ordinary re-saves (JPEG q95, resize+q70, PNG, ffmpeg). It was a test fixture, not a real AI image, and not the real apps.
- Facebook camera roll sharing suggestions: about.fb.com, 16.4.2026 (updated 31.8.2026): opt-in, EU/UK and 8 other countries, Meta says the media is not used for AI or ads unless you share it.
- Unconfirmed: Apple 'Enhanced Visual Search' default state, TikTok AI slider rollout, Samsung on-device setting.

## Honest ceiling: HOOK about 84, VIRALITY about 80, VALUE about 85, OVERALL about 82. None reaches 95/95/90/90.

## Full agent reports

### REPORT-B.md
# REPORT-B: tests we can run ourselves (9.11.2026)

## Test I RAN (real result)
Label-survival test. Source: C2PA's own signed sample CA.jpg (a test fixture from contentauth/c2pa-rs, NOT a real AI image). Checked with the c2pa-python reader.
- Original: Content Credentials found (manifest present).
- Re-saved JPEG q95 (PIL): gone. "No JUMBF data".
- Shrunk to 1600px, q70 (WhatsApp-like, my approximation, not the real app): gone.
- PNG copy (screenshot-like): gone. ffmpeg re-encode: gone.
Result: 4 of 4 ordinary re-saves removed the label. Caveat: not yet run on a real AI image (Firefly, Gemini, OpenAI) or through the real apps. Files: scratchpad/next90/testB/.
Also checked: HIBP range API works from the container. "P@ssw0rd123!" seen 30,430 times, a random-looking string 0 times.

## 5 candidates
1. **AI label survives? (RAN, see above).** Nearest: ep 77 (map pin in photo), different: AI labels, not location. Feasible today. Needs one real AI image with credentials to be publishable. Surprise: the "Made with AI" label is a note on the envelope, one screenshot removes it.
2. **AI passwords.** Steps: 30 fresh, independent Claude/ChatGPT-style runs of "give me a strong password"; count repeats, patterns (starting letter, "@", "!", year), check each by SHA-1 prefix in HIBP (tested working). Surprise if many share the same shape or are found in breaches. Feasible with sub-agents (I have none here; the parent does). Nearest: none. Risk: results may be boring (random-looking = 0 breaches); only publish if repeats show.
3. **Free AI detector vs our own text.** Write/generate 10 texts, run through 3 free detectors. Detectors have no API/need browser: not feasible without Playwright (it failed to connect). Skip for now.
4. **Voice clone, how few seconds.** Nearest ep 38 (ten seconds). Duplicate topic. Reject.
5. **What 5 AI sites send about you.** curl the HTML of 5 AI homepages, list third-party domains. Without JS execution this undercounts; cheap but weak. Needs headless browser. Park.

## CONCEPT (from #1): "Made with AI" label deleter
- Spoken hook (8 words): "A screenshot erases the 'Made with AI' label."
- First frame (drawn, light + lime): big phone-photo card with a lime "AI-GENERATED" badge (real logo of the generator used, e.g. Adobe Firefly/Google); beside it a scissors-free arrow "screenshot" pointing to the same photo with the badge gone. Words: "Made with AI -> screenshot -> label gone."
- Beats (40-45 s): (1) badge on, tick; (2) 4 drawn rows, our real test: re-save, shrink, PNG, ffmpeg, each flips green "label: YES" to red "label: GONE"; (3) why: label is metadata, picture unchanged; (4) what to do instead: 3-item checklist (look for the source account, reverse image search, ask for original file) as the SAVE card; (5) close: "Send this to the one who shares 'real' photos."
- VALUE card: "3 checks when a photo has no label" (screenshot-able).
- Named person: your uncle/aunt who forwards photos in the family chat.
- Watch twice: the 4 rows flip fast; a last-frame badge is missing and the loop returns to the badge-on frame.
- 30-second check: viewer opens any C2PA verifier (contentcredentials.org/verify), uploads an image, then screenshots it and uploads again. Must verify live before script (rule: product still real, how Google/Meta label now).
- Built without screen recordings: drawn UI, our test table, real logos.
- Nearest existing: ep 54 (deepfake test), ep 77. Different: nobody covers that labels are removable.
- Honest scores: HOOK 82, VIRALITY 80, VALUE 85, OVERALL 82. Reasons: subject shown at once, concrete test, but "label" is abstract to a lay viewer, felt stake only moderate. Does NOT reach 95. Could rise if the example photo is a famous fake the viewer already saw (needs a real, checkable one).

## Candidate #2 concept, short
Hook: "Ask AI for a password. Thousands got the same one." (do NOT say this unless the data shows it; placeholder). First frame: password field with an AI logo, a typed password, red "FOUND IN BREACHES: x" counter. VALUE: 3-step safer path (password manager generate, passkey). Named person: dad who reuses a password. Scores if result real: HOOK 85, VIRALITY 82, VALUE 88, OVERALL 83. Nearest: none in titles (ep 59-ish privacy topics only).

## Blind tests
No Agent tool here, not run. Prompt for the parent: show only the first-frame description + hook, ask persona (teen, parent, 40s office worker) "what is this about / would you stop / why / who would you send it to".

## Honest verdict
Nothing here reaches 95/95 yet. #1 is real and proven in a lab; the missing piece is a strong, felt, real example photo. #2 depends on a result we haven't measured.

### REPORT-C.md
# REPORT-C (structure-first), 9.11.2026
Structures chosen: (A) LIST of N, real result in first 6 s, comment/save close (@david_knowsai). (B) LADDER, each level = cause + one fix, ends as screenshot-able card (@ekkobuild). Dropped: spot-the-fake (no image generator in this container; would need David to generate).
Verified live today: NotebookLM was renamed "Gemini Notebook" (16.7.2026, Google blog); its Studio panel has Flashcards/Quizzes, easy/medium/hard, CSV download (support.google.com/gemininotebook/answer/16958963). iPhone Voice Memos transcript: iPhone 12+, More > View/Copy Transcript (Apple guide, iOS 26/27). Clean Up in Photos: iPhone 15 Pro/16+, Apple Intelligence (support.apple.com/en-us/121429). UNCONFIRMED, re-check before scripting: Gemini Notebook free tier, Google Photos Magic Eraser free, Live Text, subject lift.
Local tools here: faster-whisper, Chatterbox voice, ffmpeg, pillow. No local LLM, no image model.
Blind-test: no Agent tool in this run. Prompt for 3 personas (16yo student, 45yo parent, 70yo): "You see ONLY this first frame + hear this line: [hook]. 1) What is this video about? 2) Would you stop scrolling, why? 3) Who would you send it to?"

## C1 LADDER: "Why your voice transcript is wrong" (best fit)
- Hook (8): "Your phone's transcript of your lecture is wrong. Here's why."
- Frame 1: drawn iPhone Voice Memos screen, a sentence with 2 red words, logo.
- VALUE card: "5 reasons transcripts fail. 1 Noise: record in a quiet room. 2 Distance: phone within 30 cm of the mouth. 3 Echo: soft things in the room. 4 Speed: pause between sentences. 5 Names/numbers: check them by hand. Copy: Voice Memos > recording > More > Copy Transcript."
- Person: the friend who records lectures. Watch twice: levels' word-error numbers pass fast; hook sentence is re-read at end with 2 words fixed.
- Check in 30 s: stated path in Apple's guide. Test: OUR run, same sentence through ffmpeg-degraded copies (noise, echo, speed) into Whisper, real error counts. Honest label: Whisper, not Apple's engine; numbers describe the cause, not Apple.
- Built: drawn UI, our audio, pillow/HTML cards. No recordings.
- Nearest: 56 (headphones translate), 11 (narration flaw). Differs: nothing on transcription.
- Borrowed: ekkobuild ladder + cheat sheet; new: measured by us, audible.
- Scores: HOOK 80 (felt stake only for students), VIRALITY 75, VALUE 85, OVERALL 80.

## C2 LIST: "6 apps your iPhone replaces" 
- Hook (9): "Stop paying for these 6 apps. Your iPhone does it."
- Frame 1: six drawn app icons crossed out in lime, title. (Real logos only of apps we name; verify each.)
- VALUE card: six lines "Job > built-in > path" e.g. remove object > Clean Up > Photos > Edit > Clean Up (iPhone 15 Pro+); transcript > Voice Memos > More > View Transcript; plus 4 more to verify (Live Text, subject lift, Notes scan, Translate). Android twin on last line.
- Person: the friend paying for photo/scanner apps. Twice: card is fast, last line reveals the 6th.
- 30-s check: every row has an Apple support page. Built: drawn UI.
- Nearest: 58, 69, 57 (single phone-AI features). Differs: a list of replacements.
- Borrowed: david_knowsai list, 6 beats of ~6 s (about 40 s). Risk: iPhone-only audience, hardware limits, "result visible" is drawn, not real output.
- Scores: HOOK 82, VIRALITY 80, VALUE 88, OVERALL 82.

## C3 LADDER-STEPS: "Lesson to quiz in 5 steps" (Gemini Notebook)
- Hook (9): "Turn your lesson into a quiz in 30 seconds."
- Frame 1: drawn Studio panel, Quizzes button lit, "was NotebookLM".
- VALUE card: 1 Open notebook.google, new notebook. 2 Add your notes/PDF. 3 Studio > Quizzes (pencil to set hard). 4 Answer, tap Explain on misses. 5 Flashcards > Download CSV.
- Person: classmate before the test. Twice: step 4 hint. Check: Google help page. Test: none runnable, UI drawn, say so; need free-tier check.
- Nearest: 19 (Claude keeps files). Differs: study use, other product.
- Scores: HOOK 78, VIRALITY 72, VALUE 88, OVERALL 77.

## C4 LADDER: "Why AI voiceover sounds fake" (audible proof)
- Hook (8): "Hear the difference? Same AI voice, one fix."
- Frame 1: two waveforms, "A / B", real clips we render.
- VALUE card: 5 fixes (short sentences, commas for pauses, numbers as words, no ALL CAPS, swap swallowed words), each measured with voice_quality.py. 
- Person: friend who makes videos. Twice: replay A vs B. Check: viewer pastes own text.
- Nearest: 11, 24, 38. Differs: fixes for the viewer's own tool. Local model only: say so.
- Scores: HOOK 75, VIRALITY 65 (niche), VALUE 82, OVERALL 72.

## C5 LIST: "5 free things Gemini Notebook does with a PDF"
- Hook (9): "One PDF in, five study tools out. All free?" ("free" unconfirmed: drop until verified.)
- VALUE: quiz, flashcards, audio overview, mind map, report (names to verify). Overlaps C3; keep only one. Scores: HOOK 72, VIRALITY 68, VALUE 80, OVERALL 72.

## C6 PIPELINE: "Record a lecture, get notes, no app"
- Hook (9): "Record any lecture. Get the notes. No extra app."
- Steps: Voice Memos record > transcript > Copy Transcript > Writing Tools summarize (Apple Intelligence iPhone 15 Pro+).
- Overlaps C1/C2; use as C1's payoff card. Scores: HOOK 74, VIRALITY 70, VALUE 84, OVERALL 76.

## Honest verdict
No concept reaches HOOK 95 / VIRALITY 95 on my own scoring. Best: C2 and C1 (merge: C1 ladder inside a "your phone" frame). The 95 bar needs a visible surprise with REAL output; ours would be drawn. Rename to Gemini Notebook is a real hook for students, not for a general audience. Prices/free-tier claims not verified: do not script until checked.
