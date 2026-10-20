# Hook and virality research — 20.10.2026 (revised the same evening with a measured data study)

**Revision note.** The first version of this file was built from five web-search passes and was thin: search tools cannot read TikTok, Instagram or Reddit, and most "hook statistics" online have no traceable source. Instead of repeating the same searches, section 0 below is a data study built from platform data that the tools CAN read (YouTube Shorts via `yt-dlp`, and individual TikTok video pages). Sections 1-8 are the earlier literature and corpus passes, kept as they were.

## 0. Data study: YouTube Shorts from 174 AI channels (n = 9,387 Shorts) — expanded the same night

**Method.** Channels found by about 120 AI-topic searches (ChatGPT, Claude, Gemini, prompts, agents, automation, image/video tools, coding, study and work uses, news); kept a channel if at least 35% of its Shorts titles name AI or a tool and it had 25+ Shorts of 61 s or less in its latest 60. For each Short: views divided by the channel's own median (the **lift**), so a channel's audience size cancels out. For each title feature: the average difference in log-lift between titles with and without it, **within the same channel**, averaged over channels (bootstrap 95% interval over channels), with a split-half check (random half of the channels against the other half). Data: `channel/hook-corpus-youtube-shorts-ai-20-10-2026.csv`. The first run (98 channels, 5,341 Shorts) is superseded; the larger run changed one result (numbers in titles shrank from about x1.13 to a non-significant x1.07), which is why the sample was expanded.

**Grade: A for the numbers (platform data read directly); B for the conclusions (correlational, titles not spoken hooks, YouTube Shorts not Reels/TikTok, latest 60 Shorts per channel).**

**Title features (ratio = typical views of titles with the feature vs without, same channel; stars = interval excludes no effect; "both halves" = same sign in both halves):**
- "How to ..." promise: about **x1.3** (58 channels; 71% of channels positive; both halves).
- Names the tool or product (ChatGPT, Claude, Gemini...): about **x1.23** (128 channels; both halves).
- Says "free": about **x1.34** (36 channels; wide interval; both halves same sign).
- ALL-CAPS word: about **x1.23** (69 channels; both halves same sign).
- Addresses the viewer with "you/your": about **x0.88** (136 channels; negative in both halves; only 37% of channels positive). This goes against our assumption that direct address is a stronger hook, at least in titles.
- Negative framing (stop, never, mistake, wrong, scam): about x0.88, not significant.
- No measurable effect: number in the title (x1.07, not significant), question mark, first person, hype words, "this/these", "secret/hack", news-recency words, emoji, exclamation, colon/dash, title length (short or long), starts with a number.

**Topic and length (same method):** image/video-tool topics about x1.21 (80 channels, interval above 1); ChatGPT, Claude, Gemini, prompts, agents/automation, coding, money, study/work and news topics: no measurable difference once the channel is held fixed. Duration within the 61-second Shorts range: not tested further than the filter.

**The numbers that matter most:**
1. All title, topic and duration features together explain **1.7% of the variation between one channel's own Shorts** (R-squared 0.017, n = 9,387). The typical swing inside a channel is about x2.9; the top 1% are 60x its median. Wording moves views by roughly 10-35%; the spread between a channel's own videos is far larger. The text is a modest edge, not the driver.
2. **Between channels the picture is the opposite:** a channel's median Shorts views against its subscriber count (log-log, 173 channels) has slope 0.54 and correlation 0.81. Audience size explains most of the difference in views; for a small account, reach to non-followers is the whole game, and a title edge of 20-30% will not replace it.

**What the biggest organic outliers look like** (creator channels, lift versus own median; views as read from YouTube): "Talk to Your CRM with Claude (This Changes Everything)" (8.0M, x1,481 on a 92k-subscriber channel), "Make AI Writing Sound Actually Human" (3.2M), "The One Thing That Stops Every AI Agent" (5.7M), "HeyGen AI video generator just changed the game..." (5.3M), "Your AI agent NEEDS 4 types of memory... It has 1" (518k), "ChatGPT, Show Me an IPhone" (419k) and "ChatGPT Repeat After Me" (218k) (a person talking to the AI), "Stop Paying for 5 AI Tools (Use This Instead)" (4.6M). Common elements: a named tool, a concrete payoff or one specific unanswered question, often a how-to. Brand and promoted videos (certificates, PDF-tool ads) dominate the very top of the raw list and were excluded from the robustness run.

