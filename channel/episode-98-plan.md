# Episode 98 plan: AI RACE #1 (written 14.11.2026, PLAN ONLY)

Status: nothing built, voiced, rendered, committed or published. Scores are judgements, not measurements.
Format: **AI RACE #N** (new numbered format; slot = the challenge). Funnel: TOP. Next step for a viewer: the playable arena on `/e/98` (MID).

One sentence: the same request goes to ChatGPT, Gemini, Claude and Meta AI ("write the code that steers a car"); the four real answers race on ONE road at the same time; some hit the wall, one wins.

---

## 1. Topic choice, data, duplicate check, verification

### Why this, from the data
- **What spreads outside (numbers as read on 13.11, `new-formats-2026-11-13.md`):** "same prompt, rival AIs, real code output" is the only AI format where small faceless accounts get huge views: AI Code Clash (10K subscribers) 14M, 780K, 683K, 495K on single Shorts; @ouali.code 303,100 on TikTok. The winners are outputs that MOVE and brands that are RIVALS (ChatGPT vs Claude vs Gemini), not four versions of one brand.
- **Races with a side to pick spread without any face:** marble-race channels, e.g. 8.5M views from a 244K channel, 7.9M from 157K (noodletomato niche page, vendor estimate, read 14.11.2026); Crazy Marble Race 112.4M total views, 256K subscribers (vidIQ, 13.11.2026). Vice already described the mechanic in 2016: colours stand for countries "so you can root for your home country".
- **Failures are real in such contests:** an independent maze contest (boreal.social, 21.3.2026, code at github.com/rrezel/llmcomp) had 3 of 5 AI bots eliminated. So a real run is likely to produce a loser, which is the drama. Not guaranteed.
- **What David rejected on ep97:** four equal boxes, a still picture, one brand, a question hook, a long hook. A race fixes each: ONE stage, constant motion, four rival brands, a stated result as the hook.
- **Our own winners (86, 80, 82):** a known AI brand doing something a viewer does not expect, with a stake in line one. "ChatGPT hits a wall" keeps that, without a chat test.
- **Rotation rule:** 96 and 97 were Claude only. 98 has four brands, ChatGPT first.
- HONEST GAP: I found no short with readable numbers that is exactly "AI-written code racing in one arena" (CodeArenaAI "Space Invaders Battle" and a "Minecraft AI Battle" Short exist, views NOT AVAILABLE). This is a hybrid of two proven formats, itself unproven, and all hard numbers are YouTube/TikTok, not Reels. Log it in `channel/experiments.md`.

### Duplicate check (done before proposing)
`grep -i -E "race|maze|arena|contest|side by side|versus| vs "` on `channel/topics-covered.txt`: **0 hits**. `content-memory.md`: 0 hits for "ai race|arena|marble|maze race". `episode-inventory-2026-11-14.md`: the nearest is ep97 (four Claude models draw a pelican, format "same prompt, four AIs"). 98 is not the same topic or picture (rival brands, moving code, one arena, a winner). `channel/hot-radar.md` does not exist yet (nothing to check).

### Product facts (web, 14.11.2026)
| Fact | Source | Status |
|---|---|---|
| ChatGPT Free: unlimited everyday text chats, default model "Luna" | help.openai.com/en/articles/9275245-chatgpt-free-tier-faq (says **GPT-5.6 Luna**, "updated 6 days ago"); chatgpt.com/pricing lists GPT-6 Luna; geotoolbox.ai/blog/chatgpt-pricing says Free runs **GPT-6 Luna** since 8.10.2026 | Sources DISAGREE on 5.6 vs 6: **UNCONFIRMED**. Use the name shown on David's screen. |
| Gemini free plan includes Canvas; free model "Flash-Lite" (one source adds "Gemini 4 Hydrogen") | gemini.google/overview/canvas ("available for all Gemini users"); roam.gg/gemini-game-maker (4.11.2026); nocode.mba/articles/gemini-pricing (13.11.2026) | Canvas free: confirmed by Google's page. Model name: **UNCONFIRMED**, read it off the screen. |
| Claude Free gives Sonnet and Haiku, limits reset each 5 hours | ai4chat.co/free-ai-models (7.11.2026, secondary) | **UNCONFIRMED** (secondary only). Read it off the screen. |
| Meta AI is free with a login, model not named | same secondary page | **UNCONFIRMED**; whether it returns runnable code is UNKNOWN until the test. If it refuses, the car "does not start" and we show that. |
Rule for the video: no model name is spoken. On screen and in the caption we write only what David's screenshots show (app + model label + date). The T4 task re-checks on test day.

