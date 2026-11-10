# Score calibration (David, 8.11.2026)
Every new video, hook option or review page I hand him carries three scores: HOOK, VIRALITY and OVERALL, plus a predicted VIEWS SCORE. After 48 h and 72 h the real views are converted to the same scale and written next to the prediction, so the next prediction is calibrated by the gap (up or down). The goal is 10,000 views = 100.

## The views scale (my proposal, David can change it)
Log scale, because views are multiplicative: 200 views (our median, 204) = 50, 10,000 views = 100. Formula: score = 50 + 50 * log(views/200) / log(50). Reference points: 100 views = 41; 204 = 50; 500 = 62; 817 = 68; 1,000 = 70; 1,475 = 75; 2,000 = 79; 5,000 = 91; 10,000 = 100. David's own gut rating of ep 86 (about 1,475 views) was 80, close to 75.
HOOK and VIRALITY are my judgement against the written rubric (CLAUDE.md pre-publish gate); the views score is the prediction of where the real views will land on the scale above. The three can differ: write all of them.

## Rules
1. Every review page, script file and hand-off lists: HOOK x, VIRALITY y, OVERALL z, PREDICTED VIEWS (range) and its score on the scale. Never a bare score without the reasoning in a line.
2. At 48 h and 72 h add a row below: real views, real score, gap (real minus predicted). Update this file the same day.
3. After every 3 rows, adjust: if the gap has the same sign three times, shift my scoring by the average gap and say so.
4. Honest limit: n is small; a gap is a signal to look, not a law. Reach also depends on posting hour and luck.

## Log
| Ep | Predicted (who, when) | Real views | Real score | Gap / note |
|---|---|---|---|---|
| 86 | Reviewer agents on v10 (judgements, 6-7.11): kid 88, viral critic hook 93 / virality 88, honesty 92, mean 89. Views not predicted. | about 1,475 at 12 h (24 h and 72 h reading: pending, Tue 10.11 and Wed 11.11) | 75 | Hook 93 predicted while Miki did not understand the first second (so hook was over-scored); virality 88 predicted vs views score 75: about -13. First calibration row. |
| 87 | Main session, 9.11 before posting (judgements): hook 76, virality 66, overall 70, views 250-700 (score 54-66). | pending (48 h Wed 11.11, 72 h Thu 12.11) | pending | to fill |
| 84, 85 | Not recorded as numbers before this file. | 202, 186 | 50, 48 | No prediction to compare. |

## Raised bar for the NEXT video after episode 87 (David, 9.11.2026)
OVERALL at least 90, HOOK at least 95, VIRALITY at least 95. Do not propose a concept, hook or video that scores lower: change the concept until the honest scores reach the bar, or say plainly that the honest ceiling found is lower (never inflate a score to meet the bar; the scores are judgements checked by blind readers and by real views). Episode 87 (GitHub, Ctrl+Z) is the exception: it was built before this rule, honest scores about 70 overall. If this works, the same bar applies to the video after it, and then it becomes a standing rule in CLAUDE.md. Later, when 10,000 views is reached reliably, the scale moves up (100 would then mean 20,000, then 100,000); the log formula stays and the top anchor changes.

## Added 9.11.2026 (David): VALUE is a score too
Every concept and review page now carries HOOK, VIRALITY, VALUE and OVERALL (and the predicted views score). VALUE = what the viewer gets and can use (a path, a list, a setting, a thing to check) that makes them watch to the end and leads to likes and follows; it must be as strong as virality. For the next video the bar is: HOOK at least 95, VIRALITY at least 95, VALUE at least 90, OVERALL at least 90, judged honestly (blind readers, not self-scoring). Topic constraints from David the same day: not another ChatGPT-centred video (we did too many), as few screen recordings as possible (drawn UI, real logos and our own generated pictures instead), something Claude can build alone.
Real result note: David reports that episode 86 brought exactly 1 new follower (first reading, 9.11.2026; studio snapshots show 131 followers).

### Episode 88 (9.11.2026, NOT published) — hook rounds, blind panel (Claude role-plays, judgement not measurement)
- Round 1 hook "Facebook can see photos you never posted. Find the switch." (frame 0 with timer + small panel): hook 55-62, virality 40-55. A real viewer (Roni) said "Find the switch makes no sense".
- Text-only comparison of 6 strategies: D (collage you never posted) best, hook 76-84; none >= 90.
- Round 4 hook D on the REAL rendered frame 0 (drawn card, 'drawn example' label): hook 62, virality 55-58, overall 58-60, predicted 150-300 views (score ~50). A text description scored 82; the real frame scored 62: the picture lost ~20 points ("flat clip-art, says drawn example, no real proof, not my phone"). Lesson: score the rendered frame, not the description.
- Verdict: below the 85 floor (David 9.11). Do not publish unless a real Facebook screenshot / personal proof lifts it.