**Limits that matter.** (1) Titles stand in for the hook; the spoken first sentence could not be measured: YouTube blocked media access from this server, and automatic captions were blocked after the first few requests (rate limit and bot check), so only about a dozen were read. (2) YouTube Shorts count a view from the first frame (since 24.8.2026), so views include swipe-aways. (3) Latest 60 Shorts per channel only. (4) AI-niche channels that surface in search are larger and more professional than a 30-follower account. (5) Nothing here is causal. (6) 22 title features were tested; about one chance "significant" result is expected, which is why only effects that held in both halves are listed.

**What this changes in our practice:** (a) name the tool or the object in the first words; (b) a concrete how-to or one specific unanswered question, honestly kept; (c) do not assume "you"-address or hype words help; (d) a number in the title is not supported; (e) expect a hook to move results by tens of percent, so topic, payoff and reach to non-followers deserve most of the effort; (f) keep the hook honest, since the edge is small and the cost of a broken promise is unmeasured.

---


Five research passes (web search and page fetches only; TikTok, Instagram and Reddit pages could not be read by the tools except individual TikTok video pages), plus one corpus of our own built from public TikTok pages. Written from the reports, not from memory. Grades: A = replicated/meta-analytic or primary with method, B = solid single study or primary without method, C = vendor/blog/secondary, D = untraceable.

## 1. What the platforms say about ranking (and what nobody publishes)
- TikTok Newsroom (primary, B): ranking uses user interactions, video information and device settings; factors are "weighted based on their value to a user"; finishing a longer video is named as a stronger signal than a weak one; early replays and likes start an early distribution round. No ranked list of signals and no weights.
- Instagram, via Mosseri as quoted by blogs (C; original videos unreachable): the three most important ranking signals are watch time, likes and sends per reach; likes count a little more for followers, sends a little more for non-followers (Jan 2025). Another quote, May 2024, that sends correlate with reach "more than anything else" (blog quote, unverified).
- YouTube blog (primary, B): from 24.8.2026 views are counted from the first frame; "engaged views" keep the old definition; no change to recommendations. Public view counts therefore now include swipe-aways.
- Nobody publishes numeric weights. Any "3-5x for sends" or "saves count 3x" is untraceable (D).

## 2. Psychology: what is supported, and how far
- Curiosity is triggered by a specific knowledge gap (Loewenstein 1994; Golman and Loewenstein 2018: people feel the gap only when they have a specific question in mind). Grade B. Lab trivia, not hooks. Practical reading: a vague teaser may create no gap; a concrete unanswered question does.
- Curiosity engages reward circuitry and helps memory (Kang 2009; Gruber, Gelman, Ranganath 2014). Grade B, small fMRI studies. It shows learning, not scroll-stopping.
- Surprise attracts gaze in natural video (Itti and Baldi; 72% of gaze shifts landed on above-average surprising locations; about 0.7 predictive score against 0.6 for contrast). Grade B. Where the eye goes, not whether the viewer stays.
- Self-relevance: own-name capture is partial (about a third noticed their name; Wood and Cowan 34.6%), memory advantage for self-referenced material is a meta-analytic result (Symons and Johnson 1997). Grade A for memory, B for capture.
- Negativity: PNAS 2019, 17 countries, 1,156 people: higher arousal to negative video news on average; up to about 40% showed no bias. Grade B+.
- Cuts and motion: dose-dependent, 1990s TV, contested orienting response. Grade B-/C. Too many unrelated cuts hurt memory.
- Processing fluency: easier-to-process material is judged more positively (Alter and Oppenheimer 2009, abstract level). Lab-robust; not checked for replication.
- Curse of knowledge (Newton 1990 tapping study: tappers predicted 50% would guess the song, 2.5% did). Best traceable support for not assuming the viewer knows the topic.
- No peer-reviewed study was found that measures first-seconds drop-off in short video with eye-tracking or EEG. That gap is itself a finding.

## 3. Claims to AVOID (contested, untraceable or myths)
- "Zeigarnik effect makes open loops stick": a 2025 meta-analysis (Ghibellini and Meier) reports the memory advantage did not replicate; the urge to resume held up. Use curiosity theory instead.
- "Attention span is 8 seconds, like a goldfish": a myth traced to a 2015 report that did not trace to its source.
- "Losses loom twice as large": mean about 1.96 in a 2024 meta-analysis of money choices, but contested and not video evidence.
- "65% of viewers leave in 3 seconds", "first 3 seconds decide everything", "47% of value in 3 seconds" (Facebook/Nielsen, commissioned, unclear), "under 70% 3-second retention kills reach": no traceable method; some contradict each other.
- "Sends are weighted 3-5x likes", "saves 3x likes", "21-34 s has the best completion": no method or sample.
- The Buffer 1.1M-video and Socialinsider 11M-post length findings cited in `CLAUDE.md` could not be re-found by two separate searches (already flagged in `growth-research-13-10.md`). Treat 45-75 s as our own rule of thumb, not a sourced optimum.