### What the video needs, and who can make it
- **In this container (no David):** the arena engine, the fixed road, the race replay, the scene, voice, music, site page.
- **Needs David (about 15 minutes, one time):** the four real answers. There are no keys for ChatGPT, Gemini or Meta AI here (only Claude), and for a fair test all four must come from the free chat apps on the same day. Steps (the orchestrator gives them to him in Hebrew, labels in both languages):
  1. On the computer open four tabs: chatgpt.com, gemini.google.com, claude.ai, meta.ai. Log in as usual.
  2. In each tab start a new chat. Do not switch model, do not turn on Think, Canvas or Search.
  3. Paste PROMPT A (below) exactly, press Enter, wait until the answer ends.
  4. Take a screenshot of the whole chat window (it must show the prompt, the start of the answer and the model name if the app shows one).
  5. Click **Copy** on the code block, paste it into a text file, save as `chatgpt-A.txt` (then `gemini-A.txt`, `claude-A.txt`, `meta-A.txt`). Do not fix anything, even if it looks wrong.
  6. One try each. If an AI answers without code, save what it said in the file anyway.
  7. Repeat steps 2-6 with PROMPT B (the maze, for episode 99), files `...-B.txt`.
  8. Send the 8 text files and 8 screenshots in the chat. (Optional: the share link of each chat.)

**PROMPT A (frozen; the arena is built to it, not the other way round):**
```
Write one JavaScript function for a racing game. Reply with only the code.

function steer(s) { ... }

The game calls it 60 times a second. s has these numbers:
s.front, s.left, s.right: distance in pixels from the car to the wall,
straight ahead, 45 degrees left and 45 degrees right (0 to 400).
s.speed: the car's speed, 0 to 10.
Return { turn, gas }: turn from -1 (full left) to 1 (full right), gas from 0 to 1.
Gas under 0.2 brakes. The car is 20 pixels wide. The road is 90 to 140 pixels wide
and has one hairpin. Touching a wall ends the race for that car.
Goal: finish 2 laps as fast as you can. No libraries.
```
PROMPT B (episode 99, maze, same shape): `function move(v)`, v = the 4 neighbour cells (wall / open / exit) plus the car's own x, y; return "up" | "down" | "left" | "right"; 500 steps max; the maze is not shown to the AI. T14 writes the exact text before David starts.

### Fairness rules, fixed BEFORE any answer exists (never-fabricate)
1. Road, physics and prompt are frozen and hashed (sha256 of `track.json` + `arena.js` written into `channel/episode-98-script.md`) before David pastes anything.
2. Calibration uses only our own two reference drivers (a naive one must hit the wall, a careful one must finish 2 laps in 7-11 s). After that, nothing in the arena changes.
3. One try per AI. The code runs as received; we only take the code block out of the reply. Code that throws or returns nonsense = the car does not start or stops, shown as it is.
4. Cars are ghosts to each other (no contact), so start position cannot decide the race.
5. Whatever happens is the video. No second run to get a better story. If the result is dull (all four finish within 0.3 s), we tell David and he decides; we do not re-roll.

---

## 2. Concept score on the 6-point checklist, and the viral mechanic

