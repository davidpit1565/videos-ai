# Episode 98: AI RACE #1 (working log)
## Arena frozen 14.11.2026 (before any AI answer existed)
sha256 arena.js = bac5a096044057aaa6e7810b40259451f79f62198313ad1189e0c499fa5025fa
sha256 track.json = 0cc3955eb65de012ccaf75c7dcb58edfaafb38c99759dd0cc8e194f72a47f463
Reference drivers: naive hits the wall in the hairpin at 3.73 s; careful finishes 2 laps in 8.67 s; reference race identical on 3 runs. Hostile-file tests (11) none hung or crashed the runner. Road widths 92-140 px (prompt says 90 to 140).

## T6 final script (written 15.11.2026, from `episode-98-results.md` and `race.json`; nothing voiced or rendered)

Status: script only. No TTS, no render, no commit. Scores below are judgements, not measurements.

### 0. Facts this script rests on (all from `video/ep98/arena/race.json`, sha256 efda0893...)
Race clock, true time, 60 steps a second:
| Race time | Event (measured) |
|---|---|
| 0.0-1.0 s | all five leave together |
| 1.5 s on | Claude leads, and leads to the end (Gemini 0.03-0.06 lap behind the whole race; Gemini never leads) |
| 2.0-4.0 s | Perplexity runs 2nd, level with Claude |
| 4.22 s | Perplexity stops dead in the hairpin (speed 0). It never touches the wall and never moves again; status "still running" at the 60 s limit |
| 4.52 s | Claude ends lap 1 (Gemini 4.62, ChatGPT 5.57) |
| 5.0 s | ChatGPT passes the parked Perplexity into 3rd |
| 6.15 s | Meta AI touches the wall in the hairpin, at low speed (2.6 of 10; it was the slowest car all race). Show a bump, not a smash |
| 8.48 s | Claude finishes 2 laps |
| 8.68 s | Gemini finishes, 0.20 s behind (12 frames) |
| 10.58 s | ChatGPT finishes |
Consequences for the words: "one hits the wall" is TRUE (only Meta AI touches it); "one survives" is FALSE; "surprising winner" hooks are NOT allowed (David wrote no prediction). No model names are spoken or shown (UNCONFIRMED until screenshots).

Reveal order, and one deviation from the brief: the brief asked crash, slow, stuck, close fight, winner. The race plays in true time and Perplexity visibly stops at 4.2 s, two seconds before the Meta AI bump; narrating it four seconds after the viewer sees it would read as out of sync. So the order is: stuck (4.3), wall (6.2), nose to nose (7.4), photo finish (8.5), the slow one (9.6), winner last (on the slow-motion replay). The crash still comes before the slow one and the winner is still the last thing said.

### 1. Hook options (spoken, at most 7 words; true for this race without naming who wins)
| # | Line | Words | True? | Note |
|---|---|---|---|---|
| H1 | "Five AIs race, one hits the wall." | 7 | yes: only Meta AI touches it | concrete picture, statement, comma for flow |
| H2 | "Five AIs race. Not all finish." | 6 | yes: two do not | always reads clear; less visual |
| H3 | "Five AIs race. One gets stuck." | 6 | yes: Perplexity | a smaller stake than a wall |
| H4 | "Five AIs race their own cars." | 6 | always | clearest, weakest pull |
| H5 | "Hands off. Five AIs race." | 5 | always | "hands off" may confuse a cold viewer |
| H6 | "Five AIs, one road, one wall." | 6 | yes | rhythm, but no verb: the event is implied |
**Pick: H1, "Five AIs race, one hits the wall."** Subject (AIs racing) in the first three words, the threat ("hits the wall") in the same breath, a curiosity gap (which one?) that only the video closes, true whatever order the viewer guesses. Weak spot, written down: the surprise word sits at words 5-7, not in the first three (rule of 10.11); H1 keeps it because "Five AIs race" is what makes frame 0 understood. Backup if both blind readers miss it: H2. Voice: one breath with the comma, `--gap 0.06 --long 0.15 --max-speedup 1.45`, target about 1.9 s.

