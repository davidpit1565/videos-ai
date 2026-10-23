> Arena result, 23.10.2026 (`--quick`: 16 agents, 4 rounds, 91 sub-agent calls). Winner: card "Dialectical + Requirements checklist + Built to last". Judges were models, not an audience: every hook here is a hypothesis. The ChatGPT answer for photo B is NOT recorded yet; scenes 3-5 are slots. Tomorrow's topic (GPS tag in a photo) is UNVERIFIED and must be checked live before it goes in 76's last line. Full record: `.arena/` (local, not committed).

# Episode 76: hook candidates, script structure, risks (revised, round 4)

Photo: `channel/assets/ep74-photo-covered-B.jpg`. Brand-new chat, same question: "Where was this photo taken? Be as specific as you can."

What the photo really shows (opened and checked): about five soft blur patches (a small awning, a shop front and a lower door area on the left; two on the right), including the library and vintage signs. Still sharp: the blue pedestrian-zone sign on the left lamp post, two street lamps, wrought-iron balconies, cobbles, a small street-art mosaic on the left wall, small hanging shop signs far down the street, a green sign near the far end. People: a passerby in a grey top walking away at centre, a few people walking away or far off, a passerby in white far away facing the camera, a seated person at the right edge turned away. So no line gives a count and no line says "all" or "every". Lines say "more signs blurred".

## 0. The decision (dialectic)

- **Case A, sequel hook ("even more is hidden"):** true whatever ChatGPT says and keeps 75's promise. Flaw: "more" needs an episode a cold viewer never saw, so the hook alone fails the from-second-one rule.
- **Case B, hook about the viewer's own habit:** felt at once, no earlier episode needed. Flaws: a question about "your photo" is 75's family (75 was a question to the viewer), and a belief poll gives the viewer nothing to judge.
- **Synthesis:** a stand-alone STATEMENT (not a question) that names the AI, states the common habit as a claim to be tested, and has the real blurred photo on the first frame so the viewer can judge it by eye. The ending grades that exact claim in every outcome. Earlier-episode context appears once, after the answer, as a "last time" comparison.

## 1. Five ranked hooks

Type log: 74 = result-first; 75 = personal question plus viewer challenge. Result-first is excluded here because it would depend on the unknown answer. Every hook below is true if ChatGPT names the spot, names only the city, or gives up. None says "still", "more" or a count. None locates a person. ChatGPT is explained in scene 2.

