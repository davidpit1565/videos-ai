# Episode 83 script (3.11.2026, DRAFT v1, not built): "Claude Code isn't on full power"

Status: script and setup guide only. NOT produced, NOT published. Written in the lemo-opuscar test session (branch `claude/lemo-opuscar-video`).

## Product verification (live, 3.11.2026, official docs, read by WebFetch)
Source: https://code.claude.com/docs/en/model-config (section "How Claude Code sets the effort level"). Quotes as returned by the fetch tool (a small model summarised the page, so re-check the exact wording against the page before the line is final):
- Order of sources: `CLAUDE_CODE_EFFORT_LEVEL` env var, then a level picked in the session (`/effort`, `/model` picker), then `--effort` at launch, then saved settings, then the model default.
- Model default: "`high` on every model that supports effort, except that Opus 5.5, Sonnet 5.5, and Haiku 5.5 default to `medium` and Opus 4.7 defaults to `xhigh`."
- "Opus 5.5 starts at `medium` unless one of the sources above sets a level for it, and a top-level `effortLevel` in your user settings file doesn't count for Opus 5.5."
- `/effort` with no argument opens a slider; `/effort <level>` sets it; `/effort auto` clears the saved level for the active model.
- Levels for Opus 5.5: low, medium, high, xhigh, max. In the slider, Enter saves the level as the default for later sessions and `s` applies it to this session only.
- `max`: "applies to the current session only" unless set through the env var; docs say it "may show diminishing returns and is prone to overthinking".
- Platform docs (platform.claude.com/docs/en/build-with-claude/effort) list claude-opus-5-5 as a supported model; the Messages API default there was not read in full (page too long, saved locally), so the script claims only the Claude Code default.
- David's own Mac showed `medium` (env var CLAUDE_EFFORT), consistent with the docs. Not shown on screen in this draft.
UNCONFIRMED: whether the slider labels match the docs wording on the current Claude Code build (needs a real screen recording from David's Mac or a screenshot before the on-screen UI is drawn). Third-party blogs agreed on "medium" but are not used as sources.

## Why this topic (data, honest)
- `channel/demand-report.md`: "claude code tutorial beginners" is a measured high-demand keyword (159,426 median monthly searches in that report's table, row 17). Effort is a sub-topic of that cluster; **demand for "effort" itself was NOT measured**. This is an inference, labelled as such.
- It continues 82 (the postmortem said the Claude Code default effort was changed from high to medium in March for older models) without accusing anyone: this episode is only "what is the setting right now and how do you change it".
- Fits the "utility artifact" pattern the channel confirmed for saves (a setting the viewer can change in 10 seconds), not a reveal-only episode.
- Audience risk: Claude Code users are a subgroup. The hook has to explain it in the same breath (CLAUDE.md "understandable to anyone from second one"). Open question for David: is the subgroup acceptable, or does the next topic need to be broader.

## Hook candidates (type: stakes + checkable fact; last logged type was 82's accusation hook, so no repeat). Dry-sentence test is mine, not David's ear.
A. `Your Claude Code isn't on full power!` (subject in words 1-3, stake in words 4-6; "power" is plain; true: max is the top level, default is lower)
B. `Claude Code starts on medium effort.` (more exact, flatter: probably fails the dry-sentence test)
Chosen for the draft: A. Hypothesis, no evidence it beats B. Log type and 72-hour readings in content-memory.md after it ships.

## Spoken lines (target 28-35 s)
1. Your Claude Code isn't on full power!
2. Claude Code is the AI that writes code for you. (explains the product in the same breath)
3. With the Opus 5.5 model, it starts on medium effort.
4. Type slash effort.
5. A slider opens: low, medium, high, extra high, and max.
6. High is for bugs. Max is for the hardest problems, and it can overdo it.
7. Press Enter to keep your pick for next time.
8. Did you know it was on medium? Tell me below.
9. The setup's in the link in bio. (locked line, second to last)
10. TOMORROW LINE: NOT WRITTEN. Rule says the last line names tomorrow's episode, so episode 84 must be chosen from the data and verified first. David's decision, see PR description.

Voice lint still to run (`audio/script_lint.py --cues`). Words I expect to flag or avoid: "overthink" (TH, replaced by "overdo it"), "three"/"Anthropic" (not used), "effort" (check), "slider" (-ER ending), "problems" (82 reworded it), "extra" (check). Reword, do not fight the voice.

## Setup guide for /e/83 (English interface labels only, no Hebrew; goes into studio/lib/articles.ts only if the episode is built)
1. Open your terminal and type `claude`, then press Enter. Claude Code opens.
2. Type `/effort` and press Enter. A slider with the levels low, medium, high, xhigh and max appears. The level you are on right now is the one it starts on.
3. Move to the level you want with the arrow keys. (Optional, for hard bugs: high. Max is for the hardest problems and may overdo it.)
4. Press Enter to save that level as your default for later sessions, or press `s` to use it for this session only.
5. Optional: start one session at a set level with `claude --effort high`.
6. Optional: to make a level permanent for every session, set the `CLAUDE_CODE_EFFORT_LEVEL` variable to a level name. Set it to `auto` to go back to the model default.
7. Note: `/effort auto` clears the level you saved for the model you are using.
Check before shipping: steps 2-4 against a real Claude Code screen (UNCONFIRMED UI wording), and the "Enter saves / s this session" detail, which comes from the docs text only.

## Visuals (when built)
Light fixed identity, Claude orange accent, real Claude mark from the product's brand page (never redrawn from memory, CLAUDE.md logo rule), the real `/effort` slider screen recording from David's Mac if he sends one, otherwise a drawn terminal labelled "re-created". Nothing may cover the slider.
