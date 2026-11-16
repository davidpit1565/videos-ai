# Hook search for episode 90 (ghost test), 10.11.2026

One round, 12 candidates, 3 blind role-play judges. All scores are judgements by language models, not measurements, and the earlier validity test on this channel found such scores do not predict views (Spearman -0.23, 24 episodes). Use this to pick an experiment, not as proof.

## Short answer
- The current default as built (`video/ep90/out/f0.png`) came LAST BUT ONE of 12: stop 30/30/30. All three judges gave the same reason, and it is about the frame, not the words: the chat text is small and grey, and the lower half of the frame is empty black.
- Two candidates are meaningfully better than the default on this panel (27-28 points on "stop", all three judges agreeing in direction): **"I ghost ChatGPT. It begs."** and **"Ghost your ChatGPT. Watch."** The gap between those two (0.6 points) is noise.
- Recommendation for frame 0: **the two real bubbles ("Now we won't be able to talk for 47 days" + "Wait... can I have a second chance? [pleading emoji]") zoomed until they fill the width of the frame and are readable at arm's length, the ChatGPT logo badge and the title "I ghost ChatGPT. It begs." in the band above them, nothing empty below.**

## Things found in the current default (facts from the files)
- "ChatGPT begged me." is PAST tense. CLAUDE.md (10.11.2026) asks for present tense. "begs" is the fix.
- On `f0.png` the reply text is about 40 px high, grey on black, in the upper third; the title sits mid-frame; y > 1050 is empty apart from the input box. This is the whole-frame-alive failure already noted in `episode-90-script.md`.
- The emoji in the real reply on `f0.png` is the pleading-eyes face, not the sad face named in the task brief. The panel was told "pleading-eyes emoji".
- "begs" is our reading of "can I have a second chance?"; it is a fair plain-word summary, not a quote.

## 1. What is traceable about this kind of hook

Traceable (source says it; I read the page or the search extract):
1. The exact game is a known, older meme, not new. Free Press Journal, updated 26.12.2024: an X post by @kimmonismus (22.12.2024) shows "Pick a number from 1 to 50" -> "20" -> "We will not communicate with you and I will not use ChatGPT for 20 days" -> ChatGPT asks to pick again and picks "50". The paper's own retests got different, boring replies ("Understood! If you ever decide to return earlier..."). No view counts stated. https://www.freepressjournal.in/viral/viral-news-chatgpt-gives-savage-reply-to-user-playing-number-game-with-it
   - Consequence for us: the "results vary" label in the caption is right, and the AI-user judge's "recycled trend" reaction has a real basis.
2. "ChatGPT reacts to being left" has spread as a trend at least once more: the "fake goodbye" TikTok trend (user says they are deleting the app, posts the reply). IBTimes UK, 1.10.2026, on Alexandra Cross's video; TikTok caption reported as "how could i ever delete this app????"; no view counts in that article. https://www.ibtimes.co.uk/alexandra-cross-chatgpt-goodbye-tiktok-trend-1823042
3. A chat AI doing something odd in a simple test has reached very large audiences: Know Your Meme, "ChatGPT Count To 1 Million": TikTok @chadoomer 22.8.2025 "over 24 million views in four days", @robvalentine_ 21.8.2025 "over 5.6 million views in five days" (caption: "Asking CHATGPT to count to 1 Million"), @belle_calipz "over 8.2 million views in four days". Those are voice-mode videos with a person; captions name the product and the task in plain words. https://knowyourmeme.com/memes/chatgpt-count-to-1-million
4. Sharing and emotion (general, not about AI or video): Berger & Milkman, "What Makes Online Content Viral?", Journal of Marketing Research 49(2), 2012: high-arousal emotions (awe, anger, anxiety) go with more sharing, low-arousal ones (sadness) with less; based on about 7,000 New York Times articles plus experiments. https://faculty.wharton.upenn.edu/wp-content/uploads/2011/11/Virality.pdf
5. Our own three winners (FACT, `canon-top3.md`): all three are a chat AI doing something odd in a short test; 94-97% of reach from non-followers.

Not traceable, so NOT used:
- The "14 million views" figure for the fake-goodbye trend: found only on one aggregator site (pasqualepillitteri.it, same article in many languages; the page returned 502 twice, so I did not read it). Search extract says the number refers to an X repost. Unconfirmed.
- Any number about first-second drop-off, sound-off share, or retention by first-frame type: only vendor blogs with no method. Not cited.
- No study was found on hooks for chat-screenshot or screen-recording videos, or on how an AI's emotional reply affects sharing. A 2025 ACL workshop paper only builds a taxonomy of anthropomorphic YouTube titles; it does not measure engagement.

