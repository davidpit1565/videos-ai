# Ranking, retention and reel length: what is actually known (research 1.11.2026)

Labels: FACT = traced to a URL I opened this session, with the source's date. HYPOTHESIS = reasoning, not measured. UNKNOWN = could not be confirmed. Statistics from blogs that I could not trace to an original are listed as untraceable and not used.
Tools: WebSearch and WebFetch only (no Firecrawl). Several Instagram pages (help.instagram.com) returned an empty shell to the fetcher, so Instagram's own help text could only be read through search-result summaries (marked).

## 1. What the primary sources say

### Ranking signals
- FACT (Mosseri, Instagram video, quoted by Social Media Today, 22.1.2025, https://www.socialmediatoday.com/news/instagram-shares-algorithm-insights-2025/738034/): "The top three signals that matter most for ranking are watch time, likes and sends." "...pay close attention to average watch time, likes per reach, and sends per reach." "Likes are slightly more important for connected content, and sends are slightly more important for unconnected content." Note: "slightly", not "3-5x". The 3-5x weighting in blogs has no traceable Mosseri quote (UNKNOWN / do not cite).
- FACT (Mosseri via Search Engine Journal, 3.7.2024, https://www.searchenginejournal.com/instagram-algorithm-shift-why-sends-matter-more-than-ever/521389/): "One of the most important signals we use in ranking is sends per reach. So out of all the people who saw your video or photo, how many of them sent it to a friend in a DM?"
- FACT (Instagram, "Instagram Ranking Explained", Mosseri, 31.5.2023, https://about.instagram.com/blog/announcements/instagram-ranking-explained): for Reels, the most important predictions are "how likely you are to reshare a reel, watch a reel all the way through, like it, and go to the audio page." So the older official wording includes completion and audio-page visits. This is 3 years old; the 2025 "top three" is newer and shorter.
- FACT (Mosseri, Instagram video 27.2.2025 (year inferred), summarised by Lindsey Gamble https://www.lindseygamble.com/blog/instagram-reveals-how-its-algorithm-weighs-watch-time-for-reels, video https://www.instagram.com/reel/DGfycasy8VV/): ranking considers both the percentage watched and total seconds watched; 10 s watched on a 1-minute reel counts the same as 10 s on a 10-second reel (Gamble's example, not a verbatim Mosseri quote; I did not hear the video). This is the nearest thing to a primary answer on length: length is not penalised per se, absolute seconds count.
- UNKNOWN: any 2026 Instagram/Mosseri statement that ranks "skip rate in the first 3 s" as the top signal. Blogs and a Reddit post claim it; I found no primary document. Skip rate is a real Insights metric, not a confirmed ranking weight.
- UNKNOWN: whether "sends per reach" is still the top unconnected signal in late 2026. Mixed Signals podcast (Dec 2025) coverage found only second-hand through search summaries (no page opened); our content-memory.md already cites exchange4media and SEJ for it; I could not re-open those here.

### Non-followers (unconnected reach)
- FACT (Mosseri, same 22.1.2025 quote): different emphasis for unconnected (sends slightly more) than connected (likes slightly more).
- FACT (Instagram Creators blog, 21.1.2025, https://creators.instagram.com/blog/the-latest-with-instagram): Instagram says ranking "historically favored creators with larger followings" and claims "creators of all sizes have an equal chance of breaking through"; reels up to 3 minutes are eligible to be seen by non-followers (US announcement; Belgium rollout not checked).
- Reading of the above (HYPOTHESIS): for a 97%-non-follower reel like ep 80, the account is being judged by strangers' reaction (skip, watch time, sends), not by followers' likes. Fits the data, not proven.

### Skip rate and watch-time definitions
- FACT (Social Samosa, 25.8.2025, https://www.socialsamosa.com/news-2/instagram-retention-chart-skip-rate-new-performance-metrics-reels-9730992): skip rate = share of views that left the reel before the first three seconds; it replaces "view rate". Retention chart = percentage of views still watching at each moment; "the flatter the line, the more engaged".
- FACT (Metricool, 4.2.2026, https://metricool.com/instagram-reel-analytics/): says there is no official Instagram source on what a "good" skip rate is. So any "good skip rate is under X%" figure is UNKNOWN.
- Average watch time: Instagram's exact formula was not found in primary text (UNKNOWN). It is presumably total watch seconds / views, which includes everyone who left at second 1.
- Our own number (content-memory.md, ep 72, 25.10.2026): skip rate 50.3%, average watch time 10 s of 36 s (about 28%), about 60% watching at 2 s, 40% at 5 s, plateau about 20%. Ep 80: 13 s average, 97% non-followers.

### Trial Reels
- FACT (Meta newsroom, 12.6.2025, https://about.fb.com/news/2025/06/inspiring-creativity-that-brings-people-together/): "We've also made trial reels available to everyone, which lets you share a reel with non-followers at first."
- FACT (Instagram Creators blog, https://creators.instagram.com/blog/instagram-trial-reels, original Dec 2024 per the Meta post https://about.fb.com/news/2024/12/trial-reels-try-content-non-followers-first-see-what-perfoms-best/): share a reel only with people who do not follow you, then share to followers if it does well.
- Eligibility conflict: a search-result summary of the Instagram Help Center page (https://help.instagram.com/1013292530224018, not readable by my fetcher, so UNVERIFIED) says public account plus 200 followers (professional) or 1,000 (personal). David's account has about 127 followers (content-memory.md 25.10). The June 2025 Meta post says "everyone". These conflict; the only real test is the app: Reel editor, Share screen, look for "Trial". Third-party blogs (Planoly, Publer, Postfaster) describe: runs 72 hours, modes Off/Manual/Auto (Auto shares to followers if it does well). Blog-grade, not primary.
- How to use for hooks (HYPOTHESIS, method only): post two cuts of the same episode with different first 3 s as trial reels, compare skip rate at 48-72 h. n is tiny (see section 3), so it only catches big differences.

### Reel length
- FACT (Socialinsider, 9,771,822 Reels, Jan-Jun 2026, published 14.7.2026, updated 20.10.2026, https://socialinsider.io/blog/instagram-reels-length/): median views by length: 1-30 s 4,700; 30-45 s 8,564; 45-60 s 10,374; 60-90 s 9,790; 90-120 s 8,000; 120-180 s 9,000; 180 s+ 4,428. Engagement rate (likes+comments / followers): 0.28% / 0.30% / 0.35% / 0.30% / 0.30% / 0.33% / 0.15%. Caveats from the page itself: no per-bracket sample sizes, no significance tests, inconsistent account-size description, mean/median unclear, accounts of 1k-100k followers only. It is correlation: short reels may be made by different account types, and "views" is the new impressions-like metric, not reach.
- FACT: that data does NOT support "shorter spreads more". Under 30 s has the lowest median views below 180 s+. It also does not prove longer is better; 45-90 s is a plateau. Our CLAUDE.md range of 45-75 s sits inside the best bracket, which supports the existing rule.
- UNKNOWN: the Buffer "1.1M-video length study" cited in CLAUDE.md. Search of buffer.com returned a 4M-post reach study (Jan 2022-Oct 2024, Reels 1.36x reach of carousels, https://buffer.com/resources/instagram-reach-engagement-analysis/) and a 12M-post engagement claim, but no length study. This matches growth-research-13-10.md ("not found"). The CLAUDE.md citation should be removed or marked unverified.
- A buffer.com page attributes to Mosseri that the algorithm "favors shorter Reels", beyond 90 s may get less distribution (https://buffer.com/resources/instagram-reels-length/; undated, no link to the statement, old; likely the 2022-23 era). FACT that Buffer says it; UNKNOWN whether Mosseri said it, and it contradicts the 2025 relative/absolute watch-time clarification. I would not rely on it.
- Untraceable (do not cite): "7-30 s best for reach" (Revid, TikTok data), "videos over 3 min not recommended to non-followers" beyond the Instagram Creators page above (that page covers eligibility up to 3 min), any "20-minute reels" claim (low-quality site).

### Posting hour
- FACT: sources disagree. Buffer evening 6-11 pm Wed/Thu, Later 12 AM (975k Reels, 2026), SocialPilot 8am-12pm Mon-Thu, Sprout no peak on Friday, per one search summary (secondary, originals not opened). That disagreement is the finding: no reliable universal best hour. Early signals (the first hours) matter for expansion per Mosseri coverage, so the hour matters mostly by when your own audience is on. For a 97%-non-follower account and a 94%-non-follower audience mix (Belgium, Israel, India, Canada, US), a single hour fits nobody. Treat as UNKNOWN for this account; an A/B on hour is too noisy at 200-800 views.

### Trending audio
- UNKNOWN. Claimed lifts (2.5x Hootsuite, 30-50% HubSpot, 40% Social Media Today) are second-hand through blogs; I could not open the originals. Kontentino attributes to Mosseri that using shared audio is not penalised (secondary). Instagram's 2023 ranking text lists "go to the audio page" as a predicted action, which only shows audio pages are a surface. No evidence this is a lever for a faceless tip reel.

## 2. Verdict table

| # | CLAIM David hears | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Instagram ranks by watch time | Mosseri 22.1.2025: watch time, likes, sends are the top three signals (SMT). Not "only" watch time. | STRONG (as one of three) |
| 2 | Shorter reels spread more | Socialinsider 9.8M Reels (2026): under 30 s median views 4,700 vs 10,374 at 45-60 s. Mosseri 2025: absolute seconds count equally, so length is not penalised. Buffer page claims "favors shorter" but is untraceable. | WEAK (against the claim as stated) |
| 3 | Most people leave early | Our ep 72: 50.3% skip rate, about 40% left by 5 s. Instagram defines skip rate as leaving before 3 s. Typical early drop is real for us; the general "most people" number has no primary source. | STRONG for our channel; UNCLEAR as a universal figure |
| 4 | Sends per reach is the key for non-followers | Mosseri 3.7.2024 and 22.1.2025: "slightly more important for unconnected". Multiplier claims (3-5x) untraceable. | STRONG that it matters; WEAK on how much |
| 5 | Skip rate in first 3 s is the top ranking signal | Skip rate is a real metric (Social Samosa 25.8.2025). No primary statement that it is ranked first. | UNCLEAR |
| 6 | A shorter reel gets a higher average watch percentage, so Instagram boosts it | Percentage is easier to get on a short reel (arithmetic), but Mosseri says both percentage and seconds count. Our ep 72 plateau shows people who pass 5 s mostly stay: the loss is the hook, not the length. | PROMISING (percent up) / WEAK (that it alone boosts reach) |
| 7 | Trial Reels let you test hooks safely | Meta 12.6.2025: available to everyone, non-followers first. Help Center threshold (200/1,000) conflicts and was unverifiable. Hook test at about 200 viewers each has about +-3.5 points of noise (content-memory 25.10), so only big gaps count. | PROMISING (availability: check app) |
| 8 | Best posting hour matters a lot | Sources contradict each other (midnight vs morning vs evening). No primary data. | WEAK |
| 9 | Trending audio boosts reach | Only second-hand blog numbers; one source says no penalty or boost proof. | WEAK / UNKNOWN |
| 10 | Over 3 minutes is not shown to non-followers | Instagram Creators 21.1.2025: up to 3 min eligible; Socialinsider median drop at 180 s+. Irrelevant to us (45-75 s). | STRONG (irrelevant) |
| 11 | Long reels (45-75 s) are safe | Socialinsider 45-60 s is the top bracket; 60-90 s next. But it is correlation across 1k-100k accounts, not causal. | PROMISING |

## 3. Recommended length for a "fix first" AI-tip reel

Range: 30-50 s, aim for about 38-45 s (HYPOTHESIS, reasoning below; not measured by us).
- The weak claim "shorter spreads" is not supported, and below 30 s the median is lowest. So do not cut to 15 s just to please the friend's idea.
- But your data shows the loss is in the first 5 s (ep 72: 60% at 2 s, 40% at 5 s, then a plateau of about 20% to the end). A 36 s reel and a 60 s reel lose the same people. What the length costs is the plateau stretch and the ending, and the setup page needs the reader to reach step 2.
- A fix-first tip with a one-screen proof, two or three steps and the link needs about 30 s of real content; padding to 60 s lowers the percent watched with no gain. Real content to about 40 s sits at the lower edge of Socialinsider's 30-45 s (8,564) to 45-60 s (10,374) brackets: take the benefit of the plateau without the padding.
- The mechanism that does matter (Mosseri): if a send is the trigger for non-followers, the reel must end on something worth sending, not just short.
- One honest test: 3-4 episodes at about 30-40 s versus 3-4 at 50-60 s, same format, compare skip rate and sends, not views. UNKNOWN until run; with views of 200-800 per reel, expect noise.

## 4. What to measure in Instagram Insights

At 48 h (Instagram widens audience slowly; ep 72 audience shifted between 4.5 h and 4 days):
1. Views, split followers / non-followers.
2. Skip rate (first 3 s). This is the hook metric.
3. Retention chart: note the second where it flattens and the percentage at 2 s, 5 s, and the end (read by eye, write it down).
4. Average watch time, and as % of reel length.
5. Sends/shares, saves, likes (per reach: divide by reach by hand, since Mosseri's signals are per reach).

At 72 h (when Trial Reels also finish, if used):
1. Same numbers again, to see if reach kept growing or went flat (ep 72: almost all views in 2-3 days).
2. Profile visits and new follows (0 so far on ep 72 and 80).
3. Audience: countries and age (to confirm who the non-followers are).
4. If used Trial Reel: result and whether Instagram's Auto/Manual share happened.

Log both in content-memory.md as FACT with hour of reading. One reel's skip rate has about +-3.5 points of noise at about 200+ viewers (content-memory.md, 25.10.2026), so compare only gaps larger than about 7 points.

## 5. CLAUDE.md length and ending rules: what should change

1. "Length: 45-75s. Do not go under 30s. Buffer's 1.1M-video study and Socialinsider's 11M-post set both put longer above shorter" -> change the citation. The Buffer length study was not found (twice now). The Socialinsider set I verified is 9.77M Reels, Jan-Jun 2026 (updated 20.10.2026), not 11M. Wording: "Socialinsider (9.8M Reels, 2026): 45-60 s has the highest median views, under 30 s the lowest; correlation, not causal." Do not cite Buffer for length.
2. The range itself: keep "do not go under 30 s"; change "45-75 s" to "about 30-60 s, pick the shortest length that holds the real content, no padding". Reason: the data shows the hook loss, not the length, is the problem; 45-75 s forces padding on a one-screen tip. Mark this as HYPOTHESIS until the 3 vs 3 test above.
3. "Ending names tomorrow's episode / follow clause at the end": the retention curve shows only about 2% watch to the very end (ep 72), so an end-only follow ask is heard by almost nobody (content-memory.md already notes moving the tease to about 15-20 s). Recommend testing the follow/tomorrow line mid-reel at the plateau; keep "The setup's in the link in bio" before the end. Mosseri 3.7.2024 says sends per reach matter, so a line that gives a reason to send to a specific person should come before the tomorrow line.
4. Add to CLAUDE.md: measure skip rate and retention at 48 h and 72 h as the hook metrics (the CLAUDE.md "measure" section currently says watch time is NOT_AVAILABLE for the account; it is visible to David in Insights, only not in the API).
5. Trial Reels: keep the line "not tested" and add "check the Share screen; the 200 follower threshold is unverified".
6. "Mosseri / 'link in bio' does not penalise reach" etc. are outside this file's scope and I did not re-verify them.

## 6. What I could not verify
- The Help Center text on Trial Reels (fetcher got an empty page).
- Mixed Signals (Dec 2025) original, and the "audition to a small sample regardless of follower count" wording (only seen second-hand).
- Any official definition of average watch time or a benchmark for skip rate.
- Buffer 1.1M length study; Hootsuite/HubSpot/Social Media Today trending-audio figures; most "best time to post" originals.
