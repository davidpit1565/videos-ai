# Topics mined from Reddit, 15.11.2026

Purpose: find the TOPIC before building anything (hypothesis from the reference reel: topic, not hook, decides reach). Each candidate is a felt everyday situation, tested first as ONE picture or a 7-second text reel. Read-only research; nothing built, nothing published.

## How this was gathered (read this first)

- Reddit blocks this environment: `old.reddit.com/.../top/.json` returned a "Blocked" page, and the Exa fetch of `reddit.com/r/<sub>/top/?t=week` returned SOURCE_NOT_AVAILABLE for r/ChatGPT, r/ClaudeAI and r/OpenAI. **No subreddit top-list was read directly.**
- What was actually read: (a) news and aggregator articles that quote a named Reddit thread with its score (dated 26.10 to 14.11.2026); (b) `reddit.sentinel-team.org` snapshots, which are third-party copies of Reddit posts and top comments. The snapshots found are dated May to August 2026 (older than the 7-30 day window), so they show what people KEEP complaining about, not this week's top posts; (c) the sloane.ai and limitdex trackers for Claude limit complaints (they quote r/ClaudeAI posts).
- Scores: written only where an article or snapshot printed them. Everything else is UNREAD. No quote is invented; quotes below are copied from those sources.

## Ranked candidates

Ranking logic: felt in 3 seconds + obvious person to send to + the winner's pattern (two products, one glance, a joke about a habit) + recurs in many threads, not one.

### 1. "Gemini replaced Google Assistant and now it can't do the one thing I asked"
- Felt situation: you say "set a timer / play my music / navigate there" to your phone, and the new AI assistant talks for ten seconds and does nothing.
- Evidence:
  - https://www.androidcentral.com/apps-software/ai/google-pixel-owners-say-geminification-has-ruined-their-phones-what-do-you-think (13.11.2026): r/GooglePixel thread "picking up steam"; top reply "As a long-time Pixel user, I agree." Score UNREAD. Complaints named: Apple Music, Waze, Telegram.
  - Snapshot https://reddit.sentinel-team.org/posts/1tiotrf/snapshots/2026-05-22T12%3A07%3A06.902333Z (r/GoogleGemini-type thread, May 2026): user says Gemini answers "is it going to rain" with a long reply plus "do you want me to set the route in Waze?"; "I don't remember Google Assistant being that annoying". Score UNREAD.
  - Snapshot https://reddit.sentinel-team.org/posts/1vf5mbb/snapshots/2026-08-06T18%3A21%3A24.332541Z (Aug 2026): Gemini Live vs ChatGPT voice. Score UNREAD.
- Why it is shared: send to the friend who has a Pixel / the parent whose phone "got worse after the update".
- Test format, ONE picture, two panels. Left "Google Assistant, 2019": a phone, a tiny timer icon, text "Timer set." Right "Gemini, 2026": same phone, a wall of text, text "Anyway, here are 9 things I can do." Headline on picture: "Me: set a timer."  (6 words)
- Products: Google (Gemini, old Assistant). Not Claude/ChatGPT.
- Verify before use: the Android Central article is a summary of one thread; do not claim "most people". Check the current Gemini behaviour yourself (CLAUDE.md rule: verify the product is still real).

### 2. "It ends every answer with 'Want me to...?' and you feel rude saying no"
- Felt situation: you got your answer, and the AI offers one more thing, and one more, and you feel guilty closing the chat.
- Evidence:
  - Snapshot https://reddit.sentinel-team.org/posts/1td0uy6/snapshots/2026-05-15T19%3A40%3A49.640Z (title "Do you feel bad not responding to the follow up questions", May 2026; exact snapshot URL as printed by the source: https://reddit.sentinel-team.org/posts/1td0uy6/snapshots/2026-05-15T19%3A40%3A49.640Z may need the longer timestamp, see the search result). Score UNREAD. Quote: "I always feel just a little bit guilty ignoring those questions."
  - https://www.pcworld.com/article/3221302/i-got-chatgpt-to-stop-its-annoying-follow-up-questions-with-one-prompt.html (27.08.2026, not Reddit): ChatGPT, Claude and Gemini all end replies with "Want me to...", "If you like...", or clickable chips.
  - Snapshot https://reddit.sentinel-team.org/posts/1tiotrf/snapshots/2026-05-22T12%3A07%3A06.902333Z: "It just loves to talk about everything it can do like its in a constant demo mode."