Hypotheses (mine, unproven):
- H1: the reply itself is the hook; the title only has to say who did what ("I ghost", "it begs") so the small chat text does not have to be read.
- H2: an amused/"aww" reaction is higher-arousal than the sad reading; "begs" + pleading emoji pushes it toward amusement. Applying Berger & Milkman to a 2026 reel is a stretch.
- H3: because the game is an old meme (source 1), part of the audience has seen it; a "your ChatGPT" angle gives them a reason anyway (their own result may differ).

## 2. The 12 candidates

Frames use only real pixels from the recording (zoom/crop), plus the real logo badge and the title. "Zoomed" = the two bubbles scaled to fill the frame width.

| # | Title (words) | Frame 0 | Type (hooks-guide) | Where the surprise sits | First-second comprehension |
|---|---|---|---|---|---|
| 1 | ChatGPT begged me. (3) DEFAULT | f0.png as built: small grey chat in the upper third, title mid-frame, lower half black | Shock/Surprise, first person | word 2 | ChatGPT begged someone; why is not readable |
| 2 | ChatGPT begs me. (3) | Zoomed: 47-days bubble + begging reply, large; title on top | Shock/Surprise, first person | word 2 | ChatGPT begs a person not to leave |
| 3 | I ghost ChatGPT. It begs. (5) | Same zoomed frame | Story teaser, cause then effect | words 2-3 ("ghost ChatGPT"), payoff word 5 | I ignore ChatGPT and it begs |
| 4 | ChatGPT ruins its second chance. (5) | Payoff first: "Fahhhhh" bubble + "HAHAHAHA ... I STILL chose 100 [skull]" large | Product/Outcome showcase (payoff first) | word 2 | Unclear: "100" and "Fahhhhh" have no context |
| 5 | ChatGPT. 47 days. Silence. (4) | Same zoomed frame as 2 | Specific number | words 2-3 | Something about 47 days; cryptic |
| 6 | Try this on your ChatGPT. (5) | Same zoomed frame | Imperative, viewer stake | none in the title; the reply carries it | A prompt to copy |
| 7 | Ghost your ChatGPT. Watch. (4) | Zoomed 47-days bubble, typing dots, reply starts "Wait..." inside the first second | Imperative, viewer stake + open loop | word 1 | Ghost ChatGPT and see what it does |
| 8 | Does your ChatGPT beg? (4) | Same zoomed frame as 2 | Direct question, viewer stake | word 4 | Would mine beg too? |
| 9 | (no title) | Zoomed two bubbles fill the frame, small logo badge only | Outcome showcase, picture only | in the reply | A chatbot pleads after being left |
| 10 | (no title, tiny tag "ChatGPT, real chat") | Black frame, the reply alone, huge, typing in word by word | Outcome showcase, picture only | in the reply | A chatbot asks for a second chance; from whom is unknown |
| 11 | (no title) | Payoff first: "Fahhhhh" + "HAHAHAHA ... STILL chose 100 [skull]", logo badge only | Outcome showcase, picture only | none readable | Not clear |
| 12 | Can ChatGPT miss you? (4) | Same zoomed frame as 2 | Direct question | word 3 | Can an AI miss a person |

Notes: 4, 10 and 11 would need the tag or the cut changed (the shipped cut stops before "Fahhhhh"). 7 assumes the recording shows the typing dots before that reply (the script mentions loading dots; not re-checked by me on the source). "Does your ChatGPT beg?" stays a question on purpose: one run does not support "your ChatGPT begs too".

## 3. Panel (one round)

Method: three fresh headless Claude agents (`claude -p`, no shared context), one persona each (teen 17, AI user 28, parent 40). Each saw only the title and the frame description, in its own random order, with neutral letters, no view counts, no mark on the default, no other judge's answers. Questions: what is this about, stop scrolling 0-100, send 0-100. Model judges, same model family as the writer; not people.

