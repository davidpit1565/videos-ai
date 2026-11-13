# Pelican riding a bicycle: research for a four-Claude-models reel (13.11.2026)

Brief (David): "Draw a pelican riding a bicycle: same prompt, four Claude models (Haiku 5.5, Sonnet 5.5, Opus, Fable 5.2), the difference is visible". Read live on 13.11.2026 with WebSearch/WebFetch/yt-dlp. Instagram not scraped. YouTube rate-limited yt-dlp (HTTP 429) after the first listing, so per-video follower counts, upload dates and likes are NOT AVAILABLE; view counts are the numbers yt-dlp's search listing showed on 13.11.2026. Nothing downloaded.

## Duplicate check
`grep -i "pelican|bicycle|draw" channel/topics-covered.txt`: one hit, line 58 ("WhatsApp can already redraw your photo with AI"), unrelated. `content-memory.md`: no pelican/bicycle hit. Not a duplicate. Also not the "odd chat test" class: the drawing is the content.

## 1. Facts about the benchmark
- Started by Simon Willison, blog post 25 Oct 2024 (`https://simonwillison.net/2024/Oct/25/pelicans-on-a-bicycle`). Exact quotes as fetched: "I decided to roll out my own LLM benchmark"; "I chose that because a) I like pelicans and b)"; "I'm pretty sure there aren't any pelican on a bicycle SVG files floating around (yet)"; "that might have already been sucked into the training data." Prompt: "Generate an SVG of a pelican riding a bicycle." (prompt wording from a search summary, not a verbatim fetch).
- It started as a joke, by his own words as relayed in a search summary: "I started my benchmark as a joke, but it's actually starting to become a bit useful" (not re-verified on his page).
- Why people use it: AI Engineer talk page (`https://www.ai.engineer/talks/YpY83-kA7Bo-llm-pelican-benchmark`): he found "conventional benchmark numbers and leaderboards increasingly unsatisfying"; a "deliberately personal, interpretable test"; it "does not pretend to measure every capability". So do NOT claim in the reel that the pelican score ranks the models' intelligence.
- Is it a known thing people already watch: YES, in the AI-tech crowd. The talk video "2025 in LLMs so far, illustrated by Pelicans on Bicycles" has 160,958 views (AI Engineer channel, yt-dlp listing 13.11.2026, `https://www.youtube.com/watch?v=YpY83-kA7Bo`). Gigazine covered it (`https://gigazine.net/gsc_news/en/20241219-pelicans-on-a-bicycle`, `.../20260521-llms-pelicans-on-bicycles-2026/`). A July 2026 write-up "Are AI labs pelicanmaxxing?" (`https://dylancastillo.co/posts/pelicanmaxxing.html`) generated 1,008 SVGs with seven models and, per a summary, found little evidence labs optimise for it. A fan site exists (`https://scosman.github.io/pelicans_riding_bicycles/`). Not known to the general public: the audience is developers and AI followers.
- Willison's own results are on his blog tag page (`https://simonwillison.net/tags/pelican-riding-a-bicycle/`) and as GitHub gists (simonw). Gigazine said Claude Sonnet 4.5 and GPT-5.1 distorted the pelican/bike relationship while Gemini 3 drew it more naturally (search summary, old models).

## Model names (verified by search 13.11.2026, one summarising source chain, re-check before scripting)
- Opus 5.5: released 22.9.2026. Sonnet 5.5: 28.9.2026. Haiku 5.5: 7.10.2026 per DeepLearning.AI and 9to5Mac (`https://www.deeplearning.ai/the-batch/claude-fills-out-its-model-family/`); some pages still call it leaked/announced, so confirm it is selectable in the app. Fable 5.2 and Mythos 5.2: 9.11.2026 (`https://letsdatascience.com/news/anthropic-releases-claude-fable-52-and-mythos-52-models-66044607`), "a step above Claude Opus 5.5" is Anthropic's claim. Plan access (free vs paid) per model: UNCONFIRMED, check before filming.
- Keep "Opus" as "Opus 5.5" on screen once verified.

## 2. Short-video examples (as shown; followers NOT AVAILABLE unless stated)
| Handle/channel | Title | Views as shown | Link | Note |
|---|---|---|---|---|
| Dom the AI Tutor (YouTube) | "Claude Fable 5.2 Coded These Animations (vs Astra, Gemini & Opus 5.5)" | 25,202, length 489 s (long, not a Short) | `https://www.youtube.com/watch?v=GGWyDIrNSD8` | Not confirmed to be a pelican; animations test. Page could not be opened (Google block) |
| CodeWithRameshAI (YouTube) | "4 AI Models Animate a Pelican 🚲🔥 Gemini vs Claude vs GPT!" | 35, 30 s | `https://www.youtube.com/watch?v=k_tOSQEturQ` | closest to our idea, tiny |
| Tao An (YouTube) | "A Pelican Riding a Bicycle, from SVG Doodle to 3D: One Blender Script by Claude Fable 5.2" | 30, 25 s | `https://www.youtube.com/watch?v=u7S2AVNnb-A` | |
| Maker Jackie (YouTube) | "Claude Opus 5.5 vs GPT-6 Astra: same prompt, a 3D pelican riding a bike (three.js, code only)" | 436 | `https://www.youtube.com/watch?v=tNPGT3SOwfk` | |
| Nodera (YouTube) | "Crazy Pelicans! I Tested 21 AI Models With the Same Prompt — 66 Pelican Bicycle Animations Compared!" | 51 | `https://www.youtube.com/watch?v=mmClWzFsUI4` | |
| Jason Higley (YouTube) | "Pelican Riding a Bicycle Animated SVG by Qwen 3.8-27b" | 121, 59 s | `https://www.youtube.com/watch?v=jtnFKttvRQk` | |
| Unknown channel (YouTube Shorts) | "Is "Pelicanmaxxing" real? The weirdest AI benchmark explained" | NOT AVAILABLE (page blocked) | `https://www.youtube.com/shorts/NdgHvFMF07k` | seen only in search results |
| Unknown channel (YouTube Shorts) | "AI Generates a Pelican on a Bike?! Simon Willison's Test! #shorts" | NOT AVAILABLE | `https://www.youtube.com/shorts/VDC4_1sfYlk` | seen only in search results |

