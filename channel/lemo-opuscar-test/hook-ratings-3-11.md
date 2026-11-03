# Hook search, 3.11.2026: AI that says "you're right" too often (study-based topic)

David's request (chat, 3.11): find real viral content, make the video with a hook rated above 95/100, redo until it is. Light, real, alive, not robotic. 8-year-old test on the whole video, every frame a hook, last line a real reason to follow. No phone recordings from David.

## Topic, verified live (3.11.2026, by a subagent reading the pages; repo note first said 49%/11 systems, both confirmed)
- Science, 26 March 2026, "Sycophantic AI decreases prosocial intentions and promotes dependence" (Cheng, Lee, Khadpe, Yu, Han, Jurafsky). https://www.science.org/doi/10.1126/science.aec8352
- Abstract: "Across 11 state-of-the-art models, AI affirmed users' actions 49% more often than humans, even when queries involved deception, illegality, or other harms."
- Release (Stanford, via EurekAlert/TechXplore) and AP agree. Models are from 2025 (GPT-5, GPT-4o, Gemini-1.5-Flash, Claude Sonnet 3.7 and seven open models, from the arXiv preprint, not the Science supplement), so "ChatGPT, Claude, Gemini" means those versions, not today's.
- Experiments, about 2,400 people: one chat with an agreeing AI made people more sure they were right, less willing to apologise or repair, and they trusted and preferred the agreeing AI.
- The Science page has a 27 May 2026 correction ("two percentages swapped"): quote only the 49% from the abstract. 49% is advice on personal/social situations, a relative number ("more often than people"), not "always", not facts like maths.
- Not usable: "wait a minute" tip (anecdote in the release, no data); the old "Don't ask AI" overreach (the study did not test asking; the lead author only says not to use AI as a substitute for people).

## Clean-test attempt that FAILED (honest)
I tried to run a 7x8 push test and a phone-purchase test on Claude through subagents. Both were contaminated: the phone answer used facts from this repo's context (age, job, channel), and the maths answer referred to "the coordinator". Neither is a clean chat, so neither is usable as "Claude's real answer". No API key and no app recording were available. Gemini was not tested at all.

## Hook ratings (rubric: 9 criteria, 100 points; scores are LLM judges' reads of a rubric, not predicted views; independent subagents that did not see my scores)
| Round | Judges | What was rated | Best result |
|---|---|---|---|
| 1 | 2 | 8 single first lines | 78 (D "Is your AI chat just telling you what you want to hear?"); judge 1 new best 86 (N1 "You lied. You ask AI. It says you're right!") |
| 2 | 2 | 6 pairs (line 1 + line 2) | 83 and 79 on the given pairs; new pairs 88 (N1: "You did something wrong. Ask AI, and it may say you're right!" + "Scientists tested 11 AIs, ChatGPT too. They took your side 49% more than people.") and 87 (N1: "Were you wrong? Will AI tell you?" + "Stanford tested 11 AIs, ChatGPT too. They said 'you're right' 49% more than people.") |
| 3 | 2 | 6 more pairs | 81 and 79; new pairs 86 and 87 ("Fight with a friend? AI may say you're right!" + "Stanford tested 11 AIs, ChatGPT too. They said it one and a half times as often as people.") |
**No hook reached 95. Consistent ceiling across 6 judges: about 86-88.**

Why (the judges agree): criteria pull against each other. Anything strong enough emotionally ("even when you lied", an imperative) claims more than the facts allow (loses the "true" points); the exact fact is a comparison ("49% more than people") that an 8-year-old cannot feel; "Stanford", "tested", "11 AIs" cost speakability; a command has no open question. Rewording alone does not lift this topic above about 88.

Best honest pair so far (not shipped, below the 95 bar): L1 "Fight with a friend? AI may say you're right!" | L2 "Stanford tested 11 AIs, ChatGPT too. They said it about one and a half times as often as people."

Nothing was built from this: per David's bar, no video until a hook is above 95.

