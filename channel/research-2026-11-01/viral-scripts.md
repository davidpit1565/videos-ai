# Viral AI-tip short videos: script structure study (1.11.2026)

Written for David / the Actually Works channel. Every claim is labelled FACT (with source), HYPOTHESIS or UNKNOWN. No untraceable statistics are used. Nothing here was watched by eye: all structure comes from transcripts and captions, so visuals are UNKNOWN.

## 0. Method and limits (read first)

- **How the sample was built.** Search tools cannot list recent TikToks, so the sample comes from public aggregator pages that show views, likes, shares, saves and captions per video: `ttanon.com/@maverickgpt`, `ttanon.com/@taki.gpt`, `ttanon.com/@sabrina_ramonov`, `ttanon.com/@justinfineberg`, `viewlify.app/profile/<handle>` (adds full spoken transcripts), `aipick.news` (adds auto-transcripts of single TikToks), `picmany.com` (Instagram reels). Facebook (Dan Martell) came from `yt-dlp` (metadata plus the platform's own caption file). Older Maverick/Sabrina TikToks came from the public video page itself (view counts, the caption track).
- **What could NOT be done.** YouTube Shorts: YouTube answers single-video requests with a bot check ("Sign in to confirm you're not a bot"). I did not work around it, so there are no YouTube transcripts. Instagram blocks anonymous download: only plays/likes via PicMany. Numbers are snapshots from the aggregators' last crawl (about 25-31.10.2026), not live.
- **Window.** "Last 3 months" (from 1.8.2026) is met by rows A-M. Rows N-S are older (Jan-May 2026) and flagged; they are included because they are the biggest hits of the same creators and the only ones with exact per-second transcripts. Do not read them as "recent".
- **Selection bias (important).** Most rows come from 4 creators (Maverick Maltin, Taki Wong, Sabrina Ramonov, Justin Fineberg) because those are the accounts the tools could read. n is small. Every "rule" below is a HYPOTHESIS supported by at least two examples, not a causal finding. It is consistent with our own earlier study (`hook-research-20-10.md`): wording explains very little of the view differences (R-squared 0.017 on 9,387 YouTube Shorts, FACT, our own file).
- **Self-claims.** Many hooks contain numbers the creator did not source ("27% of the time", "57% (Stanford)", "150 million views"). I list them as hooks, never as facts.

## 1. The table

Seconds are real caption timestamps where marked "(cue)"; "(est.)" means position in the transcript scaled to the video length, so treat as plus/minus 2 s. "Fix" = the first actionable instruction (a click, a command, a prompt to paste).

| # | Creator | Platform, date | URL / source | Views / likes (FACT) | Length | Hook, first line (spoken unless noted) | Fix starts | CTA |
|---|---|---|---|---|---|---|---|---|
| A | Dan Martell (benchmark) | Facebook reel, 13.9.2026 | https://www.facebook.com/share/r/1DKNDc2YEm/ | 4,960,113 views (yt-dlp `view_count`), 99K reactions. NOTE: the post title says "5.9K views", which contradicts it; UNKNOWN which is right, the metadata number matches David's "5M" | 29 s | "Gpt is a yes man. It literally agrees with you on everything." | 8.2 s "here's how I reprogram it" (cue); 11.4 s first click; prompt read at 17.9 s | None. Last line is the payoff: "That's how you finally get the AI to be direct with you." |
| B | Maverick Maltin | TikTok, 30.10.2026 | https://ttanon.com/@maverickgpt ; transcript https://aipick.news/items/pso9zbmzszmi87ujq0zb96rcb | 1.4M views, 88K likes, 975 comments, 20K shares, 8.1K saves; Instagram copy 2.2M plays, 60.9K likes (picmany.com/mavgpt) | 19 s | "This has to be one of the craziest ChatGPT use cases that I've ever seen." (caption: "AI is actually getting out of hand...") | No fix: it is a story. Payoff ("two minutes later ChatGPT found them") at about 6 s (est.) | "make sure to follow me" |
| C | Maverick Maltin | TikTok, 25.10.2026 | https://ttanon.com/@maverickgpt | 1.1M views, 62K likes, 317 comments, 18K shares, 64K saves | 25 s | Caption: "The best AI tool for every job: Writing emails -> ChatGPT, Turning notes into a plan -> Claude..." Spoken script UNKNOWN | UNKNOWN (list from second 0, as his similar 974K video N) | Instagram caption: comment "Tools"; TikTok: "Save this so you know which one to open" (caption) |
| D | Maverick Maltin | TikTok, 27.10.2026 | ttanon.com/@maverickgpt | 43.3K views, 2K likes, 676 shares, 2.4K saves | 26 s | Caption: "5 Secret Photo codes for ChatGPT" | UNKNOWN (list) | caption only |
| E | Maverick Maltin | TikTok, 23.10.2026 | ttanon.com/@maverickgpt | 97.4K views, 3.4K likes, 1.3K shares, 4.3K saves | 34 s | Caption: "ChatGPT just started leaving watermarks on everything it creates, so here's how to remove them in 30 seconds." | UNKNOWN | UNKNOWN |
| F | Taki Wong | TikTok, 20.10.2026 | https://viewlify.app/profile/taki.gpt | 200K views (viewlify; ttanon says 230K), 12K likes, 3.6K shares, 1.6K comments, "12.5x his usual" | 59 s | "Claude, edit this video and add these effects." | 0 s (the command is the hook) | "Comment the word edit and I'll send you everything" |
| G | Taki Wong | TikTok, 27.10.2026 | ttanon.com/@taki.gpt | 170K views, 4.2K likes | 66 s | Caption: same watermark topic as E | UNKNOWN | link in bio |
| H | Paul Automatise (French) | TikTok, 27.10.2026 | https://aipick.news/items/cl0jhpfxf010h9i1iyfooob2s | Views UNKNOWN. aipick: likes = 1.1x his follower count, about 4.6x his usual | UNKNOWN | "You trusted ChatGPT, and it tells you peanut butter does contain peanuts. And when you say it was wrong: 'You're totally right, I'm sincerely sorry.' That's not an AI, it's a mirror." | about 25% into the transcript (est.): "go to settings, personalization, custom instructions" | "comment 'fiable'... subscribe" |
| I | Better With AI | TikTok, 15.10.2026 | https://aipick.news/items/uitk3llvmx7ao0acgc52t470r | Views UNKNOWN (aipick marks it a low-follower hit, likes 3.6x followers) | UNKNOWN | "It's become a running joke about ChatGPT giving wrong instructions and then apologizing for it later." | about 20% (est.) | "Follow me" |
| J | Nathan Hodgson | TikTok, 29.10.2026 | https://aipick.news/items/zaaqqlzq9g0je3abjwhnlsx1d | Numbers UNKNOWN | UNKNOWN | "Everyone knows you're using AI for writing, especially your boss." | "Step one" at about 25% (est.) | "follow and save this video" |
| K | Maverick Maltin | TikTok, 5.10.2026 | https://viewlify.app/profile/maverickgpt | 2.1K views, 102 likes, 25 shares | 42 s | "ChatGPT agrees with you 57% of the time, even when you're completely wrong." | about 12 s (est.) "here's exactly how you can fix this in the next 30 seconds" | comment "honest" |
| L | Sabrina Ramonov | TikTok, 24.10.2026 | ttanon.com/@sabrina_ramonov | 20.4K views, 1K likes | 25 s | Caption: "Practice interviews with tougher questions." | UNKNOWN | "Hit follow and tell me: ..." (her standard caption line) |
| M | Sabrina Ramonov | TikTok, 16.10.2026 | ttanon.com/@sabrina_ramonov | 19.8K views, 1.1K likes | 32 s | Caption: "ChatGPT explanations shouldn't need decoding... ELI Cactus" | UNKNOWN | same |
| N | Maverick Maltin (older) | TikTok, 22.5.2026 | https://www.tiktok.com/@maverickgpt/video/7642701535692033310 | 4.9M plays, 188K likes, 19.1K shares, 25.3K comments, 34.5K saves | 21 s | "People are now asking ChatGPT to take a selfie of itself, and this is literally breaking the internet." | 4.0 s (cue) | "comment 'selfie' and I'll send it" |
| O | Maverick Maltin (older) | TikTok, 17.3.2026 | https://www.tiktok.com/@maverickgpt/video/7618343189316930847 | 4.5M plays, 253K likes, 129K shares, 245K saves | 34 s | "Here are five secret codes for ChatGPT." | 2.3 s (cue) | "comment 'list'" |
| P | Maverick Maltin (older) | TikTok, 9.2.2026 | https://www.tiktok.com/@maverickgpt/video/7604921386242542878 | 1.3M plays, 53K likes, 9.1K shares, 40.8K saves | 36 s | "ChatGPT lies to you 27% of the time. Use this exact prompt to force it to always tell the truth." (the 27% is unsourced) | 2.5 s ("use this exact prompt"), real steps at 22.8 s | "comment 'truth'" |
| Q | Maverick Maltin (older) | TikTok, 19.3.2026 | https://www.tiktok.com/@maverickgpt/video/7618973209580375326 | 974K plays, 64.6K likes, 24.4K shares, 70K saves | 29 s | "For writing, this is bad. This is great for brainstorming. This is bad..." | 0 s (it is a verdict list) | none audible; caption "follow" |
| R | Sabrina Ramonov (older) | TikTok, 17.1.2026 | https://www.tiktok.com/@sabrina_ramonov/video/7596436583557942558 | 978K plays, 51.5K likes, 16.4K shares, 66K saves | 62 s | "...rewrite your resume to become un-rejectable? I tried this and it's like having the cheat code to the company's hiring process." | 18.3 s (cue) | "save this video and hit follow" (at 12 s) |
| S | Maverick Maltin (older) | TikTok, 21.3.2026 | https://www.tiktok.com/@maverickgpt/video/7619755608824302878 | 78.1K plays, 2.4K likes, 875 shares | 24 s | "ChatGPT just agrees with everything you say, but this one prompt fixes that forever." | 3.7 s (cue) | "follow me and drop 'prompt' in the comments" |

Sources for the numbers: aggregator pages above (ttanon, viewlify, aipick, picmany), the TikTok page JSON for N-S, yt-dlp for A. All FACT as snapshots; none verified against the platforms' own analytics.

## 2. Per-video structure measurements (only where a transcript exists)

| Video | Words | Seconds | Words/sec | Claims | Copy-paste artifact | Artifact share of the words |
|---|---|---|---|---|---|---|
| A Dan | 85 | 29.1 | 2.9 | 1 claim, 1 fix | prompt, 17 words ("Be my ruthless mentor. Challenge my assumptions. Stress test everything. I need bullet proof thinking not validation.") | 20% |
| B earbuds | 96 | 19 | 5.0 | 1 | none (a story with the photo) | 0% |
| N selfie | 107 | 21 | 5.1 | 1 | prompt NOT said (gated by comment) | 0% |
| O codes | 137 | 34 | 4.0 | 5 items | five short codes, said in full | about 35% |
| P truth | 156 | 36 | 4.3 | 1 | prompt NOT said (gated) | 0% |
| Q good/bad | 109 | 29 | 3.8 | 13 verdicts | none | 0% |
| S ruthless mentor | 101 | 24 | 4.2 | 1 | prompt, about 30 words | about 30% |
| K honest | 189 | 42 | 4.5 (est.) | 1 plus a trick | prompt, about 58 words | about 31% |
| F Taki edit | 122 | 59 | 2.1 | 1 (a list of effect names) | list of effect names | about 50% |
| R Sabrina resume | 220 | 62 | 3.6 | 3 prompts | prompts said in full | most of it |

Engagement ratios (FACT arithmetic on the numbers in the table): list/tool videos carry the saves (C: 64K saves on 1.1M views = 5.8%; O: 245K on 4.5M = 5.4%; Q: 7.2%), story and novelty videos carry shares and likes (B: shares 1.4%, saves 0.6%, likes 6.3%; N: shares 0.4%, saves 0.7%, comments 0.5%). Dan: reactions 2.0% of views.

## 3. Script-structure RULES (each backed by at least two examples; all HYPOTHESES)

**R1. The tool name and a plain judgment are in the first 5 words.** A "Gpt is a yes man." (5 words); S "ChatGPT just agrees with everything you say" (7); P "ChatGPT lies to you 27% of the time" (7); O "Here are five secret codes for ChatGPT" (7); Q "For writing, this is bad." (5). Nobody in the set opens with setup or a story. (Matches the 28.10 rule and episode 81's `ChatGPT is a freaking yes-man!`.) HYPOTHESIS: this is necessary, not sufficient, see R11.

**R2. Almost all the big hits are 19-36 s.** B 19 s, N 21 s, S 24 s, C 25 s, A 29 s, Q 29 s, O 34 s, P 36 s. Exceptions exist: R (62 s, 978K) and F (59 s, 200K). FACT about this sample; HYPOTHESIS that short helps (no retention data exists, and Maverick's own 69 s "dots" post reached 725K with 0 comments, so length is clearly not the only driver). UNKNOWN: whether these viewers watched to the end.

**R3. The fix or the payoff arrives within 2.5-8 s, and the viewer is told early that it is coming.** O 2.3 s, P 2.5 s, S 3.7 s, N 4.0 s, A 8.2 s ("here's how I reprogram it"), B about 6 s. Counter-example: R delays to 18 s but spends the time on a promise ("exact three prompt chains") and still got 978K. Dan is the slowest of the big ones, which says 8 s is acceptable, not that later is better.

**R4. One claim per video.** A, B, N, P, S each make exactly one claim and one action (or one story). List videos (O 5 items, Q 13 items) replace claims with a rhythm (see R7). Videos that stack several ideas or run 59-66 s (F, G) land at 170-200K for an account of 259K followers; that is good for him, but below the 19-36 s single-claim hits of an account of 626K followers (not a like-for-like comparison).

**R5. The copy-paste artifact is tiny and read out loud, word for word.** A 17 words, S about 30, O five codes of 1-2 words each. In the gated versions (N, P) the creator withholds the artifact and asks for a comment keyword; those still did very well (4.9M, 1.3M), so inline artifact is not required for reach, but it is what Dan did, and it makes the video saveable without a DM. HYPOTHESIS: a reader who hears 17 words can pause and type them; 100 words cannot be taken in by ear.

**R6. Use the same plain settings path, spoken as nouns.** "Settings, personalization, custom instructions" appears in A, S, K, H, I, J and P (7 videos; FACT from transcripts). Plain words, no UI jargon, three nouns. Caveat: it also means the "ChatGPT is a yes man" topic is crowded (R11).

**R7. A fast verdict-list rhythm gets saved.** Q ("this is bad / this is great for X" repeated 13 times in 29 s, 70K saves) and C ("Writing emails -> ChatGPT..." 1.1M views, 64K saves) are both ranking lists; O is a numbered list of 5. All three have a saves-per-view ratio of 5.4-7.2% (computed above); the story/novelty videos are at 0.6-0.7%. HYPOTHESIS: a list is easy to save for later; stories (B) get shares instead.

**R8. A story with an unbelievable result and the photo in frame can outperform every tutorial.** B (19 s, 1.4M, 20K shares): "lost his earbuds in a pile of gravel... ChatGPT found them". N (21 s, 4.9M): "ChatGPT takes a selfie of itself". Both are "look what people do with it", not a lesson. FACT: B retells a Reddit story that Newsgram reported on 27.10.2026 (https://www.newsgram.com/science/2026/10/27/viral-chatgpt-locate-the-lost-earbud-reddit-story), three days before the video, so it is a reshare. For us: a retold story needs credit and a check that it is real (never-fabricate rule).

**R9. The word "this"/"these" plus a concrete object, not a category.** "this one prompt", "this exact prompt", "this is bad". Every spoken hook points at a thing the viewer can picture or already knows (the settings page, the word "yes man"). No hook in the set is abstract ("a new way to think about AI").

**R10. Creators end on an action line ("comment X", "follow me") in 11 of the 12 videos whose ending I could read (A, B, F, H, I, J, K, N, O, P, R, S); the exception is A (Dan: none). Q's ending is UNKNOWN.** The action is nearly always a comment keyword ("comment 'selfie'", "'list'", "'truth'", "'edit'", "'prompt'"). FACT: N has 25.3K comments on 4.9M views (0.5%). HYPOTHESIS: the keyword gate inflates comments; nobody in this set ends on "tomorrow I'll show you..." or "the setup is in the link in bio".

**R11. Wording is not what separates a hit from a flop: the same script got very different reach.** Same prompt, same topic: S (Maverick, 21.3.2026, "ruthless mentor... stress test everything... bulletproof", 78.1K plays) vs A (Dan, 13.9.2026, nearly the same prompt, 4.96M); K (Maverick, 5.10, 2.1K) vs H (Paul, French, 4.6x his usual). FACT: Dan's wording matches Maverick's earlier caption almost word for word; HYPOTHESIS: account reach and timing, not script, explain most of the gap (consistent with our R-squared 0.017 and the 0.81 audience-size correlation in `hook-research-20-10.md`). Do not read the table as "copy these words and 5M follows".

**R12. Hits are rare outliers of a high-volume account.** Maverick's median post is 8.8K views (FACT, ttanon), his recent top three are 725K-1.4M (80-160x the median), and he posts about 14 times a week. Of his latest 30 videos, 3 passed 100K. Of Sabrina's latest 30, none passed 21K; of Justin's, none passed 72K. For a small account this says: volume of attempts, not one perfect script (HYPOTHESIS).

**R13. Specific named products and features of this month carry the novelty.** B, C, F, G, E all name a current product or feature (ChatGPT, Claude, "textGrain" watermark news, Claude Opus 5.5). We still must verify live before writing (CLAUDE.md rule). The watermark topic (E, G, 97K and 170K) is a news hook: FACT that two creators posted it within 4 days (23.10 and 27.10).

**R14. Voice pace does not matter as much as clarity.** The 5M benchmark A is the slowest of the big hits (2.9 words/s); B and N are fastest (5.0-5.1). Top hits span 2.9-5.1 words/s. No pace "rule" is supportable. Our own voice is calm; this does not contradict anything measured here.

## 4. Five hook templates (plain English a 8-year-old understands)

Each is built from the patterns above, not copied. Fill with a product that is verified live, and only claims we can show on screen.

1. **"[Product] is a [plain word]."** Pattern A/R1. Example: "ChatGPT is a yes-man." (ep 81 used it; for another topic: "Your phone is a snitch.") Why: subject plus judgment in 5 words, no explanation needed.
2. **"People are asking [product] to [odd thing]."** Pattern N. Example: "People are asking ChatGPT to take a selfie of itself." Then, in under 5 s, say what to type. Needs a verified, current trend.
3. **"Five short words that make [product] [better thing]."** Pattern O. Example: "Five short words that make ChatGPT explain like you're ten." Say the five words out loud, with the screen showing them. Do NOT claim "10x better" (unsourced).
4. **"[Product] is good at this. And bad at this."** Pattern Q/C. Example: "ChatGPT is great for this. And bad for this." Repeat the pair with a short verdict each time; one tiny proof on screen per pair. No numbers we have not measured.
5. **"A man lost [thing]. [Product] found it in two minutes."** Pattern B/R8. Example: "He lost his earbud in the gravel. ChatGPT found it." Only with a real, checkable story, credited by name or link, and the real photo on screen.

Also usable: "ChatGPT agrees with you even when you're wrong." (same shape as A and S; claim must be shown live, not a number from a study we have not read).

## 5. Where these findings contradict CLAUDE.md

1. **Length 45-75 s (Length rule).** Of the 8 biggest hits in this sample, 7 are 19-36 s. Exceptions: R 62 s and F 59 s. CLAUDE.md justifies 45-75 s with Buffer/Socialinsider data; this sample says nothing about those studies, but it does not support them for this niche. Ep 81 (25 s, about 200 views) already went short and did not become a hit, which fits R11 (length alone does nothing). Suggested: treat length as a variable to test, not a fixed band. UNKNOWN: retention.
2. **Final line names tomorrow's episode.** None of the 12 videos with a readable ending does this. They use a comment keyword or "follow me", or nothing (Dan). Our own claim ("converts several times better") rests on vendor blogs, which `CLAUDE.md` itself calls "trust the direction, not the numbers". Not disproved (this study cannot see follows), but nothing here supports it. Suggested: test one episode with Dan's ending (end on the payoff) against a tomorrow line.
3. **"The setup's in the link in bio" second-to-last.** Top videos either give the artifact inline in the video (A, S, O: 17-30 words) or gate it behind a comment keyword (N, P). None says "link in bio" at the end except Taki (F, G caption). Suggested: say the 17-word artifact out loud in the video (R5) and keep the full guide on `/e/N`; this does not break the "full setup path on the site" rule, it just moves the key line into the audio.
4. **Never repeat a hook type two episodes in a row.** Maverick repeats one template ("What happens when you ask ChatGPT to... I tried this and...", "5 secret codes...") in at least 8 of his latest 30 posts, and his biggest recent hit is a different format (B). HYPOTHESIS only; the repeated template gives him a median of 8.8K, so it is not a proven winner either. Keep the rule; do not conclude from this study that it is wrong.
5. **Real logo on screen, long structured setup per episode.** Not contradicted. None of the creators' scripts needs it; whether the logo helps reach is UNKNOWN (visuals were not inspected).
6. **Never fabricate.** The creators' hooks use unsourced numbers (P "27%", K "57% (Stanford)", Maverick's "150 million views"). We must not copy any such number; each one needs a source we can open, or it is dropped.
7. **Topic picked from the demand report, a new angle per episode.** The topic "ChatGPT is a yes man / stop it agreeing" appears in at least 7 videos in the last month (A, S, H, K, I and others). Dan's reach beat all of them with near-identical content (R11). So topic uniqueness is not what made him big: reach is. Whether we should keep chasing unique angles over account growth is a judgment call for David.

## 6. UNKNOWN list (so nobody fills it in from memory)

- Retention/watch time of any video here (platform analytics are private).
- The spoken script of C (1.1M), D, E, G, L, M (only captions were readable).
- Whether Dan's "5.9K views" title or 4.96M metadata number is right.
- Visuals: layout, face on screen, captions style, music, cuts.
- Whether the aggregators' numbers include replays or bot traffic. Maverick's 69 s "dots" post (725K views, 0 comments, 1.2K likes) looks unlike his organic hits; the ratio is odd and UNEXPLAINED.
- Any causal link between hook wording and views.
