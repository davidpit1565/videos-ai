# Episode 74 (SCRIPT v3, 20.10.2026) — "I asked ChatGPT where a street photo was taken"

Status: NOT BUILT. Needs David's screen recording (see "Recording v3" at the end; it replaces the older "Recording" section) before any line that quotes ChatGPT is final. Nothing here claims a result.

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
