# Episode 88 hook lab (9.11.2026): strategies, not rewordings

All scores below are my judgements against the rubric, not measurements, and no blind panel has run on these (this session has no way to run one): the 90+ goal is untested.
Facts used (only these, from `episode-88-plan.md`): feature "Camera roll sharing suggestions"; Meta: suggests photos from your camera roll and makes collages and edits, "analyses media in your camera roll"; opt-in ("you must opt in", can turn off any time); EU and UK; Meta says no AI-training and no ad-targeting use; default state UNCONFIRMED; upload UNCONFIRMED for EU/UK (US 2025 test uploaded, a different rollout); exact EU pop-up wording UNCONFIRMED (so every drawn pop-up is labelled "drawn example"); path Settings & Privacy > Settings > Camera roll sharing suggestions (Which?, menu names move).
Rejected hook: "Facebook can see photos you never posted. Find the switch." (blind reader 72 / 60; Roni: "which switch, what exactly?").

## 1. Diagnosis: why the hook fails (looking at `episode-88-frame0.png`)
The viewer, in the first second, cannot answer any of the four questions:
1. **Which switch?** "The switch" is a definite noun with no referent. Nothing said or shown names it. On the frame it is a small grey toggle with a "?" at the bottom right of a card, about 170 px wide, with two grey placeholder bars next to it. The one thing the viewer is told to find is the one thing the frame hides. (Compare @good.ball21's post in `research-2026-11-08-reels.md`: "find the tell" works because the answer is in the picture, circled. Ours is a quiz with no answer on screen.)
2. **Who does what?** "Facebook can see photos" is a capability with no actor and no act. See how? Since when? Did I allow it? It reads like a leak, but the truth is opt-in (you tap Allow). The hook promises a scandal the facts do not support, and the facts are what the video later has to say ("Meta says it's opt-in"): the payoff contradicts the hook's tone. That is also why it feels half-true to Roni.
3. **Why me?** Nothing separates "this happens to everyone" from "this happens to people who tapped Allow". The viewer who never opted in has no reason to care and no way to know whether they did. There is no recognisable moment (a pop-up they saw, a collage they got).
4. **What do I do now?** "Find the switch. Five seconds. Go." asks for an action inside the app, but the viewer does not know which app screen, and cannot start a 5-second search with no path. The countdown (0:05) then competes with the headline and turns understanding into a game before the subject is understood.
5. **Frame 0 itself.** Four text layers (headline, green "Find the switch" bar, countdown, panel title "YOUR CAMERA ROLL") plus three "NEVER POSTED" tags, all in an equal visual weight: nothing is the one thing to look at. The photos are cartoon blobs, not recognisable personal photos, so "never posted" tags label nothing felt. Facebook logo is small (about 190 px) at top left. The panel is only about 490 px tall (y 760-1255) and the headline block above it is crammed; the 5-second countdown is the biggest number on screen and is not the subject. The Facebook "f" is there (rule satisfied) but the subject is "a setting", and no setting is shown.
6. **Compared with the references.** @ekkobuild: topic said in sentence one and one saveable object. @david_knowsai: visible result in the first 6 s. @good.ball21: one image, one task, answer already inside the image. Ours: a task without its object. Ep 86 (a felt stake, hidden subject) and ours (a subject, a mild stake, hidden object) fail from opposite sides: the target is subject + felt question + the object to act on, all in frame 0.

Rule derived: a hook may ask the viewer to DO or ANSWER only if the thing to answer about is visible in frame 0 and named in the spoken line. And the claim must be conditional-true ("if you tapped Allow"), not an alarm.

## 2. Six strategies

Frame size rule for all: the main object is enlarged to fill x 65-1015, y 269-1248 (about 950 x 980). Real Facebook "f" logo (2023 icon, Commons, `video/ep88/hf/assets/facebook.svg`), icon alone, no caption. Drawn UI says "drawn example". Light page, lime accent.

### A. Check-your-own-phone, with the setting on screen
- First line: "Facebook can look through your camera roll. Is yours on?" (11 words)
- Frame 0: one giant drawn Facebook settings row filling the box, ~3 rows tall: line 1 in huge bold "Camera roll sharing suggestions" (the verified label), under it "Get camera roll suggestions when you're browsing Facebook" and a large toggle, half-way mid-flip between grey and lime so it is visibly a switch with two states; Facebook logo top-left, large (about 260 px). No countdown, no tags. Label "drawn example".
- Viewer must DO/ANSWER in 5 s: open Facebook, find that exact row, answer on/off. The name they will search for is read to them.
- Felt stake: "yours" plus a setting about their own phone's photos; the ON/OFF state is a binary they are personally either in or out of.
- Risk: "Is yours on?" assumes the viewer may have it on; default state UNCONFIRMED, so the video must not say it was switched on for them (it says "if you said yes"). Many Belgian viewers will find it missing (feature rollout) or off: the payoff must treat "it is off or missing" as a good answer, or the hook becomes a dud. Setting-name-first can read as a tutorial (lower pull).

### B. Pop-up recognition
- First line: "Facebook asked to look through your camera roll. Did you tap Allow?" (12 words)
- Frame 0: a giant drawn phone pop-up filling the box: Facebook logo large at the top of the pop-up, title "Camera roll sharing suggestions" (feature name only; no invented body text), two big buttons "Allow" (lime, with a drawn thumb about to tap it) and "Not now"; behind it the dimmed drawn photo grid. Label "drawn example, wording differs". Nothing else on screen.
- Viewer must answer: "yes / no / I tap Allow on everything and don't remember". That is a memory question about their own behaviour in 2 s.
- Felt stake: the exact moment of a tap they may have made without reading (the same reflex everyone has with pop-ups), so the stake is "I may have said yes".
- Risk: "asked" assumes a pop-up exists in the EU/UK flow; Meta says "opt in" and the exact prompt is UNCONFIRMED (the 2025 US test did show a pop-up). Mitigate: say "asked" only if line verified; otherwise use "can ask". Viewers who never saw one answer "no" and scroll: video must say in line 2 that not having seen it is also fine, and show how to be sure.

### C. Named person: mum's message
- First line: "Mum texts: Facebook wants my photos. Should I tap Allow?" (10 words)
- Frame 0: giant drawn chat screen filling the box: a grey incoming bubble from "Mum" with that sentence, below it a typing indicator and a lime "Reply" cursor; above, the small drawn Facebook pop-up thumbnail with the Facebook logo as her screenshot (label "example message"). Facebook logo large.
- Viewer must answer: "what do I tell my mum?" in 3 s.
- Felt stake: a specific person they love, a direct question addressed to them, and it makes the final "send it to mum" literally the answer to the hook.
- Risk: it is a staged message (label "example message", never claim it is real; never imply a real mum). "wants my photos" slightly overstates (Meta: looks through for suggestions, opt-in): use "wants to look at my photos". Hook's subject is a story, not the topic, so the Facebook logo plus pop-up thumbnail must carry the subject. Weaker for viewers who do not message their mum about apps.

### D. A concrete consequence they can see: the collage
- First line: "Facebook made you a collage from photos you never posted. Seen it?" (12 words)
- Frame 0: a giant drawn Facebook feed card filling the box: lime banner "Collage made for you" (drawn; the feature's real function is collages and edits, the on-screen wording is ours and labelled "drawn example"), four photo tiles arranged as a collage, buttons "Share" and "Not now"; Facebook logo large above.
- Viewer must answer: "did I ever see this in my feed?" in 3 s.
- Felt stake: recognition of a real symptom, "the app knew about a photo I never uploaded", which is the creepy moment; no need to explain the system first.
- Risk: only people who opted in can have seen it, and the rollout in the EU/UK is recent (16.4.2026), so most viewers will answer "no". The real in-app suggestion wording is UNCONFIRMED. The claim "made you a collage" must stay conditional ("if you opted in"). It scores best on "felt" only for the few who saw it.

### E. Path as a promise
- First line: "Four taps and Facebook stops looking through your camera roll." (10 words)
- Frame 0: a giant drawn saveable card filling the box: four numbered rows in huge type ("1 Profile picture", "2 Settings & Privacy", "3 Settings", "4 Camera roll sharing suggestions") and a switch on row 4 already flipped to lime OFF; Facebook logo large top-left. Looks like a screenshot to keep.
- Viewer must DO: screenshot, or follow the four rows now.
- Felt stake: low; it sells control, not a problem. Works as the save trigger.
- Risk: no personal stake or curiosity gap (the answer is in the frame, nothing left for the video to close), "stops" implies it was on (UNCONFIRMED), "four taps" depends on the app menu version (Which? path, "menu names can differ"), and instruction hooks are the type the data shows flat. Best as the first frame of the VALUE scene, not as the hook.

### F. Meta's own words (inventive: the claim is not ours, it is checkable in 30 s)
- First line: "Facebook's own announcement says it analyses your camera roll." (9 words)
- Frame 0: one giant quote card filling the box in huge type: "analyses media in your camera roll" with a lime highlight on "your camera roll", small label "Meta, 16.4.2026" (a source note is allowed, the logo itself stays caption-free), Facebook logo large. The quote is verbatim from Meta's newsroom post.
- Viewer must: "wait, is that real? it says what, exactly?" (curiosity, checkable claim, concept checklist item 6).
- Felt stake: medium: "your camera roll" in Facebook's own mouth. It does not say whose camera roll or whether I chose it.
- Risk: the opt-in half is withheld from the hook; a viewer who reads the full Meta post finds "you must opt in", so line 2 must say it at once ("only if you say yes") to avoid a misleading hook. Quote cards are a static picture: needs motion (the highlight sliding, the quote typing at a natural varying pace) to satisfy "alive".

## 3. Honest scoring of the strategies (judgements, not measurements)
| | Subject in 1 s | Felt in 3 s | Object visible | Predicted HOOK | Note |
|---|---|---|---|---|---|
| A check phone | yes | medium | yes | 80 | strong action, mild stake |
| B pop-up recognition | yes | high (own tap) | yes | 84 | needs EU prompt confirmed |
| C mum's message | partly | high (named person) | partly | 78 | staged, subject via logo |
| D collage | yes | high for the few who saw it | yes | 74 | few viewers have seen it |
| E four taps | yes | low | yes | 70 | a save card, not a hook |
| F Meta's words | yes | medium | yes | 74 | checkable but impersonal |

## 4. Top two, and what the script must change
**Honest limit first:** the topic itself probably cannot reach a blind-panel HOOK of 90+, let alone the 95/95 bar. The stake is real but mild (opt-in, Meta says no AI or ad use, most Belgian viewers will not have the feature), and the first-line promise must stay conditional. My honest ceiling on this topic is about 84-86 (B or A+B merged); a 90+ would need a verified unconditional fact (for example proof the pop-up appears by default in Belgium, or an on-by-default setting), which we do not have. If David wants 90+, the right move is a different topic, not a better hook on this one. I will not mark a hook 90 to meet the bar.

### Pick 1: B (pop-up recognition), with A's object-on-screen as the second beat
Why: it puts the feature in one recognisable moment (the Allow tap) the viewer can answer yes or no, the subject is in the first words and on the frame, it is conditional-true (Meta: opt-in means a tap), and it needs no search to act. It fixes diagnosis points 1 to 4 at once.
Script changes (`episode-88-script.md` lines):
- L1 becomes "Facebook asked to look through your camera roll. Did you tap Allow?" Verify first that "asked" is true for the EU/UK flow; if not, "Facebook can ask to look through your camera roll. Did you tap Allow?".
- L2 "Five seconds. Go." and the countdown are dropped. New L2: "Not sure? Check now. It takes ten seconds." (action stated, no game).
- L3 "It's called camera roll sharing suggestions." stays, but the pop-up title is already on frame 0, so it is a callback, shown on the settings row.
- L4 "If you tap Allow, Facebook looks through your gallery and suggests collages." stays (now the explanation of the tap in L1). Swap "gallery" for "camera roll".
- L5 "Meta says it's opt-in and not used for ads." stays, and also add "or to train its AI" only if worded exactly as the Meta line (verified), otherwise leave out.
- L6 path stays; the VALUE card is shown from the first reveal; add the line "If it's missing, you're fine."
- L7 "Send this to mum. She taps Allow every time." now pays off the hook's "Did you tap Allow?" directly. Keep.
- Frame 0 rebuilt per strategy B; remove countdown, "Find the switch" bar, and "NEVER POSTED" tags. Last second returns to the pop-up with "Not now" tapped, for the loop.

### Pick 2: A (check the setting, object on screen), as the safer version if the EU prompt wording stays unconfirmed
Why: it does not depend on a pop-up that may not exist in Belgium, it shows the one real, verified label, and it keeps the game energy David liked ("find it") but with the object visible.
Script changes:
- L1 "Facebook can look through your camera roll. Is yours on?" (replace "Find the switch"). 
- L2 "Look for this row." (while the huge row is on screen, the toggle flips once) in place of "Five seconds. Go."
- L3 "Camera roll sharing suggestions." shortened to the name only, since it already sits on frame 0.
- L4 and L5 unchanged in meaning; add "It's off unless you said yes" only if the default state is confirmed (it is NOT confirmed: use "Meta says you have to opt in").
- L6 path stays; end with the toggle flipping to OFF.
- L7 unchanged.
- Payoff rule: the video must treat "it's off or missing" as a good result in L6; otherwise most viewers find nothing and feel the hook lied.

### Both picks: checks before building
1. Run the blind reader (first frame + first second, two questions) on the new frame 0: no panel has seen these.
2. Verify the EU/UK pop-up exists and its wording (UNCONFIRMED); keep "drawn example" on screen until verified.
3. Do not say photos are uploaded, that it is on by default, or that anyone was switched on without asking.
4. Scores for the final video go in `score-calibration.md` as HOOK/VIRALITY/VALUE/OVERALL plus predicted views, with the ceiling note above.