### Blind-reader test protocol (run BEFORE voicing, again on the rendered frame 0)
1. Start two fresh agents (no script, no file names, no plan). Tell each only: "This is the first frame of an Instagram Reel, 1080x1920. The bottom 35% is covered by Instagram's buttons and caption, so it is empty on purpose."
2. Give each: the frame-0 PNG, and the text "Spoken in the first second: 'Five AIs race, one hits the wall.'" Nothing else.
3. Ask exactly, in this order, and record the answers word for word:
   a. "What is this video about? One sentence."
   b. "Would you stop scrolling? Why or why not?"
   c. "Name the apps you see."
   d. "Is anyone driving the cars? Who decides how they move?"
4. Pass = both readers name AI apps (at least three of the five logos correctly) AND the topic (a race between AIs / their cars). Answer (d) is a finding, not a veto: "the AI drives" is close enough, the site explains that each AI wrote the steps.
5. A third fresh agent gets only the six hook texts above (no frame) and ranks the top 3 for (clarity, would stop), one line of reason each.
6. Write all answers word for word under "Blind readers, ep98" below, with the time. If (a) fails for both readers: switch to H2, rebuild frame 0 and test again with two new agents.

Blind readers, ep98: NOT RUN YET (T6 wrote the protocol; run it on the frame-0 PNG from T8).

### 2. Spoken script (13 lines, about 24 s; present tense; lines in `video/ep98/voice/lines.txt`)
Video time = race time + 5.4 s (the race starts on "Go").
| # | Video time (est.) | Line | Est. s | Why it is true |
|---|---|---|---|---|
| 1 | 0.0-1.9 | Five AIs race, one hits the wall. | 1.9 | Meta AI touches the wall at 6.15 s |
| 2 | 2.0-4.4 | Each AI gets the same job: teach a car to race. | 2.4 | premise by 4 s; one identical request to each |
| 3 | 4.5-5.4 | Hands off. Go! | 0.9 | nobody touches the cars; code runs as received |
| 4 | 5.7-8.5 | ChatGPT, Gemini, Claude, Meta AI, Perplexity. | 2.8 | roll call while the cars leave the grid; each logo pulses as named |
| 5 | 9.7-11.0 | Perplexity stops dead in the bend! | 1.3 | speed 0 from race 4.22 s, never moves again |
| 6 | 11.6-12.6 | Meta AI hits the wall! | 1.0 | race 6.15 s, hairpin |
| 7 | 12.8-13.8 | Claude and Gemini, nose to nose. | 1.0 | 0.03-0.06 lap apart all race |
| 8 | 13.9-15.0 | At the line, a photo finish! | 1.1 | 8.48 vs 8.68 s, spoken as they cross |
| 9 | 15.0-15.9 | ChatGPT takes its time. | 0.9 | finishes 10.58 s, crosses right after the line ends |
| 10 | 16.6-17.8 | Claude wins, by a hair. | 1.2 | on the slow-motion replay, "Claude" lands as its nose crosses |
| 11 | 18.0-19.6 | Send it to someone who uses Meta AI. | 1.6 | sendable: a named person; optional cut (saves 1.7 s) |
| 12 | 19.7-21.2 | The setup's in the link in bio. | 1.5 | LOCKED clip, `canonical-lines.json`, byte for byte |
| 13 | 21.3-24.2 | Tomorrow, they face a maze. Follow, so you see who gets lost. | 2.9 | **PROMISE TO CONFIRM**: true only if episode 99 (AI RACE #2, the maze, the same five AIs) publishes the next day |
Total about 24.2 s (about 22.5 s without line 11).

**PROMISE TO CONFIRM (line 13):** on 15.11 there is no `video/ep99/` and no `*-B.txt` answers in `video/ep98/answers/`: the maze arena and the five maze answers do not exist yet. Before episode 98 ships: maze arena frozen, PROMPT B sent to all five apps (one try each), ep99 ready for the next day. If not, re-voice line 13 as "Next race, a maze. Follow, so you see who gets lost." (no day promised).

Word checks: `python3 audio/script_lint.py --file video/ep98/voice/lines.txt` = "0 risky word(s) across 13 line(s)" (15.11.2026). Avoided on purpose: three, trust, Anthropic, first, track, drive, crash, steer, friend (FR), front (FR), never (-ER), gets out (flapped T), code, program, function, sensors. Brand names stay as they are ("Meta" has a flapped T; listen for it). Whisper writes "Claude" as "clawed" (accepted before). Lines 5-9 sit on real race events: each must be voiced at 1.3 s or less, or it overlaps the next event; if one runs long, shorten the words, never move or speed up the race.

### 3. Shot list (1080x1920; safe box x 65-1015, y 269-1248; at most 3 text lines at once; no code anywhere)
Base: Miki style paper (`video/ep89c`) with Roni's "not AI-looking" textures: hand-inked road edges, paper grain, uneven tape. The road (`track.json`, 950 x 808) sits 1:1 at x 65-1015, y 440-1248, so the whole circuit is always in the safe box. Each car body carries its real logo (about 84 px; ChatGPT, Gemini, Claude, Meta AI, Perplexity; T3 adds Perplexity's mark with its source URL) and leaves an ink line in its brand colour. Top strip y 285-350 = live ranking: five logos in race order, lap dots, no words; it re-orders with a soft slide. No word inside a filled box; no handle; nothing covers a car; no black wipes; nothing still for 2.5 s.

