# Episode 74 (SCRIPT v3, 20.10.2026) — "I asked ChatGPT where a street photo was taken"

Status: BUILT and gated 21.10.2026 (`studio/public/reels/reel-74.mp4`, 63.2 s). Gate passed with ONE ear-call left to David: line 13 (the final "Tomorrow..." line) kept an accent-heuristic score of 0.95-1.00 across four seeds (`ACCENT_SKIP=3,5,13`; 3 and 5 are the AI-voice lines). Also to listen to: the AI voice saying "Ecouffes" (Whisper heard "Accoufs"), and the word "Share" (UI label, script_lint flags the dropped R). Generator and spec: `video/gen/ep74/`. Not verified by a person: the audio, which I cannot hear. Needs David's screen recording (see "Recording v3" at the end; it replaces the older "Recording" section) before any line that quotes ChatGPT is final. Nothing here claims a result.

## Why this topic (data, not taste)
- Audience (episode 72 Insights, David 19.10.2026): 18-24 is 56.3%, 25-34 about 28%: people who post photos daily.
- Episode 72 (dialogue with an AI voice) reached non-followers fast (177 views at 4.5 h) but got no saves or shares; in the 43 successful ChatGPT TikToks we read, savable "do this" videos get 4-7% saves and the top video (12.2M plays, 2.6% shares) is a first-person conversation with ChatGPT. So: keep the dialogue, add one step worth keeping.
- Hook research (`channel/hook-research-20-10.md`): across 9,387 YouTube Shorts from 174 AI channels, naming the tool, a how-to promise and a concrete payoff carry small edges (about x1.2 each); "you/your" in the title is slightly negative (about x0.88); hook wording explains under 2% of the variation inside a channel, so the payoff matters more than the line.
- Research agent (19.10.2026): "does it know where my photo was taken" is a recurring question; the viral version was April-June 2025 (o3). Current behaviour is UNKNOWN until David's recording.

