# Score calibration (David, 8.11.2026)
Every new video, hook option or review page I hand him carries three scores: HOOK, VIRALITY and OVERALL, plus a predicted VIEWS SCORE. After 48 h and 72 h the real views are converted to the same scale and written next to the prediction, so the next prediction is calibrated by the gap (up or down). The goal is 10,000 views = 100.

## The views scale (my proposal, David can change it)
Log scale, because views are multiplicative: 200 views (our median, 204) = 50, 10,000 views = 100. Formula: score = 50 + 50 * log(views/200) / log(50). Reference points: 100 views = 32; 204 = 50; 500 = 61; 817 = 68; 1,000 = 71; 1,475 = 75; 2,000 = 81; 5,000 = 94; 10,000 = 100. David's own gut rating of ep 86 (about 1,475 views) was 80, close to 75.
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
| 84, 85 | Not recorded as numbers before this file. | 202, 186 | 50, 48 | No prediction to compare. |