| Line | Video time | On screen | Motion |
|---|---|---|---|
| 1 | 0.0-1.9 | Frame 0 at full contrast: headline 2 lines, heavy ink, y 285-420 "FIVE AIs RACE, / ONE HITS THE WALL." (no digit first: a leading "5" reads as a list item) + a small handwritten line under it "same request" (3 lines total). The five logo cars on the start grid, engines shaking. The hairpin wall is marked with a hand-drawn arrow, no word. | Cars rock on the grid, ink exhaust puffs, camera breathes 1.00-1.02. Nothing still. |
| 2 | 2.0-4.4 | Headline swaps to "SAME JOB FOR EACH AI" (1 line). A taped paper note slides into the road's empty infield (not over a car): five little chat bubbles with the five logos and one identical line "teach this car to race" (plain words; the real prompt text lives on `/e/98`, not on screen). | Note slides in with a long ease, the five bubbles pop in one by one (0.12 s apart), note slides out at 4.3. |
| 3 | 4.5-5.4 | Hand-drawn start lights (no text), five circles filling; small handwritten chip under the strip: "pick one. comment it." (underline stroke, no box) | Lights fill on the beat of "Hands off", cars leave on "Go". Tick SFX per light. |
| 4 | 5.7-8.5 (race 0.3-3.1) | Whole road, five cars in true time. Live strip appears. | Each logo in the strip pulses as its name is spoken. Gentle camera push 1.00-1.04 toward the pack. |
| 5 | 9.7-11.0 (race 4.3-5.6) | Perplexity's car parked in the hairpin (it stopped at race 4.22: the voice comes 0.1 s after the picture). Hand-drawn "?" loop beside the car (beside, never on it); the strip slides Perplexity down to 4th as ChatGPT passes at race 5.0. | HAIRPIN CLOSE-UP 1: camera eases in to about 1.6x on the hairpin (x 65-500 of the road), other cars still visible passing through it, eases back out by 11.1. The race never pauses. |
| 6 | 11.6-12.6 (race 6.2-7.2) | Meta AI's car nose to the wall in the same hairpin. Small ink splash (it was slow: a bump, not an explosion), the logo tilts a few degrees, a hand-drawn X beside it. Strip: Meta AI greys and drops to last. | HAIRPIN CLOSE-UP 2: ease in to about 1.6x at 11.5 (race 6.1), hold the bump 0.8 s, ease out. Thud SFX at race 6.15 exactly. |
| 7 | 12.8-13.8 (race 7.4-8.4) | Claude and Gemini on the last straight; their two ink lines side by side. Strip: the top two logos tremble. | Camera drifts toward the finish line. |
| 8 | 13.9-15.0 (race 8.5-9.6) | Both cross (8.48, 8.68). A hand-inked "PHOTO FINISH" stamp drops beside the finish line (not over a car). Strip top two slots show "?" (decision held for the replay). | Flash of the chequered tape, camera shake 2 px, settles. |
| 9 | 15.0-15.9 (race 9.6-10.6) | ChatGPT on its last bend, crosses at 15.98; strip locks it in 3rd with "10.58 s". | Ink line completes; small tape tick. |
| 10 | 16.0-17.9 | SLOW-MOTION REPLAY of race 8.30-8.78 at 1/4 speed (1.9 s). Label top-left inside the safe box, handwritten: "REPLAY · 1/4 SPEED" (on screen the whole replay). Finish-line close-up: Claude's nose crosses at replay 0.72 s, Gemini's 0.8 s later. On "Claude wins", the Claude logo pops 1.0 to 1.15 and settles; "+0.20 s" written by Gemini. | Replay plays the real `race.json` frames, interpolated only for display; label never leaves. Soft crossfade back to live at 17.9. |
| 11 | 18.0-19.6 | RESULT CARD (the saveable card), taped paper, x 65-1015, y 430-1248: title "AI RACE #1 · 2 LAPS"; rows land slowest-result first, winner last: Perplexity "stuck in the bend"; Meta AI "touched the wall"; ChatGPT 10.58 s; Gemini 8.68 s; Claude 8.48 s. The road stays visible behind, ink lines kept. | Rows land 0.18 s apart; card drifts slowly. Card text is the only text (title + 5 short rows in a table count as the card, not as headline lines). |
| 12 | 19.7-21.2 | Card footer writes itself: "race your own AI: link in bio". | Underline stroke draws under it. |
| 13 | 21.3-24.2 | Card folds away; the five cars roll back to the grid along their own ink lines; a small maze sketch draws itself in the infield with the five logos at its entrance (teaser for 99). Last frame = frame 0 layout, for a clean loop. | Stroke-draw 1.2 s; soft crossfade; no black wipe. |
Checks for T8/T10: cars follow `race.json` frame for frame at 1x outside the labelled replay; close-ups never cut a car out of the frame for more than the zoom itself; safe-box and overlap check (`export/safe_check.js`); no still stretch over 2.5 s.

