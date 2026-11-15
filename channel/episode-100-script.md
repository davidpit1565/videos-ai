Publish mode: REGULAR (proposed, David to confirm)

# Episode 100 (internal name ep100): VIRAL CLAIM, CHECKED #1: Graphify and "70x" (script)

Status: script only, 15.11.2026. No voice, no build, no commit. Plan, beat list, frame 0, sources and scores: `channel/episode-100-plan.md`. Facts: `channel/ref-graphify-verify-2026-11-15.md`.
We have NOT installed or tested Graphify (this container blocked installing third-party code). The reel is a fact-check of a viral claim built on public sources, and no line may suggest that we ran it.

## Spoken lines (10 lines, 115 words, about 35 s estimated; present tense)
Voice build: `--gap 0.06 --long 0.15 --max-speedup 1.45`. Hook target about 2.6 s, one flow ("Seventy times more Claude Code" in one breath, short beat, "Not even close.").
| # | Line | Est. s | True because (source) |
|---|---|---|---|
| 1 | Seventy times more Claude Code. Not even close. | 2.6 | Viral claim "up to 70x fewer tokens" (reference caption); independent runs: -18% or more tokens (Graphify blog) |
| 2 | Viral posts say a free tool makes your twenty-dollar plan do hundred-dollar work. | 4.4 | That is what the posts say ("says"); Pro $20, Max $100 (claude.com/pricing) |
| 3 | The problem is real: every new chat, Claude Code reads your files again. | 3.8 | The problem Graphify describes. NOT in the verify file: re-check against Claude Code's docs before voicing; fallback line in the plan, section 9 |
| 4 | The tool is Graphify, about a hundred fifty thousand stars on GitHub. | 3.6 | 148.2k stars, repo page, 15.11.2026 |
| 5 | It maps your code once, so Claude looks things up instead of rereading. | 3.8 | README; verify file "what we may truthfully say" |
| 6 | The seventy? One best case, against reading every file at once. | 3.4 | 71.5x example: 52 files, 123k vs 1.7k tokens vs a read-every-file baseline |
| 7 | One real test saves some. The next one uses more. | 3.2 | -18% (The Gray Cat run); +49.5% input tokens (FastAPI, Ponfick), both reported on Graphify's own blog |
| 8 | And the hundred-dollar plan is five times the usage. No test we found comes close. | 5.0 | Max "5x Pro usage" (claude.com/pricing); no test in the verify file is near 5x |
| 9 | The setup's in the link in bio. | 1.8 | LOCKED clip, `audio/voice/profile/canonical-lines.json`, byte for byte |
| 10 | Tomorrow, five AIs face a maze. Follow, so you see who gets lost. | 3.4 | **PLACEHOLDER.** Must name the episode published the day after ep100. If ep99 (maze) goes out first, this names ep101 instead |
Lines file for the lint: scratchpad `ep100/lines.txt` (copy into `video/ep100/voice/lines.txt` when the build starts).

### Word checks
`python3 audio/script_lint.py --file <lines>` on 15.11.2026: **1 risky word across 10 lines**: "stars" (line 4, R + cluster). Kept on purpose: the star count is part of the reference's line David wants, it sits mid-sentence, and the number is on screen. If his ear hears it swallowed, use the fallback: "The tool is Graphify: free, and huge on GitHub." (the 148.2k stays on screen).
Fixed before this version: "cheaper" (hook, -ER) → "more"; "fewer" (-ER) dropped from the voice; "single" (-LE) → "every file at once"; "percent" (-ENT) and "another" (-ER) → "One real test saves some. The next one uses more."; "fifth" (-TH) avoided.
Avoided on purpose (CLAUDE.md 13.11): three, trust, Anthropic, tokens (jargon), install, command, terminal, knowledge graph (jargon, said as "maps your code").
To listen for: "Graphify" (GR cluster, a brand name: it stays); "Claude Code" must sound like ONE name (gap under about 0.12 s by Whisper word times, rule of 15.11); "hundred-dollar" (DR); "twenty-dollar" (flapped T).

## Hook check (CLAUDE.md)
- Subject in the first second, said AND shown: "Claude Code" by word 5; frame 0 shows the Claude Code and Graphify marks and "70x MORE CLAUDE CODE?". PASS on paper; blind readers decide.
- Surprise in the first 3 words: "Seventy times more". PASS.
- Short statement, not a question: 6-word claim + 3-word punch. PASS (9 words in total, the punch is a separate beat).
- Starts with a digit? Spoken "Seventy", on screen "70x MORE" sits second on the card after the logos; not read as a list item.
- Felt in 3 s: only by people who pay for Claude or hit its limits. A cold non-coder may not feel it: the honest limit of this topic.

