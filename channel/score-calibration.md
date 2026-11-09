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