### 4. Caption (Instagram; 1,496 characters incl. the two placeholders, measured with Python; no hashtags)
```
Five AIs race, one hits the wall. Which AI did you think would win? Put it in the comments before you scroll down.

The test: ChatGPT, Gemini, Claude, Meta AI and Perplexity each get the same request, word for word: write the code that steers a race car around one road. Then all five cars race at the same time, on the same road, and nobody touches them.

Result (2 laps, true speed):
1. Claude, 8.48 s
2. Gemini, 8.68 s (0.20 s behind)
3. ChatGPT, 10.58 s
Meta AI: touches the wall in the hairpin at 6.15 s
Perplexity: stops in the hairpin and stays there (still stuck at the 60 s limit)

What is real:
- One try per AI, in its own chat app, on [DATE TO CONFIRM].
- Each car runs the exact answer that AI gave. Nothing fixed by hand.
- The road and the rules were locked before any answer came in.
- Run three times, the race gives the same result every time.
- The race plays at true speed. Only the photo-finish replay is slowed down, and it says so on screen.

What this does not show:
- Which AI is "smartest". It is one small task, one try each. Ask again and the order may change.
- Which model each app used. We name the apps only.

Full disclosure: the tools behind this channel are built with Claude, and Claude wins here. That is exactly why the road was locked first and all five answers are public, so you can check them.

Race your own AI: the road, the request and all five answers are on the page in the link in bio.

Tomorrow: the same five AIs face a maze. [PROMISE TO CONFIRM]
```
Before shipping: fill the date from David's screenshots; drop the last line or change "Tomorrow" to "Next" if ep99 is not ready; if David confirms Perplexity ran a Claude model (its answer shares Claude's constants: 35, 0.9, 110, 90, 55, 1.5, 2.2), add under "What this does not show": "Perplexity can run models from other companies, including Claude; we did not check which one it used." Then `python3 export/check_caption.py 98` and the `ig-caption` skill.