## BUILD-UP check (CLAUDE.md 15.11)
1. Open question stays open and gets closer each beat: "if not 70, what?" (beats 1-7) and "does $20 do $100 work?" (beats 2-8). YES.
2. Every beat adds something new: claim, money claim, the real problem, the tool's scale, how it works, the source of 70, the real tests, the pricing verdict. YES (beat 5 is the weakest: cut it first).
3. Reasons to stay at about 10 s (148k stars: maybe it IS real?) and about two thirds (the counter flipping to +49.5%). YES.
4. No flat stretch: every beat changes the picture (cards, screenshot, map, counter, pricing card).
5. Reveal staged: the 70 is stamped BEST CASE, then the counter drops to -18% and flips to +49.5%, the money verdict comes last.
6. Every line pulls: candidates to cut if the blind reader marks them: 5, then 3.

## Blind-reader prompts (run BEFORE voicing, and again on the rendered frame 0)
Use fresh agents with no script, no file names, no plan. Tell each: "This is the first frame of an Instagram Reel, 1080x1920. The bottom 35% is covered by Instagram's buttons and caption, so it is empty on purpose."
A. Frame-0 test (2 readers): give the frame-0 PNG and the text "Spoken in the first second: 'Seventy times more Claude Code. Not even close.'" Ask, in order, and log the answers word for word:
   1. "What is this video about? One sentence."
   2. "Would you stop scrolling? Why or why not?"
   3. "Name the apps or products you see."
   4. "Do you think the people who made this video tested the tool themselves?" (must be NO or UNSURE: if a reader says YES, the frame implies a test we did not run: fix it)
   Pass = both name Claude Code (or Claude) AND the topic (a claim about saving usage/money is false or exaggerated).
B. Hook ranking (1 reader, text only): give H1-H6 from the plan, ask for the top 3 for "clear in one second" and "would stop", one line each.
C. Build-up (1 reader): give the 10 lines in order with the on-screen card per line, ask: "At which line would you scroll away, and why?" and "After the video, what would you tell a friend?" Pass = they repeat the real finding (70 is a best case; real tests are small or negative), not the viral claim.
D. Plain-words check (1 reader who "does not code"): "Which word did you not understand?" Any word named gets replaced.
Blind readers, ep100: NOT RUN YET.

## Setup guide draft for `/e/100` (English only; for `studio/lib/articles.ts` steps[]; NOT tested by us, the page must say so)
Top of the page, plain: "We have not run Graphify ourselves. These steps come from its README (read 15.11.2026). Measure before and after on your own project."
1. Open the Terminal app (Mac: press Cmd+Space, type Terminal, press Enter; Windows: open the Start menu, type PowerShell, press Enter).
2. Check that Python 3.10 or newer is installed: type `python3 --version` and press Enter. A number like 3.12 appears. If not, install Python from python.org first.
3. Install the tool: type `uv tool install graphifyy` and press Enter. Note the two y's: other packages with similar names are not from the project. (If you do not have uv: `pipx install graphifyy` does the same.)
4. Connect it to Claude Code: type `graphify install` and press Enter. It adds a note to your Claude Code settings so Claude uses the map.
5. Optional, but this is the real test: before you use Graphify, open your project in Claude Code, ask it 3 normal questions, and write down how much usage they took.
6. In Claude Code, in your project folder, type `/graphify .` (with the space and the dot) and press Enter. Wait until it says it has finished the map.
7. Start a new Claude Code session in the same folder and ask the same 3 questions. Compare the usage with step 5.
8. If it uses MORE, remove the tool's note from your project's CLAUDE.md and uninstall it (`uv tool uninstall graphifyy`).
Before publishing the page: re-read the README live (commands, flags, uninstall), confirm how Claude Code shows usage per session today, and fill step 5/7 with the exact menu or command. `export/check_setup_guide.py` must pass.

## Risks
1. **Accuracy of line 3** (not in the verify file): re-check or use the fallback.
2. **Paraphrase of the claim** ("seventy times more Claude Code" for "up to 70x fewer tokens"): frame 0 shows the original wording, so the viewer can see what was claimed.
3. **Fairness to the project:** the reel debunks a viral number, not the tool. Line 3 grants the problem, line 5 explains the good idea; the caption says it may still help some projects. Never call the project or the creators liars. The reference creator is not named or shown (no targeting); the claim is shown as "viral posts".
4. **Implied test:** every line was written to avoid "we ran"; the stamp "tests by others, not by us" sits on beats 7-8. Blind-reader question A4 checks it.
5. **Numbers change:** star count and prices are dated 15.11.2026; re-read both on build day and update the screen and caption.
6. **Unconfirmed items kept out:** 7% test, "two days", hook bug #578 status, Reddit.
7. **Weak class:** a tool explainer/fact-check, no real AI output on screen (`why-stuck-2026-11-15.md`, point 1). Expect the explainer baseline unless we add our own measured test.
8. **Final line:** a placeholder; it must name the real next-day episode.
9. **Caption length:** measured with `wc -m` (see the caption file); run `python3 export/check_caption.py 100` and the `ig-caption` skill before shipping.
10. **Copyright:** none of the reference's sentences is reused; beat order and line types only (copying a structure is allowed, David 1.11.2026).
11. **No code on screen:** commands stay on `/e/100` unless David asks for them on the verdict card.