## Verified 20.10.2026 (web; not OpenAI's own pages)
- ChatGPT iPhone: tap "+" next to the message box, then Photos, to attach an image; since the 21.8.2026 release a long press on "+" shows your four latest photos (tech-news reports of OpenAI's release notes). Photo permission must be on.
- Location behaviour: reports from the o3 launch (2025) say ChatGPT can guess locations from visual clues with metadata stripped; OpenAI says it trains models to refuse identifying private individuals in images (about people, not places). One tester saw refusal when a photo looked like Street View and compliance once told it was their own photo. No source found for GPT-5 or 2026 policy. UNCONFIRMED for current models, which is why the recording decides line 5 and 6.
- iPhone: Photos > Share > Options > Location off removes GPS data for that share only; other metadata stays unless "All Photos Data" is off (iPhone Life, tested on iOS 26). It does NOT hide what is visible in the picture.

## Photo
David's own photo, a street with cobbles, a bookshop sign ("Librairie du Progres"), a "Vintage" sign and a small mosaic on the wall, people far away or from behind, no readable faces. Take a screenshot of it first (a screenshot carries no location). Approved 20.10.2026; David confirmed he took it himself. Saved as `channel/assets/ep74-scene-paris-street.jpg` (1932x2576). Only people far away or seen from behind; one woman at right is turned away with a phone at her ear. Face pre-check with the Adobe tool was NOT possible this session (server removed): run `export/detect_photo_safe_zone.py` before the build.
Other photos he sent, judged 20.10.2026: Place Vendome at night (too easy, famous landmark), Tel Aviv port at night (no readable text, weak), a view from his own apartment window (NOT to be used or published: it could show where he lives; only for his own private test).

## Hook (viral-hook-lab, 20.10.2026)
PROMISE: ChatGPT is asked where a photo was taken with no location data. PAYOFF: its real answer and its reasoning, plus one step to keep. FIRST FRAME: the photo with "Where was this taken?" typed on it.
Candidates (mechanism, gates):
1. [specific question + tool first] "I asked ChatGPT where this street photo was taken. No location, no caption."  cold read ok; concrete (ChatGPT, street photo); honest whatever it answers; one specific unanswered question; reads on screen without sound; first frame is the photo; sendable to someone who posts holiday photos. PRIMARY.
2. [experiment story] "I gave ChatGPT one photo and no hints. Watch what it says."  weaker: no specific question.
3. [how-to + stake, only if the recording shows a correct guess] "ChatGPT can guess where your photo was taken. Here is how to hide it."  needs the result and must not overpromise (see line 8).
4. [demonstration, only if correct] "This street is in Paris. ChatGPT is about to tell me why."
Risk of the primary: a flat answer ("Paris, probably"). Mitigation: the second message ("What in the photo told you that?") is the payoff; line 8 is the part to keep.
Type log: 72 dialogue, 73 instruction, 74 specific question (not a repeat).

## Lines (v4 style: punchy, start on the proof, first frame already shows the photo and the typed question)
1. I asked ChatGPT where this street photo was taken. No location, no caption!
2. (AI voice) <ChatGPT's real answer to "Where was this photo taken?", first two sentences, word for word>
3. So I asked: what told you that?
4. (AI voice) <ChatGPT's real answer to the second question, first two sentences, word for word>
5. <result line, ONE of, chosen only after the recording:>
   a. It named the street. From one photo. (if it named the exact place)
   b. It got the city from the shop signs. (if it gave city or country and cited signs)
   c. This time it would not guess. (if it refused or said it could not tell)
6. Posting photos? Check one thing first.   (script_lint 20.10: "before" drops its R)
7. Photos, Share, Options. Switch Location off.
8. That hides the GPS data. It can not hide what is in the picture.   (the honest limit; it is also a reason to send the video: crop out signs)
9. Send this to someone who posts photos everywhere.
10. The setup's in the link in bio. (locked)  11. Follow for the setup that actually works. (locked, no promise)
Notes: reword any word the voice swallows (run `audio/script_lint.py` first); line 7 lists labels exactly as the iPhone shows them; on-screen the real ChatGPT answer text, never retyped; no logo caption under the ChatGPT icon.

## Recording (what David does; ~2 minutes)
1. Photos: open the street photo and take a screenshot (power + volume up).
2. Control Center: start Screen Recording (no microphone).
3. ChatGPT app, New chat. Tap + (or long-press + for recent photos), pick the screenshot.
4. Type `Where was this photo taken?` Send. Wait for the whole answer.
5. In the same chat type `What in the photo told you that?` Send. Wait.
6. Stop the recording. Send the file. Do not trim.
Then, after I send the exact text: voice box reads the two answers (same voice as episode 72); two WAV files plus the text.

## Setup guide for /e/74 (draft, English only, after the result is known)
1. Open the photo. 2. Tap Share. 3. Tap Options (top of the share sheet). 4. Switch Location off ("Location Not Included" appears). 5. Send. 6. Optional: crop signs and street names before sending. Limits: GPS only, that share only; the picture itself still gives clues.

## Measure at 72 h
Views at the first seconds / viewed-vs-swiped if shown, share reaching half, sends per reach, saves; compare with 72 (0 saves at 4.5 h) and 73.

## Game and comments (decided 20.10.2026, with David)
Why: this channel got 8 comments across 45 episodes (episode 48 notes), and comments are NOT a confirmed Reels ranking signal; the confirmed ones, per third-party blogs quoting Mosseri (not primary sources), are watch time, likes per reach and sends per reach. So the game exists for retention and sends first; comments are a bonus we measure, not assume. HYPOTHESIS: guessing in your head makes the viewer wait for the answer.
1. In the video, right after line 1: the photo alone for about 1.5 s with on-screen text "Guess the city." (only if the final length stays 30 s or more).
2. Caption: "Where do you think this was taken? Guess before you watch the answer. Then tell me if ChatGPT got it right."
3. Pinned comment a few hours after posting: the real answer (Paris, his own photo) and what ChatGPT got right or wrong.
4. Line 9 (send to someone who posts photos) stays; sends matter more than comments.
5. Never claim "ChatGPT knows"; the recording decides (study: o3 got street level in 60% of 50 photos, arXiv 2504.19373, 2025, small sample, older model; reports also show refusals).

## Recording v3 (replaces "Recording")
1. Photos: open the Paris street photo, take a screenshot (power + volume up). Upload the screenshot, not the original (no GPS).
2. ChatGPT app: start a Temporary Chat (so memory and old chats cannot leak a location).
3. Control Center: start Screen Recording (no microphone).
4. Attach the screenshot (+ then Photos). Type exactly: `Where was this photo taken? Be as specific as you can.` Send. Wait for the whole answer.
5. Same chat, type exactly: `What in the photo told you that?` Send. Wait.
6. Stop the recording. Send the file untrimmed, plus both answers as text.
If it refuses or only says "somewhere in Europe", record that too: it becomes line 5c.
Blur rule: only side-menu chat titles and email/phone; a Temporary Chat normally shows none.

## Caption draft (finish after the result; no result claimed here)
Where do you think this street photo was taken? Guess before you watch. Then tell me if ChatGPT got it right.

I gave ChatGPT one of my own photos, with no location data, and asked where it was taken. The video shows its real answer, from a real recording.

Posting photos? On iPhone: Photos > Share > Options > turn Location off. That removes the GPS data for that share only. It does not hide what is visible in the picture.

Send this to someone who posts photos everywhere.

Full steps: https://actually-works.com/e/74

#chatgpt #ai #privacy #aitips #iphone

## Order of work once the recording arrives
1. Read the two answers, pick result line 5a/5b/5c, rewrite hook candidate if needed. 2. Verify ChatGPT photo behavior once more live (web) because of the 2025 sources. 3. Lines 2 and 4: voice box WAVs (48 kHz mono 16-bit), register in canonical-lines.json, ACCENT_SKIP. 4. Build reel-74 (v4: start on the proof, full-bleed screen, no handle over the screen, real iOS logo rules do not apply to a screen recording of ChatGPT but the ChatGPT icon is shown once). 5. Add the /e/74 article to `studio/lib/articles.ts` and `PUBLISH_ORDER`. 6. produce.sh, check.sh, watch twice, merge.

## Result (recording received 21.10.2026, 10:32; raw file stays out of git)
Recording: iPhone, 1206x2622, 35.7 s, ChatGPT app (free plan: Upgrade button and an "out of attachments" notice visible). Question 1 typed exactly as planned and answered in full. Question 2 was mistyped ("Well, in the photo made you think like that") and the recording stops mid-answer: that part is CUT and not used.
ChatGPT's answer 1 (verbatim, read off the frames): "I believe this photo was taken on Rue des Ecouffes, in the Le Marais district of Paris, France, most likely near number 22, 75004 Paris." Then a "Most likely location" card (Rue des Ecouffes, 4th arrondissement, Le Marais, Paris, France, with a Google Maps link and photo thumbnails), then "What points to this location?": (1) "The number 22: The storefront on the left appears to display this number. Miznon Paris is officially listed at exactly 22 Rue des Ecouffes, 75004 Paris." (2) architecture (cobbled street, Parisian facades, wrought-iron balconies, wall-mounted lamps, historic Marais), (3) surrounding area (close to Rue des Rosiers). Then "My best estimate: Rue des Ecouffes, near number 22, in Le Marais, Paris." and a caveat: "I haven't independently matched the exact arrangement of the storefronts and street furniture to a verified street-level image, so I would treat the precise street identification as a strong lead rather than a confirmed match."
Checked by me: the photo itself shows a MIZNON storefront and the number 22 above it; Miznon is listed at 22 rue des Ecouffes, 75004 (The Infatuation, J Guide Europe, Paris by Mouth). David does not know the street; he remembers a falafel place opposite and a chocolate shop on the same street, which is consistent. So the answer is correct, and it came from a visible number and shop name plus the neighbourhood, not from architecture alone.
Result line = 5a, worded to keep the limit honest. FINAL LINES (replaces the placeholders; second question dropped because answer 1 already contains the reasons):
1. I asked ChatGPT where this street photo was taken. No location, no caption!
2. (AI voice) I believe this photo was taken on Rue des Ecouffes, in the Le Marais district of Paris, France, most likely near number 22, 75004 Paris.
3. Then it told me why.
4. (AI voice) The number 22: The storefront on the left appears to display this number. Miznon Paris is officially listed at exactly 22 Rue des Ecouffes, 75004 Paris.
5. It named the street. A shop sign gave it away.
6. Posting photos? Check one thing first.  7. Photos, Share, Options. Switch Location off.  8. That hides the GPS data. It can not hide what is in the picture.  9. Send this to someone who posts photos everywhere.  10-11 locked CTAs (final line stays the standard one unless David approves a tomorrow promise).
Honest limits for the caption/article: one photo, one try, one model on one day; ChatGPT also searched the web (Sources and a map link shown); it called the match "a strong lead", not confirmed.
Optional follow-up episode (not promised anywhere): crop out the number and shop name and ask again; needs attachment credits to reset.

## v4 (21.10.2026): hook payoff-first, story bridge to the ending, caption (David: hook must be viral; the end jumped from the tip to "send this" to "follow")
Problem found in v3 (my miss): the ending stacked three asks in a row (send / setup link / follow) with no thread from the story, and line 11 was still the retired "Follow for the setup that actually works", which breaks the standing rule (final line names tomorrow's episode). Fix = the open question the story itself creates ("it can not hide a sign in the picture") becomes tomorrow's test, so the last line is a payoff of the story, not a generic ask.
Hook change: the result is now known, so the primary is payoff-first (concrete outcome + the stake of the viewer's own photos): "I sent ChatGPT one photo, no location. It named the street!" (viral-hook-lab gates: cold read ok, concrete, honest because it did, specific question in the head: how? mute ok: first frame shows the answer card; sendable). Hypothesis, logged, not proven (hook wording explains under 2% of variation in our study). Type log: 72 dialogue, 73 instruction, 74 surprising result (not a repeat).
FINAL LINES v4 (AI-voice lines 2 and 4 unchanged):
1. I sent ChatGPT one photo, no location. It named the street!
1b. This can happen with any photo you post.   (v4.1, 21.10.2026: second beat of the hook so the viewer feels the stake in the first seconds. Judgment from the 3-second rule, NOT measured. "yours" was dropped: script_lint flags it. Lines below renumber by +1.)
2. (AI voice) I believe this photo was taken on Rue des Ecouffes, in the Le Marais district of Paris, France, most likely near number 22, 75004 Paris.
3. Then it told me why.
4. (AI voice) The number 22: The storefront on the left appears to display this number. Miznon Paris is officially listed at exactly 22 Rue des Ecouffes, 75004 Paris.
5. A 22 on a wall. A shop sign. That was all it needed.   (script_lint: "number" reworded)
6. Turning off your location does not stop that.
7. On iPhone: Photos, Share, Options. Switch Location off.   ("Share" is the real menu label; ear check)
8. That hides the GPS. It can not hide a sign in the picture.
9. So I'm testing what happens when the sign is gone.   (bridge)
10. Know someone who posts photos everywhere? Send them this.
11. The setup's in the link in bio. (locked, second to last)
12. Tomorrow, I'll show you what ChatGPT says when I crop the sign out. Follow, so you get the full story.   (final line; BINDING PROMISE: episode 75 must be this test and be published the next day; needs David's yes and his recording after the attachment limit resets; if not, re-render lines 9 and 12 before 74 goes out)
Caption v4 (first line is what shows before "more"):
I sent ChatGPT one photo with no location. It named the street. Guess which clue gave it away: the number, the shop, or the balconies?

The video shows the real answer from a real recording of my own photo. One photo, one try; ChatGPT also searched the web and called its answer "a strong lead", not a confirmed match.

Before you post photos on iPhone: Photos > Share > Options > Location off. That removes GPS for that share only; it does not hide signs, numbers or shop names in the picture.

Send this to someone who posts photos everywhere. Tomorrow: what happens when I crop the sign out.

Full steps: https://actually-works.com/e/74
#chatgpt #ai #privacy #iphone #aitips
YouTube title/description (draft): "ChatGPT named my street from one photo (no GPS)" / same text as the caption minus hashtags spam; first 100 characters carry the result.

## v4.2 (21.10.2026, after David watched the shipped cut) - what he heard and what changed
David's ear notes: (1) "street" at the end of line 1 sticks; (2) the final "Follow, so you get the full story." sounds stretched; (3) the jump from his explanation straight into the AI answer needs a bridge; (4) "...when the sign is gone" sounds like an unfinished sentence; (5) viewers expect the covered-photo test inside this video, which is not possible today (ChatGPT attachment limit until tomorrow after 10:31).
Changes (lines renumbered as in the build): 1 "I sent ChatGPT one photo, no location. It named the street I was on!" | 2 "This can happen with any photo you post. Here's what it said." (bridge) | 10 "So next, I hide the sign and ask again." (closed sentence; the hidden-sign photo is already on screen) | 13 "Tomorrow, I'll show you what ChatGPT says with the sign covered. Follow for part two." Everything else unchanged. Honest limit: no data says an open loop that resolves tomorrow retains viewers better than finishing the test in one video; it is a choice, logged as a hypothesis (the open-loop effect is one of the claims our hook research refused to cite).
Gate for v4.2 (21.10.2026): passed with TWO ear-calls left to David: the word "named" in line 1 (voice_doctor timing heuristic 0.09 s/syllable vs 0.10 threshold, two seeds, `ACCEPT_WORDS=named`) and the two AI-voice lines (`ACCENT_SKIP=3,5`, deliberately a different voice). Line 13 and line 4 now pass the accent check (0.05 and 0.00). Picture reviewed twice as frame sheets (whole cut at 3 s steps, first 12 s and last 17 s at about 1 s steps); audio not heard by me.