TikTok and Instagram: I found NO TikTok or Reels pelican comparison. One TikTok search hit (`@techfren/video/7492072132424387848`) was opened with yt-dlp and is an unrelated code-review video; the search summary about it was wrong, ignore it. Instagram NOT AVAILABLE (cannot be scraped).

Honest reading: FACT, I could not find a pelican-comparison short that went big; the visible ones sit at 30 to 436 views. The benchmark is famous inside developer circles (160K-view talk) but I found no proof it travels as a short on TikTok/Reels. The broader "same prompt, several AIs" format does have proven big numbers (see `new-formats-2026-11-13.md`: 14M and 303K), but those are visual animations, not pelicans. So the pelican is a hypothesis about a niche in-joke, not an evidenced hit.

## 3. Hooks and titles used
Pattern in titles: "<N> AI models ... same prompt", "X vs Y vs Z", "Who wins", "Is it real?", emoji and "#shorts". Hooks seen: the model-comparison title as the hook ("4 AI Models Animate a Pelican"), a mystery frame ("weirdest AI benchmark"), a named-authority frame ("Simon Willison's Test"). Spoken openings: NOT AVAILABLE (videos not watched).

## 4. What would make OUR version more shareable (hypotheses, not facts)
Constraint check: faceless, calm voice, 15 to 25 s, plain present-tense English, no spoken THR/TR clusters (avoid: three, try, tree, trust, through, Anthropic, travel, "true"). Use: "four", "same words", "draw", "bike", "bird", "worst", "best", "last", "Fable" (R before a vowel-less cluster is not an issue here).
- Subject in the first second, visually: first frame = four drawing boxes in a 2x2 with the real Claude logo and the four names, each box already starting to draw, with "Draw a pelican on a bike" as the only text (under 3 lines). A stranger gets it without knowing the benchmark. Explain the pelican in plain words in the same breath ("a bird on a bike, drawn in code").
- Reveal order: show the smallest model first and the biggest last, but the visible rank is the payoff: Haiku, Sonnet, Opus, then Fable. If the real results do not show a clear step up, the hook is the surprise instead ("the cheap one wins") and we say it. Never pre-decide: one run per model, no silent retries; if retried, show it. Prompt text on screen so a viewer can paste it (30-second check).
- Ranking card at the end (worth saving, screenshot-able): 1 to 4 with each model name and what was visibly wrong or right ("wheels", "bird on the seat", "feet on the pedals" as real observations, not invented).
- Named person: "Send it to the friend who says AI is all the same." Spoken, plain.
- Last-second payoff and loop: final frame shows the ranking, the last spoken word is the winner's name, then a cut back to the first frame (four empty boxes) so the loop re-draws. A detail easy to miss: a small wheel or beak detail that differs, shown by a ring in the second watch.
- Series wrapper: "Same prompt, four models #1" (a numbered format per CLAUDE.md "Think in formats"); next slot: a different drawing (a dog riding a skateboard) so the pelican in-joke is not required. Tomorrow-line at the end per the closing rule.
- Risks: pelican benchmark audience = developers; for everyone else it is just a funny bird, which suits us. The claim "difference is visible" is only honest if the real outputs differ: render all four first, decide the hook after. Do not say it measures intelligence (Willison himself says it does not).
- Honest score: concept virality about 55 to 65, ASSUMPTION, a judgement, not a measurement. Predicted views 300 to 1,500, ASSUMPTION, based on the 30 to 436 view comparables and our median; no evidence it breaks out. If Fable 5.2's pelican is clearly the best, the ranking becomes the sendable bit.
- Cost/effort: four free or low plan runs, four screen recordings, 2x2 grid, real logos. Needs the user to confirm Haiku 5.5 and Fable 5.2 are available on his plan.

## Unconfirmed
Per-video follower counts and dates; any TikTok/Reels pelican reel; Haiku 5.5 official launch page; plan access to Fable 5.2; whether Willison has published a Fable 5.2 or Opus 5.5 pelican (a search summary names Opus in Feb 2026 as "Poor" on a third-party timeline, `https://select.keenable.ai/r/the-pelican-on-a-bicycle-model-timeline/t60MmAZHsfyZXd1m4oACVw`, a low-trust aggregator).