## Revision 15.11.2026 (David's instruction, twice): same hook and same lines as the reference reel
David asked for the reference's hook and texts, only the "comment REPO" ending replaced by "The setup's in the link in bio." Kept: hook shape and line order (claim, "$20 does $100 work", the problem, the fix, Graphify + stars, maps once, the big 70x number, the plan). Changed on purpose, because of the never-fabricate rule (verify file `channel/ref-graphify-verify-2026-11-15.md`): the claims are attributed ("They say...", "the big number ... is its best case") instead of stated as facts; one extra truthful beat (real tests: one saves a little, another uses more; the $100 plan is 5x usage, nothing we found comes close). Not copied word for word. Current lines: `video/ep100/voice/lines.txt`. Line 3 ("every new chat starts from zero") rests on Anthropic's memory docs (each session begins with a fresh context window, https://code.claude.com/docs/en/memory); "reads your files again" means on demand, not a full re-scan: UNCONFIRMED beyond that. Line 10 is a placeholder: it must name the real next episode after 100.

## BUILD-UP check on the real voice (15.11.2026, scaffold `video/ep100/out/pic-v3.mp4`, cues from `voice/narration-raw-cues.json`, word times from `voice/words.json`)
Beat list with what is NEW on screen and when (times in seconds; the same list is written by `build100.py` into `cues100.json` under `buildup`). Open question after the hook: is the claim true, and if not, what do tests show? It closes in three steps: where 70 comes from (19.2), what tests show (21.7-23.2), the money claim (24.9-28.8).
| Line | Time | What is new here | Tension |
|---|---|---|---|
| 1 | 0.00 | Frame 0: VIRAL CLAIM tag, "70x FEWER TOKENS" in quote marks, the Claude and Graphify marks, the usage bar already draining | the claim is stated, as a claim |
| 1 | 0.72 / 1.46 / 2.00 | "FREE" on the tool; on "killed" the tool plugs in and the bar refills to 100%; the names appear | the claim looks true |
| 2 | 3.98 / 4.84 / 5.18 | PRO $20 card, the "=", MAX $100 card; the word "TRUE?" appears top right | the money claim: the viewer's own plan |
| 3 | 6.49 / 8.12-9.8 | six file cards; then the Claude badge hops over them, "read x2 / x3", the bar drains to 17% | the problem is real |
| 4 | 10.58 / 11.54-13.0 | Graphify card (free, open source); the star count runs to 148.2k | it is huge: maybe the claim is real (reason to stay at about 10 s) |
| 5 | 13.72 / 15.42-16.6 | the map: nodes and links; one look-up along three links; the bar refills to 97% | the idea is good; the claim looks best here |
| 6 | 17.05 / 17.72 / 19.54 | status turns to CHECKING; the giant "70x"; BEST CASE stamp, "one example, about 52 files" | reveal 1 |
| 7 | 20.82 / 21.70 / 22.44 / 23.24 | bar shows "?"; 18% fewer; +49.5% more; issue #985 no savings | reveal 2, each row worse (about two thirds) |
| 8 | 23.66 / 24.88-25.9 / 27.10 / 28.80 | Pro bar 1x; Max bar grows to 5x; the best test as a thin slice on the Pro bar; NOT CLOSE stamp | reveal 3, the money verdict, last |
| 9 | 29.22-30.8 | the saveable card, five rows | value to keep |
| 10 | 31.22-34.96 | only the headline changes (placeholder) | FLAT, see below |
Flat stretches over 2.5 s with nothing new: **one, 31.22-34.96 (line 10)**: the card is held and only its numbers wiggle. Fix when the final line is known: show a picture of the next episode there. Longest gaps elsewhere: 2.00-3.98 (the bar and tiles move, nothing new; the hook's second half) and 25.9-27.1.
Weak beats by my own reading (not a blind reader): line 5 repeats the "problem solved" picture of line 1; line 8 is 5.5 s long and its first 1.3 s shows only the small Pro bar.
Blind reader on the beat list: NOT RUN.
