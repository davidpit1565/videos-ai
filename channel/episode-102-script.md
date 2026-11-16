Publish mode: ASK DAVID (TRIAL or REGULAR; default REGULAR if he does not say)

# Episode 102 script: FREE TWINS #1, six free alternatives to apps you pay for (built 16.11.2026)

Status: BUILT, not published, not merged. Plan and verification table: `channel/episode-102-plan.md`. Build: `video/ep102/` (build102.py, mix102.py, voice/, hf/). Funnel: TOP. Format: numbered series candidate "Free twins #1". Experiment: a list format, new for us (log in `channel/experiments.md` when it is published).

## TOPIC verdict (first, per the topic rule)
Why a stranger cares today: money that leaves their account every month for apps they know by name (Loom, Notion, Calendly, ElevenLabs), and a free twin for each. Proof: public pricing pages and public GitHub pages, all read on 16.11.2026. Weak side: only part of it is an AI story (VoiceStudio, OpenWhispr, AppFlowy's AI), many viewers cannot host a server, and none of our three canon winners is a list. Compared with the queue (`channel/queued-ideas.md`): the only queued idea with outside proof of engagement (reference reel: 1,414 likes, 609 comments, views not shown) and a saveable payoff. It is an experiment of a new format, not an extension of a proven one.

## Scores (judgement labels, not measurements; our scores have not predicted views so far)
HOOK 72, VIRALITY 70, OVERALL 70, PREDICTED VIEWS about 500 (range 250-1,200). Log real 48 h / 72 h views in `channel/score-calibration.md`.

## Spoken lines (`video/ep102/voice/lines.txt`, 15 lines)
1. Loom, Notion, Calendly. Free twins exist!
2. Six apps, seventy-five bucks a month. Watch it hit zero!
3. Loom makes screen videos. Cap does it free.
4. Notion? AppFlowy. Notes, docs, even AI.
5. Calendly? Cal D I Y, for personal use only.
6. Intercom bills per seat, and per AI reply.
7. Chatwoot is free if you host it.
8. Wispr Flow? OpenWhispr. You talk, it types.
9. And the big one, ElevenLabs.
10. VoiceStudio clones your own voice, on your own machine.
11. It's new, just seven months old.
12. We did not test these, so check each one yourself.
13. Save the list. Send it to a friend who pays for Loom.
14. The setup's in the link in bio. (locked canonical clip)
15. Want the next one? Follow, and you'll see it.

Wording rules kept: "free twin" / "free alternative", never "replaces"; Cal.diy "personal use only" is spoken and stamped; VoiceStudio "seven months old" is spoken and stamped; "We did not test these" is spoken and on the end card; no promised next episode. Hook type: named products + surprise statement (not a question).
`python3 audio/script_lint.py --file video/ep102/voice/lines.txt`: 3 notes left on purpose: "Calendly" twice (a brand name, shown on screen with its logo) and "month" (the lint's own suggestion is "a month", which is what the line says). Swapped after the first lint run: dollars to bucks, records to makes, answer to reply, computer to machine, first to yourself, whoever to a friend who.

## Numbers on screen (all read 16.11.2026; full list with sources is written by the build into `video/ep102/cues102.json`)
- Prices (cheapest paid plan on each official pricing page): Loom $18, Notion $10, Calendly $10 (yearly billing), Intercom $19 per seat (yearly new-customer rate; $29 otherwise) + $0.99 per AI answer, Wispr Flow $12 (yearly billing; $15 monthly), ElevenLabs $6. Sum $75, tagged "from: cheapest paid plan, per person, Nov 2026".
- Stars, rounded DOWN: Cap 25K+ (25,113), AppFlowy 78K+ (78,984), Cal.diy 50K+ (50,090), Chatwoot 39K+ (39,919), OpenWhispr 11K+ (11,623), VoiceStudio 111K+ (111,733). Method: the GitHub repo pages through Exa's page fetch (github.com and api.github.com answer 403 from this container). AppFlowy, Chatwoot and OpenWhispr returned exactly the same count as in the plan's earlier read the same day, so those three may be a cached snapshot; rounding down covers it. UNCONFIRMED: last commit dates; VoiceStudio's star history (111K in 7 months is unusual).

## BUILD-UP beat list (what is NEW per beat; times are in `cues102.json` under `buildup`)
Open question after the hook: does the total really reach zero, and what is "the big one"?
| Beat | Line | Picture | What is new |
|---|---|---|---|
| 1 | 1 | Receipt: Loom, Notion, Calendly logos, "$75 A MONTH", FREE TWINS stamp | the stake: money + named apps |
| 2 | 2 | The receipt lists six apps with prices, total $75 flashes red | the promise: it goes to zero |
| 3 | 3 | Loom $18 struck out, Cap card, real screenshot, total 75 to 57 | first proof |
| 4 | 4 | Notion to AppFlowy, real screenshot, total 47 | AI enters |
| 5 | 5 | Calendly to Cal.diy, PERSONAL USE ONLY stamp, total 37 | a limit, said out loud |
| 6 | 6 | Intercom: "$19 PER SEAT", "+$0.99 PER AI ANSWER" | reversal: you pay per answer |
| 7 | 7 | Chatwoot card, FREE IF YOU HOST IT, total 18 | the condition |
| 8 | 8 | Wispr Flow to OpenWhispr, voice wave turns into typed words, total 6 | a felt demo (illustration, tagged) |
| 9 | 9 | THE BIG ONE + the ElevenLabs logo | the withheld item |
| 10 | 10 | VoiceStudio card, real screenshot, total hits $0 (green) | the payoff |
| 11 | 11 | NEW: 7 MONTHS OLD stamp | a caution on the biggest claim |
| 12 | 12 | New scene: the saveable card, six rows; "NOT TESTED BY US" | the honest limit + the thing to save |
| 13 | 13 | The rows nudge one by one | save + a named person to send it to |
| 14-15 | 14, 15 | SETUP: LINK IN BIO, then the FOLLOW card | CTA |
Check: (1) the total visibly gets closer to zero on every pair; (2) each pair adds a new kind of fact (screenshot, AI, a limit, a hidden fee, a demo, the biggest name); (3) reasons to stay at about 8-10 s (AI + the falling total) and at two thirds (hidden fee, then the big one); (4) no beat only repeats the picture; (5) the reveal ($0, the sixth app) is held until line 10; (6) weakest beat by my own reading: beat 5 (Cal.diy: a caveat, least exciting).

## Blind-reader test, frame 0
See the section at the end of this file (added when it ran).