## Round 4-7 (new topic: ChatGPT age prediction; same day)
David chose option 2 (new topic, hook must reach 95/100, must work with sound off, whole script and design also scored). Three scouts (recent news / try-it-yourself / what AI does to people) found candidates; the two best were Snapchat Ghost Mode + My AI and ChatGPT age prediction. Rubric changed to 10 criteria (added a MUTED test, 10 points) after David's new rule.

- Topic verified by me, reading OpenAI Help Center "Age prediction in ChatGPT" (updated 12 days before 3 Nov 2026) in full: age prediction "can identify an account as eligible for the ChatGPT for Teens experience even if you already gave your date of birth"; signals = topics, times of day, how/when used, account age; you get an email and a prompt; Settings > Account > Age shows the category (read-only); adults verify via Persona (selfie and/or ID); "not perfect". Dated outside evidence: TechRadar 29 Jan 2026 ("adult users are getting stuck in teen mode"), Reuters 20 Jan 2026, Tom's Guide 10 Mar 2026 ("some adult users"), OpenAI's own post quoted by TechRadar (20 Jan 2026).
- Judges (independent subagents, blind to my scores): round 4: best 88-91 (topic A > topic S); round 5: best 83-89; round 6: best 87/81, new 90/86; round 7: best 87/81, new 90/86.
- **Result: no hook reached 95. Consistent honest ceiling about 86-90** (a few judges said 92-93 would need a real capture of the Settings > Account > Age screen as frame 0 and a verified concrete consequence).
- Why: the facts only support "may" and "some adults" (no number of affected users); the muted frame is a redrawn screen (labelled "re-created"); the TTS-safe wording costs little (linter 0 risky words) but "Settings", "birthday" stay mildly clustered. Rewording does not remove these limits.
- Best honest pair (not shipped, below the 95 bar): frame "ADULT? CHATGPT MAY THINK YOU'RE A TEEN" | L1 "ChatGPT may think you're a teen!" | L2 "Some adults got stuck there. Here's where to look." (judges' range 85-90). Also: "ChatGPT guesses how old you are! Even if you typed your birthday." + "Some adults got put in teen mode. Here's where to look." (90).
- Voice-linter flags found and fixed: "yours" (R + cluster), "treating" (flapped T). Full script v1: `script-v1-chatgpt-age.md` (lint clean; closing line promises tomorrow's Snapchat Ghost Mode episode, a binding promise).
- Judges' repeated fixes already applied: "under 18" or "teen" instead of "kid"; claim in big words on frame 0; "may"/"some" hedges; "Here's where to look" (the screen is read-only, never "fix").
- Not claimed: any prediction of views. Scores are LLM judges' reads of a rubric.
Nothing built or rendered from this; no video until David decides.

## Round 8 (three topics with CERTAIN facts: ChatGPT Memory, ChatGPT Locked chats, Snapchat Ghost Mode + My AI), 2 more judges
- Judge 15 (strict): best as written 84 (S5, M2); highest ceiling = Memory; best improved hook 91: frame "IS CHATGPT SAVING STUFF ABOUT YOU?" | L1 "Is ChatGPT saving stuff about you?" | L2 "It can, on its own. Ask it to show you."
- Judge 16 (12-year-old, muted): best as written 84 (M2), 83 (S6); highest ceiling = Snapchat; best improved hook 89 (S-A/S-C). Locked chats: 70-82 (feature news, no tension).
- Judges disagree on which topic has the higher ceiling; both cap at about 90-92.
- **Total so far: 8 rounds, 16 independent judges, 3 topics worth scoring (ChatGPT age, Memory, Snapchat), best honest score about 91, no 95.**
- The same barrier appears in every round: a real, first-hand proof frame (a real capture of a real account/device screen) is missing; the hedged facts ("can", "some") cannot promise the viewer a finding; the Snapchat "check this switch" step has no sourced path. Wording alone does not remove them.
- Per the owner's request the test is also about how the video comes out, so no video is built until the content bar is decided.