- Why it is shared: it is the same felt habit as the 2:37 AM picture (the "one more thing" loop). Send to whoever you stay up chatting with the AI next to.
- Test format, 7-second text reel (3 cards): "AI: Here is your answer." / "AI: Want me to also...?" / "Me: no. (feels rude)". 
- Products: ChatGPT, Claude and Gemini all named in the PCWorld test. Make Gemini the visible one to rotate.
- WARNING: very close to the winner's "one more thing" idea. Treat as a sibling of the winner, not a new concept; test only if the winner is not re-posted in the same form.

### 3. "I pay for three AIs and use one"
- Felt situation: ChatGPT, Claude and Gemini subscriptions all renew on your card, and you open only one.
- Evidence:
  - Snapshot https://reddit.sentinel-team.org/posts/1tiw6f6/snapshots/2026-05-22T19%3A21%3A36.340416Z (May 2026): "i downgraded from every paid AI subscription and nothing broke"; "sixty dollars a month. every month. for eight months." Score UNREAD.
  - Snapshot https://reddit.sentinel-team.org/posts/1v690dt/snapshots/2026-07-30T04%3A40%3A03.223031Z (Jul 2026): 64 comments on "which subscriptions do you pay for". 
  - https://www.xda-developers.com/gemini-4-argon-made-me-consider-cutting-claude-and-chatgpt-subscriptions/ (14.11.2026, not Reddit): "hard to defend paying for multiple chatbots".
- Why it is shared: send to the friend with "three AI subscriptions and one job".
- Test format, ONE picture: three logo cards (ChatGPT, Claude, Gemini) stacked as bills "$20 / $20 / $20", one lit up, two grey. Text: "Paying for three. Using one."  (5 words)
- Products: ChatGPT, Claude, Gemini (rotates by design).
- Real logos required by CLAUDE.md; no word inside a filled box.

### 4. "You hit the usage limit in the middle of the thing"
- Felt situation: the AI stops mid-task and says come back at 3 pm.
- Evidence:
  - https://sloane.ai/limits/claude/ (updated 14.11.2026): tracker counts 71 reports in 7 days (83 the week before); quotes r/ClaudeAI posts such as u/Tummes "Claude just revoked the weekly limit reset I saved for this morning". Individual scores UNREAD.
  - https://startupfortune.com/claude-admits-recent-issues-used-more-limits-than-intended-and-offers-users-a-reset-but-that-is-not-enough/ (10.11.2026): Anthropic gave all paid users one free reset after weeks of complaints (the article quotes Anthropic's ClaudeDevs post on X, not Reddit).
  - https://limitwatch.beehiiv.com/p/two-claude-resets-and-936-limit-reports-in-one-week (12.11.2026): 936 limit reports in a week across tools; Claude Code 433, OpenAI Codex 386 (X and GitHub, not Reddit).