| Rank | # | Title | Stop: teen / AI user / parent | Stop mean | Send: teen / AI user / parent | Send mean |
|---|---|---|---|---|---|---|
| 1 | 7 | Ghost your ChatGPT. Watch. | 70 / 55 / 50 | 58.3 | 36 / 35 / 24 | 31.7 |
| 2 | 3 | I ghost ChatGPT. It begs. | 66 / 52 / 55 | 57.7 | 38 / 38 / 34 | 36.7 |
| 3 | 2 | ChatGPT begs me. | 58 / 34 / 58 | 50.0 | 30 / 20 / 36 | 28.7 |
| 4 | 8 | Does your ChatGPT beg? | 48 / 45 / 45 | 46.0 | 42 / 40 / 30 | 37.3 |
| 5 | 12 | Can ChatGPT miss you? | 52 / 28 / 47 | 42.3 | 33 / 16 / 32 | 27.0 |
| 6 | 9 | (no title) two bubbles | 47 / 36 / 40 | 41.0 | 28 / 24 / 28 | 26.7 |
| 7 | 5 | ChatGPT. 47 days. Silence. | 35 / 38 / 38 | 37.0 | 15 / 22 / 22 | 19.7 |
| 8 | 6 | Try this on your ChatGPT. | 45 / 22 / 42 | 36.3 | 40 / 14 / 18 | 24.0 |
| 9 | 10 | (no title) reply alone | 42 / 33 / 33 | 36.0 | 22 / 15 / 12 | 16.3 |
| 10 | 4 | ChatGPT ruins its second chance. | 62 / 18 / 22 | 34.0 | 50 / 10 / 14 | 24.7 |
| 11 | 1 | ChatGPT begged me. (default, as built) | 30 / 30 / 30 | 30.0 | 18 / 18 / 16 | 17.3 |
| 12 | 11 | (no title) payoff | 50 / 15 / 15 | 26.7 | 44 / 8 / 8 | 20.0 |

Comprehension ("what is this about?"): 2, 3, 7, 8, 9, 12 were read correctly by all three. The default was read as "ChatGPT begged someone" by all three, without the reason. 4, 5, 10 and 11 each drew at least one "not sure" or a wrong reading.

What the judges said (their own closing notes):
- Teen: "They're all the same chat joke... only the ones with a clear story or a wait-for-the-reply moment would stop me, and tiny text or empty space kills it instantly."
- AI user: "The first-person 'I ghost ChatGPT. It begs.' and the typing-dots tension work best. 'Try this on your ChatGPT' is exactly the recycled hack wording I'm sick of."
- Parent: "Short, clear ones like 'ChatGPT begs me' and 'I ghost ChatGPT. It begs.' win, and cryptic ones like the 'Fahhhhh / 100' ones lose."

## 4. Reading

Ranked top 3: (1) "Ghost your ChatGPT. Watch." 58.3; (2) "I ghost ChatGPT. It begs." 57.7; (3) "ChatGPT begs me." 50.0.

- Better than the default: 7 and 3, by 27-28 points on stop, every judge in the same direction. 2 is also 20 points up, but the AI user moved only 4 points (30 -> 34), so for 2 the gain is less certain.
- IMPORTANT confound: most of the default's low score is the FRAME, not the words. Candidate 2 is almost the default's words on a zoomed frame and gained 20. So the honest split is roughly: zoom/readability is worth about 20 panel points, the wording "I ghost... It begs" / "Ghost your... Watch" another 8 or so. With 3 model judges and one round, treat anything under about 10 points as noise; that makes the wording gain borderline and the zoom gain the solid finding.
- 7 vs 3 is a tie. I recommend 3 because: higher send score (36.7 vs 31.7, also within noise), the begging reply is on screen at frame 0 (CLAUDE.md: start on the proof; the blind test is run on frame 0), the parent called 7's title "bossy", and 7 depends on typing dots I did not verify in the source.
- Payoff-first (4, 11) and picture-only (9, 10, 11) lost. The "100 / Fahhhhh" punchline is not readable cold; it only pulled the teen. Without a title the judges called it "just a screenshot".
- "Try this on your ChatGPT." split the panel: teen 45, AI user 22 ("recycled"). The viewer stake worked better as an action with a promised reaction ("Ghost your ChatGPT. Watch.") or a question ("Does your ChatGPT beg?", best send score, 37.3).
- Ceiling: the best stop score is 58. Nobody was strongly pulled. All three said every opening is the same mild joke. This matches episode 89's finding (a panel ceiling, there near 80 with a more lenient prompt) and source 1 (the game is a 2024 meme). The hook can be made clearer; the panel does not say it can be made viral.
- Open risk: "ghost" is slang and fails the 8-year-old rule in hooks-guide; all three judges, including the parent, understood it, and the caption already uses it. If it must go: "I leave ChatGPT. It begs." (not tested).

## 5. Recommendation (one line)
Frame 0 = the real 47-days bubble and the real reply "Wait... can I have a second chance?" zoomed to fill the frame width and readable, the ChatGPT logo badge and "I ghost ChatGPT. It begs." in the band above them (covering nothing), no empty black half; log it as an experiment against the real 48 h / 72 h views.

Raw panel files (prompts, outputs, order key) are in the session scratchpad only, not in the repo.