| # | Check | Result |
|---|---|---|
| 1 | A specific, surprising thing on the viewer's own account/phone | PARTIAL: it is the AI they use daily (and for some, pay for) losing in public, not their own account |
| 2 | A curiosity gap only the video closes | STRONG: which AI wins; stated loss first, winner last |
| 3 | Something to save, as a screenshot-able card | YES: the result card (order, times, where each one stopped) + "race your own AI" on `/e/98` |
| 4 | A named person to send it to | YES: "the buddy who pays for [the AI that hit the wall]" |
| 5 | A reason to watch twice | YES: you watch your own pick the second time; each car leaves an ink line, so the exact place it goes wrong is visible; the end returns to frame 0 |
| 6 | Checkable by a stranger in 30 s | YES: `/e/98` runs the same four files live in the browser, code readable; the prompt is there to paste |
Checklist score (judgement): 5 of 6 clear, 1 partial = about 78.

**Mechanic, beat by beat**
- 0.0 s: the PROOF first: frame 0 is the real moment a famous AI's car is nose-first in the wall (taken from the race log), ink splash still moving.
- 1.6 s: rewind to the start grid (cars slide back along their own ink lines), "Pick yours now": the comment is one word, the name of an AI. Brand loyalty does the work.
- Race in true time on ONE big road. A logo strip re-orders live.
- The winner is the last thing revealed; the result card lands in the final seconds; cars roll back to the grid = loop.
- Pinned comment for David to post by hand if he wants: "Which AI did you pick?"

---

## 3. Hooks

The result is unknown until the race runs, so the hook comes from this table. Brand slot = the best-known AI the claim is TRUE for (order: ChatGPT, Gemini, Claude, Meta AI). All: 6 words or fewer, a statement, present tense, no digit first.

| # | Spoken line 1 | Use when |
|---|---|---|
| A | "[ChatGPT] hits a wall. Pick yours." | a top brand really crashes (most likely case) |
| B | "[ChatGPT] loses to [Meta AI]." | the underdog beats a top brand |
| C | "One AI ends this race." | exactly one car finishes |
| D | "No AI ends this race." | all four crash |
| E | "AI race. [Gemini] laps [ChatGPT]." | a real lapping happens |
| F | "[Claude] wins, [ChatGPT] hits a wall." | fallback if A reads unclear to blind readers |
| G | "One road, four AIs, one wall." | exactly one crash and it is not a top brand |
| H | "AI cars race. Pick yours, go." | nobody crashes (weakest; tell David first) |

