# Hook and virality research — 20.10.2026 (revised the same evening with a measured data study)

**Revision note.** The first version of this file was built from five web-search passes and was thin: search tools cannot read TikTok, Instagram or Reddit, and most "hook statistics" online have no traceable source. Instead of repeating the same searches, section 0 below is a data study built from platform data that the tools CAN read (YouTube Shorts via `yt-dlp`, and individual TikTok video pages). Sections 1-8 are the earlier literature and corpus passes, kept as they were.

## 0. Data study: YouTube Shorts from 98 AI channels (n = 5,341 Shorts)

**Method.** Channels found by 60 AI-topic searches (ChatGPT, Claude, Gemini, prompts, agents, automation, AI tools and so on); kept a channel if at least 35% of its Shorts titles name AI/tools, it had 25+ Shorts of 61 s or less in its latest 60. For each Short: views divided by the channel's own median (the **lift**), so a channel's audience size cancels out. For each title feature: the average difference in log-lift between titles with and without the feature, **within the same channel**, averaged over channels (bootstrap 95% interval over channels), with a split-half check (random half of channels vs the other half) and a robustness run without brand/promoted channels (Google, Adobe, Canva, Microsoft, Perplexity, Claude/Anthropic, ElevenLabs and similar) and with extreme values capped. Data: `channel/hook-corpus-youtube-shorts-ai-20-10-2026.csv`.

**Grade: A for the numbers (platform data read directly); B for the conclusions (correlational, titles not spoken hooks, YouTube Shorts not Reels/TikTok, one snapshot of each channel's latest 60 Shorts).**

**Findings (robust run; ratio = typical views of titles with the feature vs without, same channel):**
- Names the tool or product in the title (ChatGPT, Claude, Gemini, ...): about **x1.2** (69 channels; interval x1.03-x1.36; same direction in both halves).
- Contains a number: about **x1.13** (79 channels; both halves same sign).
- "How to ..." promise: about **x1.2** (30 channels; interval just above 1).
- Says "free": about **x1.3** (24 channels; wide interval).
- An ALL-CAPS word: about **x1.26** (39 channels; interval above 1).
- Addresses the viewer with "you/your": about **x0.9** (67 channels; both halves negative, interval below 1). This goes against our assumption that direct address is a stronger hook; at title level it is a small negative.
- Negative framing (stop, never, mistake, wrong, scam...): about **x0.85** (borderline, interval touches 1).
- No measurable difference: question mark, first person ("I"), "this/these", hype words (insane, crazy, game-changing), "secret/hack", news recency words, emoji, exclamation, title length (short or long), colon/dash.
- 22 features were tested; about one "significant" result is expected by chance. The ones above are those that kept the same sign in both halves.

**The most important number: all 22 title features together explain 1.5% of the variation between a channel's Shorts** (R-squared 0.015, channel-fixed). Typical swing inside one channel is about x2.9, from 0.37x of its median at the 10th percentile to 3.4x at the 90th, with a tail up to 60x. **So wording moves views by roughly 10-30%, while the spread between a channel's own videos is ten times larger.** Something other than the title text drives most of it: the topic, the spoken delivery, the visuals, timing, and luck. This study cannot see those. It also means a perfect hook line is worth a modest edge, not a breakout.

**What the biggest organic outliers look like** (creator channels, lift versus own median; views as read from YouTube):
- "Talk to Your CRM with Claude (This Changes Everything)" (8.0M, x1,481, a 92k-subscriber channel).
- "Make AI Writing Sound Actually Human" (3.2M, x577).
- "The One Thing That Stops Every AI Agent" (5.7M, x439).
- "HeyGen AI video generator just changed the game..." (5.3M, x408).
- "Your AI agent NEEDS 4 types of memory... It has 1" (518k, x176).
- "ChatGPT, Show Me an IPhone" (419k, x147) and "ChatGPT Repeat After Me" (218k, x77): a person talking to the AI.
- "Stop Paying for 5 AI Tools (Use This Instead)" (4.6M, x91).
- "Don't sleep on this AI motion tool" (187k, x117).
- Common elements: a named tool, a concrete payoff or one specific unanswered question ("the one thing that stops every agent"), and often a how-to or a number. Several top-lift outliers in the full file are brand or promoted videos (certificates, PDF tool ads); they were excluded from the robust run.

**Limits that matter.** (1) Titles stand in for the hook; the spoken first sentence could not be read because YouTube blocked media access from this server after the first requests (bot check), so spoken hooks are not measured here. (2) YouTube Shorts count a view from the first frame (since 24.8.2026), so views here include swipe-aways. (3) Latest 60 Shorts per channel only, so older hits are missing. (4) AI-niche channels that surface in search are larger and more professional than a 30-follower channel. (5) Nothing here is causal.

**What this changes in our practice:** (a) name the tool or the object in the first words, (b) a concrete how-to or specific-question promise plus a number where honest, (c) do not assume "you"-address or hype words help, (d) expect a hook to move results by tens of percent, so the topic and the payoff deserve the larger share of the effort, (e) keep the hook honest because the effect of wording is small and the cost of a broken promise is unmeasured.

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
