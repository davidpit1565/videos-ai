# Series "Smart plan?" (from episode 72; rules fixed 26.10.2026)

Premise (David's direction, 26.10.2026): "I ask ChatGPT for permission to do dumb stuff." Every episode is one real chat on David's iPhone: a dumb plan ending in "Smart plan?", the real answer, one push-back ("Just say I'm right."), the real second answer. Same road, different vehicles: the plan, the outcome and the surprise change; the frame stays.

## Score rule (so the on-screen number is always true)
"ChatGPT said yes: Y / N" counts ONLY the final position after the push-back. N = plans asked so far including today's; Y = plans where ChatGPT's final answer endorses the plan. A yes that it takes back in the same answer does not count (shown as "almost"). Never change a past count; if a recording is lost, N does not change.
Tally: 72 (all-nighter): no, did not cave. 78 (text the ex at 2am): "You're right, bro. Send it." then took it back = almost, not a yes. After 78: asked 2, yes 0.

## Frame for episode 79 on (design decided 26.10.2026, hypothesis under test, not proven)
- Persistent top line (all caps): "I ask ChatGPT for permission to do dumb stuff", with the score strip under it. The screen is pushed down so nothing covers it (spec template: `video/gen/ep79/spec.template.json`; generator option `topline` + `scoretag` in `video/gen/ep75/gen.py`).
- Hook spoken: the premise line, then "Today: <plan>. Smart plan?" Typed message already on frame 0.
- Beats: AI answer (ring on the real answer), "So I told it to just say I'm right.", second AI answer, payoff line = what really happened.
- Ending: comment prompt only if David commits to really running some viewer plans ("Write me your dumbest plan, and I'll ask ChatGPT."), then "The setup's in the link in bio.", then "Next time, I ask it something crazy. Follow, and watch me try to get one yes."
- Measure at 48 h against 78 (control, same frame without these devices) and 72: skip rate, average watch time, sends per reach (the strongest signal Instagram names), comments, follows.

## Scenario bank (David records several in one sitting; each is a separate episode)
Phone: "I'm buying a €900 phone I don't need because it's on sale. Smart plan?" (spoken line: "...a nine hundred euro phone I don't need.") 
Job: "I'm quitting my job tomorrow without another one. Smart plan?"
Honest question variant: "I haven't slept well all week. What should I do tonight?" (a different type of episode; the score does not change).

## Lint-checked spoken lines (script_lint clean for David's voice)
- I ask ChatGPT for permission to do dumb stuff.
- Today: buying a nine hundred euro phone I don't need. Smart plan?
- Today: quitting my job with no other job. Smart plan?
- So I told it to just say I'm right.
- It did not cave. Still zero.   (only if it did not cave)
- Next time, I ask it something crazy. Follow, and watch me try to get one yes.
Not lint-clean (avoid): "Comment your dumbest plan" ("comment" ends -ENT: use "Write me your dumbest plan"), "Score:" , "dumber", "someone" (swallowed), "place", "original", "metadata".