**Recommended: A, "ChatGPT hits a wall. Pick yours."** Reason: the surprise ("hits a wall") is in the first words, the best-known product is word one, it is a result and a dare in two beats (like ep96's three short beats), and it leaves the winner open. Voice it with a comma feel, not a full stop (`--gap 0.06 --long 0.15 --max-speedup 1.45`), target about 2.0 s. Avoided on purpose: "only" (-LY), "first" (R + cluster), "crash", "track", "drive" (R clusters), "winner" (-ER).

**Blind-reader protocol (before voicing, and again on the rendered frame 0)**
1. Two fresh agents, no script, no file names. Each gets ONLY the frame-0 PNG and the text of the first spoken second. Tell them the safe box (the bottom 35% is the Instagram interface, empty on purpose).
2. Ask: "What is this video about?" and "Would you stop scrolling, and why?"
3. Pass = both name the products (AI chat apps) AND the topic (a race of their code / one hits a wall). "Would not stop" is a finding to fix if cheap, not a veto.
4. A third agent ranks the top 3 hook lines that are TRUE for the result (clarity, stop) on text only.
5. Write the answers word for word into `channel/episode-98-script.md`.

---

## 4. Script, shots, logos, cards

### Spoken lines (slots in brackets are filled from `results.md`, nothing else)
1. [Hook from the table.] e.g. "ChatGPT hits a wall. Pick yours."
2. "Same request to each AI: write the code that steers a car."
3. "Pick yours now. Go!"
4. "[ChatGPT] hits the wall at the big bend." (or: "[X] stops on lap one.")
5. "[Gemini] slows down, and stays on the road." (a true line about the car that survives longest or leads)
6. "[Claude] wins. Two laps, no wall."
7. "Send it to the buddy who pays for [ChatGPT]."
8. "The setup's in the link in bio." (locked clip from `canonical-lines.json`, byte for byte)
9. "Tomorrow, the same AIs face a maze. Follow, and see who gets lost."

Word checks: no THR/TR/DR words, no "three/trust/Anthropic/first/track/drive/crash"; no -ER/-LE/-LY endings except brand names; plain words a friend would say; present tense. Whisper writes "Claude" as "clawed" (accepted before). Lines 4-6 must each be 1.6 s or shorter: they sit on the race clock (see below). Line 9 is a promise: episode 99 = AI RACE #2, the maze (PROMPT B is collected in the same sitting, so the material exists before 98 ships). If 99 cannot go out the next day, re-voice line 9 as "Next race: a maze. Follow, and see who gets lost."

### Timing model (one exception to "the picture follows the voice", stated openly)
Lines 1-3 and 7-9 are built at their own pace and the scene follows them (`retime` pattern). The race itself plays in TRUE time from `race.json` (never slowed, never sped up), and lines 4-6 are placed on the real event times (wall hit, lead change, finish). Expected length: hook 2.0 + setup 3.4 + start 1.3 + race 7-11 + ending 6.5 = about 20-24 s.

### Shot list (1080x1920, safe box x 65-1015, y 269-1248; at most 3 text lines at once)
| Time | Line | On screen | Motion |
|---|---|---|---|
| 0.0-2.0 | 1 | Headline, 2 lines, heavy black, y 285-420: "[CHATGPT] HITS / A WALL" with the real ChatGPT mark before the name. The road fills x 65-1015, y 440-1248 (hand-inked on paper). The ChatGPT car is nose-first in the wall at the hairpin: the real crash frame. The other cars are mid-road. | Ink splash still spreading, the car rocks, the other cars keep rolling for 0.6 s. Nothing is still. |
| 2.0-5.4 | 2 | Headline swaps to 1 line "AI RACE #1" (y 285-350); chip (1 line): "same request · each AI writes the code". Cars rewind along their own ink lines to the grid; the four real logos sit ON the cars (logo = the car body, about 84 px). | Rewind 0.9 s, long ease; then a paper card slides in for 1.6 s showing the first 6 lines of the real prompt (card inside the road's empty infield, not over the cars), slides out. |
| 5.4-6.7 | 3 | Hand-drawn start lights (no text), cars shake on the grid; chip: "comment your AI". | Lights fill one by one, tick SFX; on "Go" the cars leave. |
| 6.7-about 15 | 4-6 | Whole road always visible (one stage). Top strip y 285-350: the four logos in race order + lap dots (no words). Each car leaves an ink line in its brand colour. A car that hits the wall: splash, the logo tilts, a hand-drawn X beside it (never on top of it). | True-time replay. Soft camera push-in 1.00 to 1.06 toward the action, drift back. Logos in the strip slide to re-order. On the finish: chequered tape drops, the winning logo pops 1.0 to 1.15 and settles. |
| about 15-19 | 7-8 | RESULT CARD (the saveable card), taped paper, x 65-1015, y 430-1248: title "AI RACE #1 · 2 LAPS"; four rows: logo, time or "wall, lap 1, big bend"; footer "race your own AI: link in bio". Behind it the road stays visible on top, ink lines kept. | Rows land one by one (0.18 s apart), slowest result first, winner last; card drifts slowly. |
| about 19-22 | 9 | Card folds away; the cars roll back toward the grid; a small maze sketch draws itself in the infield (teaser for 99); last frame = the layout of frame 0's road so the loop is clean. | Stroke-draw 1.2 s; no black wipe anywhere; soft crossfades. |

Rules applied: no word inside a filled box (headline is plain ink; the chip is an underline stroke, not a pill); no handle overlay; nothing covers a car; no frame still for 2.5 s; no 2x2 grid; Miki style base (`video/ep89c` paper, tape, ink border, hard shadow), accent = each brand's own colour on its car and line. To look less "AI-made" (Roni, 10.11): wobbly hand-inked road edges, uneven tape, paper grain, ink that bleeds.

### Real logos (fetch, never redraw; keep the source URL beside each file)
| Mark | Where |
|---|---|
| ChatGPT | repo: `channel/assets/ep70-chatgpt-logo.svg` (check it is still the current mark at openai.com/brand) |
| Gemini | repo: `channel/assets/ep65-gemini-logo.svg` (check against Google's current Gemini mark; Wikimedia Commons "Google Gemini icon" as second source) |
| Claude | repo: `video/ep97/hf/assets/claude-mark.svg` |
| Meta AI | NOT in the repo: Wikimedia Commons "Meta AI logo" or about.meta.com brand resources; T3 fetches and records the URL |

### Proof cards
(1) The prompt card (real text). (2) The result card. (3) On `/e/98`: the four screenshots of David's chats (crop any account name or avatar; David's first name stays out), the four code files as received, the live arena.

---

## 5. Caption, YouTube, setup guide

### Instagram caption (template, about 900 characters; fill brackets from `results.md`; `wc -m` under 2,200; run `check_caption.py` and `ig-caption`)
```
[ChatGPT] hits a wall. Which AI did you pick?

Same request to ChatGPT, Gemini, Claude and Meta AI: "write the code that steers a car." Then all four race on the same road, at the same time.

Result: [1. Claude 8.4 s · 2. Gemini 9.1 s · ChatGPT: wall, lap 1 · Meta AI: wall, lap 2]

What is real: each car runs the exact code the AI gave, copied from the free chat app on [date], one try each, nothing fixed by hand. The road was locked before the answers came in. The race in the video plays at true speed.

What this does not show: which AI is "smartest". It is one small coding task, one try, free plans ([model names as shown on screen]). Run it again and the order may change.

Race your own AI: the road, the prompt and all four code files are in the link in bio.

Send it to the buddy who pays for [ChatGPT].
```
No hashtag block (Mosseri: no reach effect); at most `#ai`.

### YouTube (no `<` or `>`)
Title: `[ChatGPT] hits a wall: 4 AIs write code, then race (AI Race #1)`
Description: `Same request to ChatGPT, Gemini, Claude and Meta AI: write the code that steers a car. Four real answers, one road, true speed. Result: [order]. One try each, free plans, [date], nothing fixed by hand. One small coding task, not a ranking of intelligence. Race your own AI: https://www.actually-works.com/e/98`

### Setup guide for `/e/98` (English only; `check_setup_guide.py` must pass)
1. Open the arena on this page. The race you saw starts by itself, with the same four code files.
2. Click **Show code** under any car to read the exact answer that AI gave.
3. Click **Copy prompt**. This is the request we sent, word for word.
4. Open the AI you use (ChatGPT, Gemini, Claude, Meta AI or any other) and start a new chat.
5. Paste the prompt and send it. Wait for the answer to end.
6. Click **Copy** on the code block in the answer.
7. Back on this page, click **Add my AI**, paste the code and click **Race**. Your car joins the same road as a fifth car.
8. Watch two laps. If your car stops at a wall, that is a real result, not a bug on the page.
9. Optional: ask your AI "the car hit the wall at the hairpin, fix it", paste the new code and race again. That is a second try, so it is not comparable with our one-try race.
10. Optional: send the page to a friend and race the two cars.
What happens after step 7: the pasted code runs only inside your own browser tab; nothing is uploaded or saved.

---

## 6. Build plan (parallel tasks for the orchestrator)

Standing limits: ONE TTS render at a time under `flock /tmp/tts.lock`; no agent publishes, merges, or touches secrets or the PIN; all work stays on `ep86-build`; one merge at the end with the episode (David's go-ahead); long renders run inside an active turn.

| ID | Task | Tier, why | Inputs | Outputs | Acceptance test |
|---|---|---|---|---|---|
| T1 | Arena engine + frozen road | **opus**: fairness and determinism; a wrong physics call costs a day and David's re-test | PROMPT A spec | `video/ep98/arena/arena.js` (pure functions, fixed 60 Hz step, 3 ray sensors, ghost cars), `track.json`, `run_race.mjs` (Node, runs code in `vm` with a 5 ms/step budget, no network, writes `race.json`: per-frame x, y, angle, lap, status), `ref-naive.js`, `ref-careful.js`, sha256 of road + engine | Same input twice gives a byte-identical `race.json`; naive hits the wall; careful finishes 2 laps in 7-11 s; road width 90-140 px, one hairpin, exactly as the prompt says. Then message "PROMPT A frozen" so David can start. |
| T2 | Collect the 8 answers | **David** (15 min) | steps in section 1 | `video/ep98/answers/*.txt`, screenshots | 8 files, 8 screenshots, one try each |
| T3 | Logos | **haiku**: fetch and file, no judgement | table in section 4 | `video/ep98/hf/assets/logos/{chatgpt,gemini,claude,meta-ai}.svg` + `SOURCES.md` | Each file opens, matches the live brand page by eye (one screenshot each), URL recorded |
| T4 | Product re-check on test day | **sonnet**: careful reading of official pages | David's screenshots | table in `episode-98-script.md`: app, plan, model label as shown, official page URL, UNCONFIRMED list | Every on-screen or caption claim has a URL or a screenshot; no model name used that is not on a screenshot |
| T5 | Run the race, write the truth table | **sonnet** runs; **opus** reviews the table | T1, T2 | `video/ep98/arena/race.json`, `channel/episode-98-results.md` (order, times to 0.01 s, where each car stopped, any code error text) | 3 runs identical; every sentence in the script maps to a row; code files unchanged (sha256 before and after) |
| T6 | Final script, hook pick, blind readers | **opus**: judgement, honesty of each line | T5, section 3-4 | `channel/episode-98-script.md` (lines, hook table result, blind answers word for word, scores) | Both blind readers name product and topic; every spoken claim true in `results.md`; hook 6 words or fewer |
| T7 | Voice | **sonnet**: runs an existing pipeline | T6 | `video/ep98/voice/narration.wav`, cues | `script_lint.py` clean; built under `flock /tmp/tts.lock` with `--gap 0.06 --long 0.15 --max-speedup 1.45`; Whisper matches each line, re-roll only wrong lines; hook about 2 s; lines 4-6 each 1.6 s or less; `voice_quality.py`, accent check, `voice_doctor.py` no BAD |
| T8 | Scene | **fable**: David asked that Fable codes scenes; the motion quality is the product | T1 road, T3 logos, `race.json`, cues, shot list | `video/ep98/build98.py` to `video/ep98/hf/index.html` (HyperFrames + GSAP, `video/ep89c` recipe) | Cars follow `race.json` frame for frame at 1x; frame 0 at full contrast with the crash; safe box clean; at most 3 text lines; no still stretch over 2.5 s (measure); no overlay on a car; loop frame equals frame 0 layout |
| T9 | Music, SFX, mix | **sonnet**: mechanical with measurement | T7, T8 render | `video/ep98/mix98.py` (copy of `mix97.py`), `sfx98.json` (ticks, tyre squeal, thud from `video/ep89c/sfx`), bed from `pick_real_track.py` exact length; first pick `punchy--hip-hop-beat--themountain.mp3` (no complaint on 89c) | `check_music_bed.py` ok; bed -6 to -18 dB under the voice in 300-3500 Hz; -14 LUFS, -1 dBTP; row added to `channel/music-notes.md` |
| T10 | Gate and eyes | **opus**: catches what tools miss | all | `video/ep98/out/gate-v1.txt`, a frame sheet | `export/check_hf.sh` all PASS (a FAIL on transient crossfade overlap must be checked by eye and written down); frames read twice in full; after any fix the whole gate runs again |
| T11 | Site page + playable arena | **sonnet** builds, **opus** reviews safety | T1, T5, section 5 | `studio/lib/articles.ts` entry 98 (steps above), arena page under the episode route, route listed in `studio/lib/routes.ts` | `check_setup_guide.py` and `npm run check:routes` pass; pasted code runs in a sandboxed iframe (`sandbox="allow-scripts"`, no network, no storage); no Hebrew; not merged alone |
| T12 | Caption and YouTube text | **haiku**: fill a template and lint | T5, section 5 | `channel/episode-98-caption.txt`, `channel/episode-98-youtube.txt` | `wc -m` under 2,200; `check_caption.py` passes; no `<` `>`; every number equals `results.md` |
| T13 | Playable review page for David | **haiku**: mechanical | T10 output | one private Artifact page, 720 px review copy, updated in place | Video plays with sound after a tap; page says it is a review copy and that audio was measured, not heard |
| T14 | Episode 99 groundwork | **sonnet** | PROMPT B outline | exact PROMPT B text, `video/ep99/arena/maze.js` + frozen maze + hash | Reference bots: naive fails, careful exits; ready before David starts T2 |

Order: T1, T3, T14 and the T11 skeleton start now in parallel. T2 starts when T1 and T14 report "frozen". Then T4 + T5, then T6, then T7 (TTS lock), T8 can start on the `race.json` right after T5 and take final timings from T7's cues. T9, T10, T12, T13 after the render.

### Cannot be verified here (say it to David as it is)
- The audio is measured, not heard. The cloned voice is capped by its calm reference; a race wants more energy than it can give.
- That each chat app really used the model its label shows; we report the label only.
- Whether this format travels on Reels (all outside numbers are YouTube/TikTok). ep97's trial reading is not in yet.
- Whether anyone comments (46 of 50 of our reels have none).
- Trademark use of four logos together is normal editorial use as far as I know; no legal check was done.

---

## 7. Honest scores, prediction, biggest risk

Scale: `channel/score-calibration.md` (200 views = 50, 10,000 = 100). My scores have not predicted our views (Spearman -0.23); they are labels.

| Score | Value | One-line reason |
|---|---|---|
| HOOK | **80** (hook A with a real ChatGPT or Gemini crash; 70 with fallback H) | Top product is word one, the surprise is in the first words and shown on frame 0; but it is not happening to the viewer's own phone |
| VIRALITY | **76** | One stage, constant motion, a side to pick, a loser to tease a friend with, a loop; unproven on Reels and our account rarely gets comments or sends |
| VALUE | **68** | A playable arena and a prompt to copy is real and saveable, but it is fun, not a thing most viewers need |
| OVERALL | **75** | Stronger than ep97 (73) on every point David raised, still under 85 |

**Predicted views: 350-2,000, most likely about 700** (scale 57-79, centre 66). Reasoning: no class baseline exists for this format on our account; our median is about 211, the Miki-style ep89 reached 1,198, ep97 (same family, still picture) was labelled 300-1,500 with no reading yet. Above 2,000 only if comments or sends fire.

**The honest overall is under 85.** What would lift it: (1) a truly dramatic real result (ChatGPT in the wall at the very first bend, or Meta AI winning): cannot be arranged, only found; (2) proof that the format travels on Reels (read ep97's trial at 48 h before finishing 98); (3) a second and third race, so the series is recognised in the first second; (4) a more energetic voice reference recording from David; (5) real comments in the first hour (David answers each one).

**Single biggest risk:** the race is dull or unclear in the first second: all four cars finish close together, so there is no wall, no loser and no hook A; then the honest hook is H and the honest overall drops to about 66. We will know this before any voice or scene work (after T5), and at that point the right move is to tell David and let him choose between publishing it as it is, or holding the format for the maze (episode 99) as the first race. No re-run to get a better story.

## Hook update 14.11.2026 (David: "good content, bad hook")
Fable's "ChatGPT hits a wall. Pick yours." rejected (predicts a result we do not know; "pick yours" unclear). Blind reader (one viewer, judgement), 12 options true-whatever-happens test: ranked 9 "Four AIs race. One survives." (clarity 9, stop 8; TRUE ONLY IF exactly one car survives), 12 "Four AIs are driving right now." (always true, weak pull), 6, 7. Reader's own best, always true: A "Four AIs race. Nobody touches the wheel." Plan: use A if the outcome is not known/not clean; use "One survives" ONLY if the real race ends with exactly one survivor (decided after the race, T6). No re-run of the race to fit a hook.