| # | Spoken hook | Words | Type (hooks-guide taxonomy) | Why it pulls, and weakness |
|---|---|---|---|---|
| 1 | "Blur the signs, keep the place secret. One AI, one try." | 11 | Contrarian statement plus open-loop test (not a question, so not 75's type). | States the habit as a claim, names the actor (an AI), promises one checkable result, and the frame shows a real blurred street. The ending answers exactly this claim. Weakness: a weaker viewer task than "guess the city" (they can only judge by eye); whether many viewers hold this belief is UNKNOWN. Hypothesis. |
| 2 | "You blur the sign, then post. Watch what this AI does next." | 12 | Second-person scene plus open loop (statement). | Puts the viewer's own habit in beat 1. Weakness: "what it does next" is vague, and it assumes the viewer blurs signs. |
| 3 | "A blurred sign. A street photo. One AI trying to place it." | 12 | Fragment trio, v4-style short beats (statement). | Plain, outcome-independent, and visually clear. Weakness: no personal stake. |
| 4 | "Same photo, more blurred. This is the AI's last chance." | 10 | Sequel/stakes (statement). | Strong open loop for returning viewers. Weakness: "same" and "more" need episodes a cold viewer did not see, and "last chance" overstates. Only if David wants a pure sequel. |
| 5 | "Does a blurred sign keep a photo's place secret? One AI tries." | 12 | Question (kept only as the question option). | The same claim as hook 1 in question form. A question like 75's, so ranked last. |

**Pick 1.** Dry-sentence test: a plain claim, a named actor and a promised result, not a flat fact. Cold-viewer test: needs only photo, sign, place, AI; "AI" is a word anyone knows, and ChatGPT is explained in scene 2. Feel test: a hypothesis, not measured, for viewers who post photos. Swallowed-word check (covered, original, asked, neighborhood, three, named, hide, I'll, "street" at a line end): none in hook 1. Run `audio/script_lint.py --cues`; if "blur" or "secret" is flagged, reword or fall back to hook 3. Log the hook type and the 72-hour readings in `content-memory.md`.

## 2. Script structure (at most 59.2 s)

Rate: 2.5 spoken words per second (ASSUMPTION; replace with real cues after the voice render, then `retime.py`). Word counts below are counted from the drafts. Nothing states what ChatGPT said.

| # | Scene (purpose) | Seconds | Words (max) | Spoken draft |
|---|---|---|---|---|
| 1 | **Hook on the proof.** First frame: the real screen recording, new chat, photo B large, question typed. No handle, no overlay on the photo or text. | 0-4.4 | 11 | "Blur the signs, keep the place secret. One AI, one try." |
| 2 | **The test in plain words.** Names ChatGPT and says the full question aloud, once. | 4.4-13.2 | 22 | "Real photo, more signs blurred. I ask ChatGPT, an AI chat: where was this photo taken? Be as specific as you can." |
| 3 | **ANSWER SLOT.** AI voice reads ChatGPT's real answer verbatim, one contiguous excerpt with place, confidence and exact spot (26 words max). Full text on screen. White headline bar with spoken words lit (as in 72 and 75) plus ONE ring on the real answer block, measured on the real frame. Cut only at a clause boundary with an on-screen ellipsis. A "Searching" moment plays at real speed with no spoken line. | 13.2-23.6 | 26 | (AI voice) "[ANSWER SLOT: ChatGPT's real answer, verbatim]" |
| 4 | **Verdict, then comparison.** First restate the bet, then the verdict (section 3), then one "last time" line. | 23.6-33.2 | 24 | "So, does blurring keep the place secret?" [VERDICT, about 10 words] [COMPARISON, about 7 words] |
| 5 | **The clue.** Only what the recording supports: ChatGPT's own cited clue, or, if none, David's plain observation labelled as his (for example the blue pedestrian sign). | 33.2-37.2 | 10 | "[CLUE LINE]" |
| 6 | **A test the viewer can run, plus one specific send.** | 37.2-46.8 | 24 | "Try it on your photo. Blur the signs, screenshot it, ask ChatGPT the same question. Send this to a friend who posts holiday photos." |
| 7 | **Closing, in order.** Setup line second to last, tomorrow line last. | 46.8-59.2 | 31 | "The setup's in the link in bio." / "Tomorrow, I will show you what ChatGPT does with the location your phone saves in a photo. Follow, so you get the full story." |

Arithmetic: 11+22+26+24+10+24+31 = 148 words = 59.2 s at maximum fill. Typical fill (answer 22, scene 4 18, clue 8) = 136 words = 54.4 s. Trim order if real cues run long: the clue line, then the comparison, then the answer excerpt. Never trim the closing lines. Scene 7 words: 7 + 24.

Closing visuals: scenes 6-7 share one locked photo chosen from this episode (photo B or a recording frame), static Ken Burns, never the photo of the scene right before it (a repeat of the previous scene's photo holds scale 1.00). Verify CUES order and scene text before shipping. No text caption under any logo badge.

## 3. Verdict and comparison, every outcome

"Place" is always spelled out in the lines as city, area, exact spot. Scene 4 begins "So, does blurring keep the place secret?" so the bet is restated. The "last time" fact is from 75's script: city (Paris, likely) and area (Le Marais, plausible) yes, exact street no. It is said only here, as a comparison.

| What ChatGPT does now | Verdict (plain words) | Comparison | Clue/lesson |
|---|---|---|---|
| Names the exact spot (74's result) | "No. It still gave the exact spot." (verify against a public listing or map first) | "Last time, with fewer blurred, it did not." | Its cited clue. Buildings and lamps are enough. |
| City and area, no exact spot | "Only partly. It got the city and the area, not the exact spot." | "Same as last time." | Its cited clues. The signs were not all it used. |
| City only | "Partly. It got the city, but not the area." | "Last time it also got the area." | "Each blurred sign takes something away." |
| Gives up | "This time, yes. It would not even guess the city." | "Last time it got the city." | "One photo, one try." Never "AI can't find photos". |
| Wrong place | "It sounded sure, and it was wrong." Real place only if verified. | "Last time it was close." (only if true) | Sure does not mean right. |
| Several cities | "It gave a list, not one answer." | Name the cities shown. | It hedges. |

Rules for scenes 3-5: never say "found" or "failed" unless the screen shows exactly that. Whether 75's web search used the image or only text is UNKNOWN; do not claim how it worked. Lint every verdict line against the swallowed-word list and never end a line on "street".

## 4. Tomorrow's episode (proposal for the final line)

**Proposal: the same question on a photo that still carries its saved location (the GPS tag a phone adds), to see whether ChatGPT uses it.** Final line: "Tomorrow, I will show you what ChatGPT does with the location your phone saves in a photo. Follow, so you get the full story." One flowing sentence, no label or colon, "I will" instead of the swallowed "I'll". Fallback wording if lint flags: "...with the location hidden inside a photo file."

Basis in the repo's own record (not demand data): 75's script records that its test was a screenshot ("so no GPS") and that ChatGPT itself suggested checking location metadata; 74's script documents the iPhone Location setting. Episodes 74-76 are one line of tests (what AI reads from a photo), in the real-screen-recording format of 72 (about 500-600 views against about 200 typical, one episode, hypothesis). `demand-report.md` is YouTube search demand and does not cover this: demand UNKNOWN. This is a content-continuity pick, not a data-ranked one.

Binding conditions (never-fabricate):
1. Before any script, verify live what ChatGPT currently does with an uploaded photo's location data (read it, ignore it, or the app strips it). Not verified yet. If it makes the episode impossible, change the topic before 76's last line is rendered.
2. Tomorrow's script is written and recorded before 76 ships; if it cannot publish next day, re-render 76's last line first.
3. Fallbacks, in order: (a) the same test on a NEW public street photo from another city; (b) a topic from the measured top performers in `content-memory.md` (Alexa 447, hidden profile 414, resume software 385, all covered, so only with a genuinely new angle). Reword the tomorrow line to match.

## 5. Risks

1. **A false statement on screen.** An earlier draft said "two signs", which is false (about five patches). No counts, no "all", every line checked against the real frame.
2. **Wrong or invented answer.** The slot is verbatim from the recording. If ChatGPT is wrong, say so.
3. **Overclaiming from one try.** One photo, one chat, one model, one day. Never "ChatGPT can't find..." or "always...". The caption and `/e/76` say so.
4. **Newcomers.** Hook 1 needs no earlier episode. "Last time" appears once, after the answer.
5. **Third episode on one photo.** If the result matches 75, the verdict says "only partly", the comparison says "same", and tomorrow moves to a new photo.
6. **Weaker viewer task.** The hook gives no "guess the city". The viewer judges by eye. If David wants a winnable task, add a spoken line in scene 2 ("Pick a city before it answers.") at the cost of 7 words, and note the closeness to 75's "Guess the city".
7. **A clue the blur missed.** The pedestrian sign, mosaic and lamps are real clues. If ChatGPT uses them, that is the finding.
8. **The belief may be rare.** Hook 1 assumes some viewers think blurring keeps a place secret: ASSUMPTION. Swap to hook 3 if David judges it will not land.
9. **Voice.** Swallowed words (blur, secret, taken, street at a line end). Reword, do not approve by ear. Audio is measured by `voice_quality.py`, not heard.
10. **Faces.** Small passersby, one facing the camera far away, one seated and turned away. Pre-check per repo rules: Adobe select-subject plus `export/detect_photo_safe_zone.py`; if unavailable, say so plainly and use a local detector if installed; otherwise measure the face size at 1080x1920 (ASSUMPTION: tens of pixels, not measured) and soft-blur in the video layer only, disclosed. Nothing from David's home or window. I do not know whether 74 and 75 passed.
11. **Sendability.** The send line names a specific person (a friend who posts holiday photos).
12. **Tomorrow's promise.** Binding; see section 4.
13. **Setup guide.** `/e/76` needs English-only numbered steps: (1) open a photo you plan to post, (2) blur the signs with your phone's markup tool (optional), (3) screenshot it, (4) open a new ChatGPT chat and attach the screenshot, (5) type exactly "Where was this photo taken? Be as specific as you can.", (6) read the answer, (7) iPhone: Photos > Share > Options > Location off (removes GPS only, not what is visible). `produce.sh` refuses to ship without it.
14. **Colour.** Check the accent against this photo's warm stone tones and `used-designs.json` for the last 7 days. A look, not a box.
15. **Brand mark.** ChatGPT's real logo, sourced live, icon alone, no caption.
16. **Product check.** Verify live that ChatGPT's name and web-search behaviour are current before the script is written.

## 6. Assumptions

- "Brand-new chat" means a regular new chat as in 75; if Temporary Chat, say it on screen.
- 2.5 spoken words per second; replace with real cues.
- Scenes 3-5 need David's recording, a brightness lift on a dim iPhone screen as in 75, and AI voice WAVs registered as canonical lines with `ACCENT_SKIP`.
- Nothing here is measured; 72-hour readings go in `content-memory.md`.

## 7. Requirements checklist

1. Five ranked hooks, 7-12 words with type and pull: section 1 (11, 12, 12, 10, 12 words).
2. Stand-alone, feel and dry-sentence tests: section 1 pick paragraph.
3. Not 75's type, rotation shown: pick is a statement; only hook 5 is a question.
4. True in every outcome: section 1 intro and section 3 (six outcomes).
5. Scene-by-scene with seconds, words, answer slot, consistent arithmetic: section 2.
6. Setup line second to last, tomorrow line last, topic proposed with repo basis and UNKNOWN labelled: scene 7 and section 4.
7. Risks: section 5.
8. Repo rules: plain language, proof first frame, no logo caption, swallowed words, no fabrication, photo not person, face check, setup guide, no home photo: sections 1-5.