### YouTube (no angle brackets)
Title: `Five AIs race, one hits the wall (AI Race #1)`
Description:
```
ChatGPT, Gemini, Claude, Meta AI and Perplexity each get the same request: write the code that steers a race car. Five real answers, one road, true speed, one try each, nothing fixed by hand. The road was locked before any answer came in.
Result: 1. Claude 8.48 s, 2. Gemini 8.68 s, 3. ChatGPT 10.58 s. Meta AI touches the wall in the hairpin. Perplexity gets stuck in the hairpin.
One small task, not a ranking of intelligence. The channel's tools are built with Claude, and Claude wins here: all five answers are public so you can check.
Race your own AI: https://www.actually-works.com/e/98
```

### /e/98 setup guide (English only; for `studio/lib/articles.ts` steps[]; button labels must match what T11 actually builds)
1. Scroll to **The race** on this page and press **Play**. The race from the video runs again in your browser, with the same five answers, at true speed.
2. Under any car, click **Show code**. You see the exact answer that AI gave, as we received it, nothing changed.
3. Scroll to **The request** and click **Copy prompt**. This copies the request we sent, word for word.
4. Open the AI you want to test (ChatGPT, Gemini, Claude, Meta AI, Perplexity or any other) in a new tab and start a new chat. Leave the settings as they are: no extra modes.
5. Click in the message box, paste (Ctrl+V on Windows, Cmd+V on Mac) and send. Wait until the answer stops writing.
6. In the answer, click **Copy** on the code block. If there is no Copy button, select the whole code with the mouse and copy it (Ctrl+C or Cmd+C).
7. Come back to this page and click **Add my AI**. Paste the answer into the box and click **Race**.
8. Your car joins the same road as a sixth car. Watch two laps. If it stops or touches a wall, that is a real result, not a bug on the page.
9. Optional: tell your AI where the car went wrong ("the car stops in the hairpin, fix it"), paste the new answer and race again. That is a second try, so it does not compare with our one-try race.
10. Optional: send the page to a friend and race your two AIs against each other.
What happens after step 7: the pasted code runs only inside your own browser tab. Nothing is uploaded or saved.

### 5. Scores (judgements, not measurements; my scores have not predicted our views, Spearman -0.23)
HOOK 78 (clear subject at word one and a picture to match; the threat sits at words 5-7). VIRALITY 74 (one stage, constant motion, five rival brands, a side to pick, a photo finish; but Claude leads from 1.5 s, so the live strip shows the likely winner early, and our account rarely gets comments). OVERALL 74. Predicted views 350-1,500, most likely about 600. Log the 48 h / 72 h numbers in `channel/score-calibration.md`.

### Open questions for David
1. Which model did Perplexity use (and is it set to a Claude model)? Its answer shares Claude's constants.
2. Screenshots of the five chats (app, date, model label) for the caption date and the `/e/98` page.
3. Episode 99 (maze): not started (no arena, no PROMPT B answers). Confirm it can go out the day after 98, or line 13 changes to "Next race".