## 4. Hooks that went viral on AI content: very thin
- No primary case where a creator quotes their own hook and credits it. Third-party examples only (C/D): "POV: You wake up in 1351 during the Black Plague" (AI-made history video, account @timetravellerpov, reported 19.5M and 21.8M views by a vendor blog), "YOUR AI VIDEOS LOOK SO FAKE" (on-screen overlay, no numbers), generic template lists with no results.
- Vendor structure data (D): a claimed 500-Shorts study (numbered about 30%, curiosity gap about 25%, mid-action 20%, contrarian 15%); a claimed 34,635-clip dataset (project and product showcase hooks about 2x the lowest type). Direction only.
- Reported pattern for AI educators (C): show the tool, the prompt and the result ("the visible test"; Riley Brown, 1M+ followers across platforms per secondary profiles).
- Hebrew/Flemish AI short-video creators: none found by search. Could be a search limit; check in the apps.

## 5. Why hooks fail: no rigorous data
- Only vendor assertions (logo intros, "welcome back" preambles, slow cold opens). No retention numbers traceable.
- Clickbait and trust (all about news headlines, not video): mixed. Three experiments/surveys found lower perceived credibility; Munger et al. 2020 found null effects. "A broken promise costs trust" is plausible, not established. The channel's own follow rate is the test.
- Silent viewing: publisher-reported figures of 50-85% of Facebook video views without sound (self-reported, dated, not Reels). Supports hooks that read without sound.

## 6. Our own corpus (the only new data in this pass)
Source: a public Hugging Face dataset (Gopher-Lab/Tiktok_Chatgpt_Prompt_Guide, scraped 5.8.2025, 47 TikTok video links with spoken transcripts); I read each video's public stats from its TikTok page on 20.10.2026. 43 of 47 pages read. File: `channel/hook-corpus-chatgpt-tiktok-20-10-2026.csv`.
- Selection bias: a scraper's list of ChatGPT-tip videos, median 760k plays. It is a sample of videos that already did well, not of ChatGPT TikToks in general. It cannot say what makes a video succeed, only what successful ones look like.
- Medians: saves 3.3% of plays, shares 0.85%, likes 5.9%, duration 80 s (13 videos at 60 s or less had median 833k plays, 30 longer ones 658k; n too small to conclude).
- Our episode 72 had no saves and no shares at 4.5 hours. Savable how-to content in this corpus gets about 3% saves. This matches the hypothesis that 72 gave nobody a step to keep; it does not prove it.
- Crude hook features (first-person opener, "you" address, superlatives, "prompt/hack/tip" words): median plays differ by less than the spread; no feature separates winners from losers at n=43. Do not build rules from this split.
- The top video (12.2M plays, 2.6% shares, 67 s) is a conversation story: "I had that weird conversation with ChatGPT. I said, rule number 1, only respond with one word..." That is the closest relative of our dialogue format (a viewer-visible exchange with the AI), and the biggest by shares in the set. One video; no causal claim.
- Spoken hooks that carried 2-5 million plays on small or mid accounts were first-person and specific about a result or a discovery ("I've been adding this sentence to all my ChatGPT prompts and I get better output every single time", 3.8M, 4.2% saves; "I don't think I've ever seen a prompt like this", 2.4M, 5.6% saves). The weakest videos in the set were not distinguished by any visible hook trait.

## 7. What this means, without going beyond the evidence
1. There is no proven hook formula in the sources. What exists: a coherent, partly supported theory (specific question, self-relevance, honest payoff, plain wording, something to keep or send) and a clear instruction from every platform source: behaviour after the first seconds (finish, replay, send) is what is rewarded.
2. Therefore the hook is a hypothesis per episode, not a rule. Every episode must log the hook type and be read against its own retention curve and sends per reach.
3. The strongest corpus signal is about the payoff, not the opener: savable steps get saves.
4. Our hard rules from `hooks-guide.md` (cold read, plain language, no repeats) are compatible with the evidence, but nothing here proves they cause retention.

## 8. Integration
- Skill: `.claude/skills/viral-hook-lab/` (generic; can be uploaded elsewhere).
- `channel/hooks-guide.md`: pointer plus an evidence-status block (below the title).
- Episode 74 hook candidates were redone with the skill (see `channel/episode-74-script.md`).
- To close the loop: per episode, store hook text, hook type, and the retention graph reading (view at 3 s, 50% watched) in `channel/content-memory.md` after 72 hours.
