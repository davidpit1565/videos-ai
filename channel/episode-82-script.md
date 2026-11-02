# Episode 82 script (2.11.2026, draft v1): "Did Claude get dumber on purpose?"

Structure copied from a viral reel David was sent (IG DfNHMkaE9yg, 43.7 s, ~110 words): accusation hook, three sarcastic "steps", personal beat, question to the audience. Rony's notes on it (David's friend, 2.11.2026): the visual hook is strong, the call to action is a question so people comment, drawn animations like that are made with "Claude motion". We copy the SHAPE only: no face, no meme clips (not ours), no gun image, no swear word (open decision Q8), and no claim we cannot source.

## Why the wording differs from the reel (honest, decided once)
The reel states as fact that Anthropic diluted Opus 5.5 on purpose to save compute. Nothing we found supports that. What is sourced (first party, Anthropic, "An update on Claude Code quality reports", 23.4.2026, https://www.anthropic.com/research/april-23-postmortem):
- 4 March: Claude Code default reasoning effort changed from high to medium (reverted 7 April). Affected Sonnet 4.6 and Opus 4.6.
- 26 March: a bug cleared Claude's earlier thinking on every turn of a session instead of once (fixed 10 April). Affected Sonnet 4.6 and Opus 4.6.
- 16 April: a system prompt line limiting text to 25 words between tool calls and 100 words in final answers hurt coding quality (about 3% on one eval), reverted 20 April. Affected Sonnet 4.6, Opus 4.6 and Opus 4.7.
- All three resolved by 20 April; usage limits reset for all subscribers on 23 April. The API was not affected. Anthropic wrote: "We never intentionally degrade our models."
NOT confirmed, so not said: that Opus 5.5 got worse, that anything was done on purpose, or that it saved money. The postmortem is about Opus 4.6/4.7 in Claude Code, not 5.5. Anthropic is the maker of Claude, so this episode is about the maker and the narrator-assistant is Claude: say so in the caption.

## Spoken lines (target about 30 s)
1. Some say Claude got dumb on purpose!
2. Anthropic says it never does that.
3. But it did own up to three real problems.
4. One: in Claude Code, the default thinking effort dropped from high to medium.
5. Two: a bug made Claude forget its own reasoning.
6. Three: a rule that kept replies short hurt coding quality.
7. All three were fixed by April 20.
8. Did you notice a change? Tell me below.
9. The links to Anthropic's own report are in the caption.   <- rehook (permanent test element, as in 66)

Lint (2.11.2026): script_lint flagged "People", "dumber" and "answers" (endings the voice swallows), so line 1 became "Some say Claude got dumb on purpose!" and line 6 "replies ... coding quality". The scene files were edited to match. Original reminder: "dropped" and "forget" are fine; check "effort", "problems", "quality" with `audio/script_lint.py --cues`; reword anything flagged instead of fighting the voice.

## Visuals (our own, light fixed identity, Claude orange accent)
Real Claude logo (from the product's own brand page, not redrawn). Hook: the Claude mark with a visible crack and a "?" that settles; steps as three cards with real date labels (4 Mar, 26 Mar, 16 Apr) drawn as UI, labelled "re-created". No photos, no faces, no memes. Visual change at least every 2.5 s (Alive rule).

## Experiment (log in channel/experiments.md)
Copied structure of a viral reel with an honest claim set. Prediction (a guess): reach above 66, comments from the question line, no promise it explodes. Read at 48 h and 72 h. Post at 08:00 Belgium so it is comparable.