- Why it is shared: send to the friend who "is always waiting for Claude to come back".
- Test format, 7-second text reel: "Me: almost done." / "Claude: come back at 3 PM." / "Me: it is 1 PM."
- Products: Claude mainly, ChatGPT/Codex also hit limits (per limitwatch).
- Caution: the felt audience is heavier users (coding). Everyday viewers may not feel it. Also a news-cycle topic, not an evergreen one (David's rule: viral, not new). Rank 4 for that reason.

### 5. "ChatGPT said 'ready in 45 minutes' and then never came back"
- Felt situation: the AI promises to finish later and you wait for something it cannot do.
- Evidence:
  - https://tricklings.com/hilarious-chatgpt-fails-amp-funny-things-people-asked/ (06.11.2026, a roundup of Reddit screenshots, authenticity not guaranteed by the author): item 8, u/bfg10000000000000, "I'll have it ready in 45 minutes" then ghosts; the author calls it "classic coworker energy". Score UNREAD.
- Why it is shared: send to the coworker who says "I'll get back to you".
- Test format, ONE picture: a chat bubble "Ready in 45 minutes" and an hour-glass, then the same bubble 3 days later. Text: "Still waiting. 3 days."  (5 words)
- Products: ChatGPT.
- DUPLICATE RISK: see duplicate check (ep90 ghosting is the reverse direction). Evidence is a single roundup item, so this is a weak candidate; the real thread was not opened.

### 6. "The AI agrees with everything my friend says"
- Felt situation: someone you care about checks every decision with ChatGPT and it always says yes.
- Evidence:
  - https://www.themarysue.com/homeowner-took-in-friend-who-lost-custody-of-her-kids-then-learned-where-all-of-her-attention-is-allegedly-going-she-treats-it-like-a-best-friend/ (12.11.2026): AITA post, the author calls ChatGPT "basically just a yes man for everything she feeds it". Score UNREAD.
  - Snapshot https://reddit.sentinel-team.org/posts/1tspxoj/snapshots/2026-06-05T19%3A30%3A44.375215Z (Jun 2026): users say the AI swung from too agreeable to pedantic.
- Why it is shared: send to the person it describes, which is exactly why it is risky: the source story involves psychosis, a real vulnerable person. Do NOT use the story; only the general habit.
- Test format, ONE picture: text "Ask ChatGPT if you are right." / "It says yes." / "Ask again. Yes." (max 12 words)
- Products: ChatGPT.
- DUPLICATE: dropped in the duplicate check (episodes 72, 73 cover "ChatGPT just agrees with you"). Listed to show what was found. Not recommended.

### 7. "Is this video AI or real? I can't tell anymore"
- Felt situation: you watch a clip and the comments argue about whether it is fake.
- Evidence:
  - https://aifrontierpost.com/articles/next-generation-never-see-real-video/ (13.11.2026): r/ChatGPT, 753 upvotes and 159 comments in about 5.5 hours; comments do frame-by-frame forensics. The article is a secondary source; I did not open the thread.
  - https://aifrontierpost.com/articles/seinfeld-ai-minimax-h3-george-spy-parody/ (10.11.2026): AI Seinfeld clip on r/ChatGPT, 6,200 upvotes, 1,400 comments (secondary source).
  - https://aifrontierpost.com/articles/ai-karen-job-interview-viral-video/ (10.11.2026): r/ArtificialIntelligence, about 5,800 upvotes, 358 comments; the avatar says "absolutely" so often that commenters riff on it.
- Why it is shared: send to the relative who forwards fake clips.
- Test format, ONE picture: a paused video frame with a hand and "REAL?" "AI?" two small circles. Text: "Real or AI? Look at the hands."  (7 words)
- Products: general AI video (MiniMax H3 named by the article), not a chatbot rivalry.
- Warning: the viral Reddit objects were AI VIDEOS, not chatbots; they spread because of the clip, which we cannot copy. Also the CLAUDE.md "Package every episode as an everyday thing" rule asks for AI inside an everyday product.

### 8. "ChatGPT found my lost earbud"
- Felt situation: you dropped something small in a messy place and you wish you had a second pair of eyes.
- Evidence:
  - https://www.ndtvprofit.com/trending/man-loses-earbud-in-gravel-turns-to-chatgpt-finds-it-in-less-than-5-minutes-12239265 (26.10.2026): Reddit post of u/Just_a_fungi893, "over 2,800 upvotes", hundreds of comments. Secondary source; thread not opened.
  - https://www.republicworld.com/viral/ai-to-the-rescue-man-uses-chatgpts-computer-vision-to-find-lost-earbuds-in-minutes-2026-10-27-139762 says "thousands of upvotes".
- Why it is shared: send to the person who always loses earbuds.
- Test format: this one is a TEST, not a joke, so it needs our own real run first (CLAUDE.md: never promise what we did not test). One picture only after we try it on our own photo (not from David's home or window).  Draft text: "ChatGPT found my lost earbud." (5 words)
- Products: ChatGPT (image analysis).
- Warning: one positive story, the OP's claim is not independently verified; success may not repeat. This is the "explainer/test" class David is tired of; only one marked option.

### 9. "They are taking away my ChatGPT voice"
- Felt situation: you like one particular ChatGPT voice and it disappears in December.
- Evidence:
  - https://www.techradar.com/ai-platforms-assistants/chatgpt/im-beyond-disappointed-because-chatgpt-means-a-lot-to-me-users-are-furious-that-openai-is-retiring-their-favorite-voice-modes (11.11.2026): Standard and Advanced voice end 11.12.2026 (the article says December 11); quotes Reddit users, no score printed.
  - https://community.openai.com/t/keep-standard-voice-mode/1414888 (OpenAI forum, not Reddit): petition thread, active 13.11.2026.
- Why it is shared: send to someone who talks to ChatGPT out loud on walks.
- Test format: skip as a reel. It is a news item and an emotional niche ("a small but vocal contingent" per TechRadar). Kept as a low rank to show it was checked.
- Products: ChatGPT.

### 10. "My AI said 'You're absolutely right' while breaking everything"
- Felt situation: you point out a mistake, the AI says "You're absolutely right!" and breaks something else.
- Evidence:
  - https://digg.com/ai/g0t2mp6r (14.11.2026): @ziv_ravid on X (not Reddit) satirical post: Copilot "You're absolutely right, let me revert my changes." / "Fixed! The servers now reject all traffic." Score UNREAD.
  - https://aifrontierpost.com/articles/ai-karen-job-interview-viral-video/: commenters riff on the avatar's overuse of "absolutely" (Reddit, 5,800 upvotes on the thread, not on the joke).
- Why it is shared: send to the developer friend, or anyone who got apologised to by a bot.
- Test format, 7-second text reel: "Me: that is wrong." / "AI: You're absolutely right!" / "AI: (breaks something else)".
- Products: Copilot (named), Claude (known for this phrase, but no source found here, so UNVERIFIED), ChatGPT.
- Check the phrase is still current for each product before naming one.

## Duplicate check (against channel/topics-covered.txt and channel/content-memory.md)

grep keywords: earbud, usage limit, weekly limit, voice, absolutely right, Google Assistant, Geminification, subscription, yes man, sycophan, want me, follow-up, dumber, Gemini, WhatsApp, Meta AI, friend, ghost, 2am, cancel, karen, real video, Seinfeld.

- 1 Gemini replaces Assistant: no hit for "Google Assistant", "Geminification", "assistant". Only Gemini episodes found are 15 (formula), 61 and 83 (can people read your chats), 86 (secret test). NOT a duplicate.
- 2 "Want me to" follow-ups: no hit for "want me", "follow-up". Not an episode. BUT content-memory.md line 1762-1763 records the "Me with Claude / Me with ChatGPT" picture with "endless 'one more thing'": same felt habit. Treated as a SIBLING of the winner, not clean. Keep, flagged.
- 3 Paying for three AIs: ep41 and ep50 are about bank-account subscriptions, not AI chatbot subscriptions; no hit for "cancel". NOT a duplicate, but near ep50's "subscriptions" angle, so the picture must say "three AIs".
- 4 Usage limits: no hit for "usage limit", "weekly limit", "limit". Nearest is ep82 "Did Claude get dumber on purpose? ... effort setting", which is a different angle. NOT a duplicate.
- 5 "Ready in 45 minutes": ep90 "ChatGPT picks a number then gets ghosted ... begs for a second chance" is the reverse (the user ghosts the AI). Partly adjacent; keep as weak.
- 6 Agrees with everything: DUPLICATE, episodes 72 ("Does ChatGPT just agree with you?"), 73 ("3 ways to make ChatGPT stop agreeing with you"), 80 ("Does your ChatGPT cave when you push?"), 14. Dropped from the ranking list as a recommendation.
- 7 Real or AI video: ep54 covers "video call might not have a real face" and ep38 voice cloning. Different scope (a clip, not a call), but near. Keep, flagged.
- 8 Earbud: no hit. ep74 to 77 are photo location tests (ChatGPT finding a street), a related "ChatGPT reads a photo" family but not the same. NOT a duplicate.
- 9 Voice retirement: no hit (only voice cloning ep38, Echo ep55). NOT a duplicate.
- 10 "You're absolutely right": no hit. NOT a duplicate.

After dropping the duplicate (6) the clean list is 9 candidates; 2, 5 and 7 carry a "near" flag.

## Honest notes

- Direct Reddit was unreadable: no live top-posts list, no top comments straight from Reddit for the last 7 days. UNREAD: the real score and comment count of every thread cited through a snapshot (May to Aug 2026), and the scores of the posts behind candidates 1, 2, 3, 4, 5, 6, 9, 10.
- Printed numbers I did read: earbud post "over 2,800 upvotes" (NDTV Profit, 26.10); r/ChatGPT real-vs-AI video 753 upvotes / 159 comments (aifrontierpost, 13.11); AI Seinfeld 6,200 / 1,400 (aifrontierpost, 10.11); AI Karen 5,800 / 358 (aifrontierpost, 10.11). These are secondary sources, not checked against Reddit.
- The aifrontierpost, wegotthiscovered and tricklings sites are small aggregators; their accuracy is unverified.
- The sentinel-team snapshots are captured copies; their "posted N days ago" labels do not match the snapshot dates, so treat the dates as approximate. They are older than the 30-day window.
- Candidates 1-5 and 10 are patterns that appear in several unrelated threads, which is the stronger kind of evidence; 7 and 8 are single viral posts, the weaker kind (CLAUDE.md: one outlier is not a pattern).
- Everything here is a hypothesis from reading, not a measurement. The winner picture is n = 1, a trial audience and an AI-looking image.
- Recommended order to test as a picture (cheapest first): 1, 3, 2 (sibling of the winner), 4. Nothing else needs a build.
- David's rules applied: no code words in text, max 12 words, real logos for named products, rotation of products across the list (Google, ChatGPT, Claude, Copilot). No candidate covers Meta AI, Grok or local models; the one Meta AI joke found (WhatsApp AI not knowing it is in WhatsApp) came from a roundup (tricklings item 7, u/Buzstringer) and was not verified, so it is not ranked.
- Fix needed in candidate 2: the first snapshot URL above may be incomplete; use the search result "Do you feel bad not responding to the follow up questions" on reddit.sentinel-team.org to find the exact page.