### Episode 89 candidates (9.11.2026, NOT built) — blind panel on rendered frame 0 (3 Claude role-plays, judgement)
- C2 iPhone alarm turns down because it checks if you look: overall 74/79/80 (hook 78-82, virality 72-80), predicted 600-2,000. Best, but under the 85 floor; channel-fit risk (Apple attention awareness, not AI).
- C4 'SCAM OR AI?': 60/62/74. C1 'Which text is the scam?': 60/61/70. C3 '5 free Google AI tools': 46/52/57 (4 logos missing).
- Note: all readers called the bottom ~35% 'empty'; that area is the Instagram UI zone (y>1248), the card already fills the safe box. Tell readers the safe box next time.
- Verdict: nothing >= 85, so nothing built (David's rule 9.11).

### Panel validity test (9.11.2026): does a blind frame-0 panel predict real views? NO.
Method: 30 first frames (t=1.2 s, bottom 10% cropped so the handle does not leak), 24 of our episodes 57-87 (real views 95-1563) + 6 viral references David sent (views unknown), shuffled, anonymous. 3 Claude role-play readers (teen, builder, parent) scored STOP / SEND / CLEAR 0-100 each. Key: channel/calib-key-2026-11-09.json.
- Spearman correlation of panel mean vs log(views) on our 24 episodes: -0.23 (stop -0.20, send -0.21, clear -0.21). No positive signal.
- Our 4 best (ep86 1563, ep80 817, ep82 656, ep72 580): mean panel score 45.7 vs 50.0 for the other 20. The three biggest winners sat in the lower half (ep86 46, ep82 38, ep80 29).
- The 6 viral references scored LOWER than our episodes (33.3 vs 49.3).
- Raters agree with each other moderately (Spearman 0.45-0.61), so the panel is consistent but not predictive.
- Caveats: n=24, views also depend on timing/account/algorithm; the panel sees only a still frame; readers are Claude role-plays.
- Consequence: the panel can catch confusion (CLEAR) but cannot be used as a virality gate. The 85 floor on panel scores measures nothing proven. Open for David: replace the gate with real experiments (post, read 48 h) and keep the panel only for clarity.

### Episode 88 final6 vs reference realism panel (10.11.2026 ~03:40, 3 Claude role-play readers, blind X/Y boards of 4 frames each; judgement)
- Realism: ours 35-45/100, reference DeJ_gTHs-FB 80-85/100 (all three picked the reference as more real, ours as more AI/templated).
- Readability: ours 70-80, reference 55-65. Interest: ours 35-40, reference 78-85. Stop scrolling: ours maybe, reference yes.
- Subject clear in the first frame: ours yes, reference no (the reference does not state its subject; ours does).
- Motion (scene-change per second, >0.01/>0.03/>0.08): final6 7.5/3.6/1.1 vs reference 7.4/4.1/2.4.
- What gives ours away: flat crisp title strips (no ink bleed/fibre/thickness), identical tape, tiled textures, the same three photos repeated faded in the bottom half as filler, blank fake UI cards, same layout every scene. What works in the reference: halftone portraits, uneven scale and layering, real archival scans, torn cut-outs at different scales, stamps with different details.
- Against ep88-publish-criteria.md: criterion 1 (realism >= 70) FAILS, criterion 2 partly (third level 46% of reference). Not publishable by the agreed rule; next round started.

### Episode 88 final7 vs reference realism panel (10.11.2026 ~04:45; 3 Claude role-play readers; judgement)
- Realism: ours 38/55/45 (mean ~46, was ~40 for final6), reference DeJ_gTHs-FB 72/80/80. All three again chose the reference as more real.
- Subject clear in frame 1: ours YES (all three), reference NO (all three). Readability ours 74-82, reference 55-62. Interest ours 55-58, reference 68-80. Stop scrolling: ours maybe(leaning yes), reference maybe.
- Motion (>0.01/>0.03/>0.08 per s): final7 7.7/3.6/1.85 vs reference 7.4/4.1/2.4.
- Complaints: yellow strips and tape still uniform; the same scrap pile (ticket, map, stamps) unrelated to Facebook repeated; flat UI card; cake/dog photos look filtered/stock; cork background never changes; no real shadows or curl.
- Against ep88-publish-criteria.md: criterion 1 (realism >= 70) FAILS (46 vs 70). Round 7 moved realism only ~6 points for a very large effort: code-composited collage is likely capped around 50. NOT published. Options for David: real filmed material, or accept the cut knowingly.
