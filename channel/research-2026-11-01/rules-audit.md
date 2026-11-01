# CLAUDE.md rules audit (1.11.2026)

Scope: `CLAUDE.md` (540 lines, 47,768 bytes) read in full; checked against `SUNDAY.md`, `NEXT_SESSION_PROMPT.md`, `channel/content-memory.md`, `channel/experiments.md`, `channel/hooks-guide.md`, `channel/episode-81-plan.md`, `channel/episode-81-v6-script.md`, `channel/style-research-31-10.md`. CLAUDE.md was NOT edited. Proposed replacement: `CLAUDE.proposed.md` (13,412 bytes, 28% of current). Everything moved out is in `rules-history.md`.

Method rule: nothing is marked OBSOLETE unless a dated David decision or a dated practice contradicts it. Where only practice (not a stated decision) contradicts, status is CONFLICT and the question is in ASK DAVID. Line numbers refer to current CLAUDE.md.

## What David actually decided on 1.11 (evidence base, all FACT from the files)
- `episode-81-plan.md`, section "David's decisions 1.11.2026 (night of 31.10)": no real screen recording for 81, chat drawn in our UI with the exact real words, labelled "Re-created from my real test, same words"; "overrides the 28.10 'do not draw ChatGPT's answer' rule for this episode only"; look closest to the grey/light style samples; wants a persistent moving figure behind everything.
- `SUNDAY.md` 1.11 (night entry): "David liked the green colour (the light 'works' version with lime)", dark ChatGPT version, ChatGPT-logo wheels, his messages in blue; not decided: fixed identity "instead of a different colour every episode", success = 5,000-10,000 views.
- `episode-81-v6-script.md`: "David's decisions: no chat demo, no closing line, fix early, hook without the swear word"; structure of Dan Martell's reel with our own text; cut 25.3 s; "check.sh / produce.sh / safe_check / qa.py were NOT run on this cut".
- `content-memory.md` 1.11 "episode 81 final cut" and `experiments.md` "Episode 81 final cut": hook changed by David to `ChatGPT is a freaking yes-man!`; chat demo gone; closing line gone; "fix starts about 9 s in"; recorded as a TEST ("does a copied viral STRUCTURE ... beat our own built scripts"), not as a new standing rule.
- `CLAUDE.md` line 230 already carries the 1.11 smooth-motion rule and "Colour stays light (the approved light + lime base) unless he says otherwise".
Important limit: the 81 decisions are written as decisions for episode 81 or as tests. David has not, in any file I read, said they replace the older rules for all videos. Hence most older rules are CONFLICT + ASK, not OBSOLETE.

## 1. Rule table

Status key: KEEP-EVERY-VIDEO, KEEP-SITUATIONAL, OBSOLETE, CONFLICT, DUPLICATE. "Proposed" = what the new file does.

| ID | Rule (one line) | Line | Date / source | Status | Evidence / note | Proposed |
|---|---|---|---|---|---|---|
| R01 | Answer in Hebrew; content English (4-5/wk) + Flemish (1/wk) | 9 | undated | KEEP-EVERY-VIDEO | | kept |
| R02 | Explain via `explain-steps`, chat labels in both languages | 11 | undated | KEEP-EVERY-VIDEO | | kept |
| R03 | Say the honest thing once, then work | 15 | undated | KEEP-EVERY-VIDEO | | kept |
| R04 | Tell him to switch to Sonnet 5 before mechanical work | 18-32 | "he asked to be reminded", data 21.8 | KEEP-EVERY-VIDEO | Model name now "Sonnet 5.5" in this session; proposed says "the cheaper Sonnet tier". Wording change only. | condensed |
| R05 | `/fast` not cheaper; session length is the lever | 34-39 | 21.8 | KEEP-EVERY-VIDEO | | condensed |
| R06 | Hebrew session-handoff section | 41-42 | 25.10, David | KEEP-EVERY-VIDEO | Required verbatim | copied verbatim (checked by script) |
| R07 | Never fabricate; ASSUMPTION label; unconfirmed listed | 46 | undated | KEEP-EVERY-VIDEO | Hard safety rule | kept |
| R08 | Verify the product live before any script | 49-56 | ep 18 | KEEP-EVERY-VIDEO | Hard rule; story to history | kept, story moved |
| R09 | Real logo/icon of every named product, whichever style | 57-70 | 30.9, David | KEEP-EVERY-VIDEO | Ep 81 uses ChatGPT-logo wheels (SUNDAY 1.11). The clause "get a real screenshot rather than an AI stand-in" conflicts with 81's re-created chat (see R28); that clause moved to history | kept without the screenshot clause |
| R10 | Logo badge = icon only, no caption | 71-79 | 5.10, David | KEEP-EVERY-VIDEO | 55-57 retro-fix note is history | kept |
| R11 | Measure, don't guess; ear wins, disagreement written down | 80 | undated | KEEP-EVERY-VIDEO | | kept |
| R12 | Topic chosen from demand data + content memory, not fresh (from ep 25) | 83-92 | 5.9 | CONFLICT | `experiments.md` "Episode 81 final cut": script copied a known creator's structure "instead of our own data-built script", David's decision (1.11); `episode-81-plan.md`: "the hook must come from the result, not the keyword". Test, not stated replacement. | kept, flagged [ASK 7] |
| R13 | Secrets only in Vercel env vars; publication id public | 93 | undated | KEEP-EVERY-VIDEO | Hard rule | kept, widened to "never in chat/git/files/logs" (as in the PIN rule) |
| R14 | Nothing ships untested silently | 95 | undated | KEEP-EVERY-VIDEO | Hard rule | kept, plus "measured not heard" |
| R15 | Full English setup path on `/e/N`, enforced by `check_setup_guide.py`; no Hebrew on visitor pages | 97-108 | 2.9; 16.10 | KEEP-EVERY-VIDEO | `/e/81` exists with the text per SUNDAY/plan | kept |
| R16 | Run `viral-hook-lab` on every opening line; log hook type and 72 h readings | 109 | 20.10 | KEEP-EVERY-VIDEO | 81 logged in content-memory | kept |
| R17 | Read `hooks-guide.md`; never the same hook type twice in a row | 110-118 | 2.9 | CONFLICT | `episode-81-plan.md` v2: "Rule conflict, decided here for David to confirm"; `NEXT_SESSION_PROMPT.md` open item 2: "rule 'not same hook type twice' vs a series: not yet decided". hooks-guide checklist item 5 still enforces it. | read-rule kept; rotation flagged [ASK 6] |
| R18 | Viewer must FEEL the problem in 3 s | 119-128 | 30.9, David | KEEP-EVERY-VIDEO | | kept |
| R19 | Package as an everyday thing already happening to the viewer, AI inside | 129-140 | 6.10, David | KEEP-EVERY-VIDEO | CLAUDE.md itself says "working direction, not a confirmed pattern"; proposed keeps that label | kept, labelled |
| R20 | Understandable to anyone from second one | 141-151 | 24.9, David | KEEP-EVERY-VIDEO | Superseded in strictness by the 8-year-old test (R20b) | merged with R20b and R50 |
| R20b | 8-year-old test on every line; no idioms; cave/fold -> "say yes" | not in CLAUDE.md | 31.10, David via Miki, `hooks-guide.md` line 548 | KEEP-EVERY-VIDEO (MISSING from CLAUDE.md) | | added |
| R20c | Hook: product and claim in the first three words | not in CLAUDE.md | 28.10, David, `hooks-guide.md` (PR #500), SUNDAY 28.10 | KEEP-EVERY-VIDEO (MISSING) | | added |
| R21 | Voice profile exaggeration 0.50, cfg 0.30 | 155-156 | undated | CONFLICT | Line 227 (18.10): exaggeration about 0.78; `NEXT_SESSION_PROMPT.md` step 4 uses 0.72. Both are true at different layers (default vs per-episode). | rewritten as default + per-episode range |
| R22 | `script_lint.py --cues` before narration; word endings; swap words | 157-159 | undated | KEEP-EVERY-VIDEO | SUNDAY 30.10 adds: end lines on hard consonants | kept |
| R23 | Flagged lines via `line_doctor.py`; locked takes in `canonical-lines.json` | 160-167 | undated | KEEP-EVERY-VIDEO (mechanism) | The locked "link in bio" content is R24b | kept, mechanism only |
| R24 | Final line names tomorrow's episode; episode N+1 scripted before N ships | 168-188 | 6.10, David | CONFLICT | Practice: ep 76 ended "Follow for the setup that actually works." (SUNDAY 26.10), ep 77 "Next, I'll show you..." (`episode-77-script.md`), ep 80 uses both locked lines with no promise, ep 81 has no closing line (v6 script: "no closing line"; hook log: "no tomorrow line: no episode 82 yet"). Rule is applied only when a next episode exists, and 81 drops it entirely. | flagged [ASK 5]; the "never promise a non-existent episode" part kept |
| R24b | Locked "The setup's in the link in bio." second to last | 164, 185 | undated / 6.10 | CONFLICT | 81 v6 script: "no closing line" | flagged [ASK 5] |
| R25 | Both closing-CTA scenes share one per-episode photo; "open, not designed" | 189-209 | 30.9 / 1.10 | CONFLICT | No closing line in 81 and no photos (see R49); open design item still listed `NEXT_SESSION_PROMPT.md` 6.3 | moved to history; [ASK 4, 5] |
| R26 | Repeated photo scene holds Ken Burns static | 210-217 | 1.10, David | KEEP-SITUATIONAL | Only applies to photo-composite builds | history |
| R27 | `speak_language.py` / Flemish needs reference recording | 218-219 | undated | KEEP-SITUATIONAL | Flemish weekly | kept one line |
| R28 | v4 standard: real motion from the real screen recording at natural speed (`data-rt/dl`) | 224 | 18.10, David (ep 71 v4) | CONFLICT | `episode-81-plan.md` (31.10 night): "No real screen recording for 81 ... for this episode only". Final cut has no chat demo at all. David called v4 the direction for "all future videos". | situational if a recording exists; flagged [ASK 3] |
| R29 | Start on the proof: first frame shows the key state | 225 | 18.10 | KEEP-EVERY-VIDEO | Generalised (stake/action from frame 0, 79 v3 practice) | kept, generalised |
| R30 | Short punchy lines, exclamation beats on hook; reword swallowed words | 226 | 18.10 | KEEP-EVERY-VIDEO | 81 hook `...yes-man!` fits | kept |
| R31 | Voice exaggeration about 0.78, re-roll at 0.64 on flagged lines | 227 | 18.10 | KEEP-EVERY-VIDEO | See R21 | merged into R21 |
| R32 | Energetic music from real library (69 tracks), `FORCE_TRACK` | 228 | 18.10 | KEEP-EVERY-VIDEO | | merged with R52 |
| R33 | Nothing we add covers what the screen shows; handle dropped on full-bleed screen episodes | 229 | 18.10, David | KEEP-EVERY-VIDEO (principle) | "Handle dropped" part is situational (full-bleed screen) | principle kept, handle exception kept |
| R34 | Motion smooth, never robotic; colour light + lime unless he says otherwise | 230 | 1.11, David (after 81 v5) | KEEP-EVERY-VIDEO | Newest decision in file. Light+lime is in `SUNDAY.md` 1.11 as David's liking. | motion kept; colour moved to design TODO |
| R35 | Two-voice dialogue episodes: WAV resample 48 kHz mono, canonical clips, `ACCENT_SKIP` | 231 | 72 on | KEEP-SITUATIONAL | 81 has no second voice | history |
| R36 | Answer scenes: white headline bar + one ring; no moving per-word box | 232 | 21.10, David | KEEP-SITUATIONAL | Dialogue episodes only | history |
| R37 | His own photos are first-class; never from his window/home; people far or behind; face pre-check | 233 | ep 74 / 21.10 | KEEP-EVERY-VIDEO (privacy part) | Safety rule | kept in Privacy bullet |
| R38 | Verify a number on screen before it goes in a script | 234 | ep 74 | KEEP-EVERY-VIDEO | Folded into never-fabricate | merged into R07 |
| R39 | Container suspends when a turn ends; keep loops resumable | 235 | undated | KEEP-SITUATIONAL | Duplicated in SUNDAY/NEXT_SESSION section 5 | one line |
| R40 | Everything we build becomes an episode, same-day angle | 237-247 | undated | KEEP-EVERY-VIDEO | "Already shipped ... nothing queued as of episode 24" is stale (now ep 81) | kept, stale list to history |
| R40b | `/skills`, `/prompts` public pages removed | 249-257 | 28.9, David | KEEP-SITUATIONAL | History | one line |
| R41 | Content memory: two files, weekly loop, FACT/HYPOTHESIS/UNKNOWN, no numeric score; Confirmed after two episodes | 259-284 | undated | KEEP-EVERY-VIDEO | "12 published episodes is not enough volume" is stale | kept, stale clause dropped |
| R42 | Merge, don't just push; Studio shows only `main` | 288-295 | undated, "said more than once" | KEEP-EVERY-VIDEO | | kept |
| R43 | Merging is not shipping: verify deploy and file size | 296-304 | 21.10 | KEEP-EVERY-VIDEO | SUNDAY 1.11: builds also fail when DB unreachable (deleted Supabase project); added one line | kept + 1 line; commit list to history |
| R44 | Standing authorization: do not re-ask approved directions | 305-314 | 30.9, David | KEEP-EVERY-VIDEO | | kept |
| R45 | Accent colour must suit the episode and its photos; not same colour twice in 7 days; `produce.sh` design-variety check | 315-334 | 30.9, David | CONFLICT | `style-research-31-10.md` "Decisions waiting": "One fixed visual identity for the series (this replaces the 'different colour every episode' variety check)"; `SUNDAY.md` 1.11: undecided; line 230 of CLAUDE.md itself says light + lime. If identity is fixed, `produce.sh` design-variety check will FAIL on the same colour (code change needed). | moved to history; [ASK 1] |
| R46 | `produce.sh` is the one pipeline entry point; no third pipeline | 335-339 | undated | KEEP-EVERY-VIDEO | SUNDAY 1.11: HyperFrames build "not connected to produce.sh and its gates: a published video must pass them"; 81 v6 script says gates were not run and 81 was published 1.11 16:35 UTC (`content-memory.md`) | kept, flagged [ASK 10] |
| R47 | Real handle is `@actually_works.ai` with underscore | 340-343 | undated | KEEP-EVERY-VIDEO | | kept |
| R48 | Picture follows narration; `retime.py`; `--fit` only for fixed cut | 344-347 | ep 02 | KEEP-SITUATIONAL | HTML pipeline | one line |
| R49 | Motion-recipes: six recipes, `motion-kit.js`, templates | 348-376 | 1.10, David approved one by one | KEEP-SITUATIONAL | Template-specific; "recipes 1-3 not shipped yet" stale; 81 is HyperFrames | history, pointer to `channel/motion-recipes.md` |
| R50 | Every episode uses real photo backgrounds (`reel-template-photo.html`), source via Unsplash/Pinterest, save as `ep<N>-scene-*.jpg`, face pre-check, `safe_check` | 377-399 | 1.10, David | CONFLICT | Ep 81 look: light + lime, drawn UI, phone frame, logo wheels (`content-memory.md` 1.11 hook log; plan "Look"); v4 episodes were real screen recordings (R28). No file says the photo rule was cancelled. Safe-area and privacy parts survive elsewhere. | moved to history; [ASK 4] |
| R51 | Plain, natural spoken language | 400-411 | 1.10, David | DUPLICATE | Of R20/R20b, strengthened by the 8-year-old test | merged |
| R52 | Render with `FRAMES=1 render.sh` | 412-413 | undated | KEEP-SITUATIONAL | HTML pipeline; HyperFrames renders differently | kept one line |
| R53 | Music only from licensed library, never `build_music.py`; `check_music_bed.py`; last positional arg; regenerate on length change | 414-440 | repeated, three incidents | KEEP-EVERY-VIDEO | Third incident list to history | kept, condensed |
| R54 | `voice_doctor.py` before delivery; `BAD` blocks | 441-443 | undated | KEEP-EVERY-VIDEO | | kept |
| R55 | Long cut stays on recorded path (24,000 screenshots) | 444 | undated | KEEP-SITUATIONAL | No long cuts in current series; no reference found after Oct | history |
| R56 | Verify sync via brass flash cards | 445-446 | undated | KEEP-SITUATIONAL | Legacy template (brass); not applicable to light+lime | history |
| R57 | Safe area numbers (top 14%, bottom 35%, sides 6%) | 448-454 | undated | KEEP-EVERY-VIDEO | Measured | kept |
| R58 | `safe_check.js`; `data-decor` | 456-461 | undated | KEEP-EVERY-VIDEO | | kept |
| R59 | Word-by-word captions, lit in brass, 2-3 word chunks | 462-466 | undated | CONFLICT (minor) | "brass" vs 1.11 lime identity; word-by-word kept, colour = series accent | kept, colour generalised |
| R60 | Master -14 LUFS/-1 dBTP; music 18-20 dB under voice | 467-468 | undated | CONFLICT (minor) | 21.10 rule measures music at about -6 to -18 dB under in the 300-3500 Hz band; two different measurements | both stated |
| R61 | Length 45-75 s; not under 30 s | 469-470 | undated, based on Buffer/Socialinsider | CONFLICT (strong) | `experiments.md` 8.10: David "if you think it's better, do it" (62 short test, rule explicitly NOT changed: "a test, not a rule change"); ep 80 about 40 s; ep 81 final cut 25.3 s by David's decision (v6 script, experiments.md); "do not go under 30 s" is directly violated | rule replaced by "per episode" + [ASK 2] |
| R62 | `check.sh` must pass before anything goes to him | 474-487 | undated | KEEP-EVERY-VIDEO | See R46 | kept |
| R63 | `voice_quality.py` on every episode | 489 | 21.10, David | KEEP-EVERY-VIDEO | | kept |
| R64 | Check, fix, re-check whole | 491-497 | ep 18 | KEEP-EVERY-VIDEO | | kept |
| R65 | Watch the rendered file twice | 499-507 | ep 25 | KEEP-EVERY-VIDEO | | kept |
| R66 | Studio: Next.js on Vercel, branch deploys off, never redeploy old deployment | 511-515 | undated | KEEP-SITUATIONAL | Studio work only | condensed |
| R67 | Vercel "Skip deployments" toggle story | 516-524 | 3-4.9 | KEEP-SITUATIONAL | Diagnostic tip | one line, story to history |
| R68 | `/api/track` daily | 525 | undated | KEEP-SITUATIONAL | | one line |
| R69 | Public routes declared once in `routes.ts`; `check:routes` | 526-531 | undated | KEEP-SITUATIONAL | | one line |
| R70 | Site English LTR; studio Hebrew RTL island | 532-534 | 16.10 (no Hebrew on site) | KEEP-SITUATIONAL | | one line |
| R71 | Phone notification (PushNotification) when a reel is ready | 536-537 | 25.10, David | KEEP-EVERY-VIDEO | Required verbatim | copied verbatim (checked) |
| R72 | Claude may read the studio with the PIN given in this session | 539-540 | 25.10, David | KEEP-EVERY-VIDEO | Required verbatim; PIN never stored | copied verbatim (checked) |
| R73 | Header: David 18, Flemish Belgium, employed elsewhere | 3-5 | undated | CONFLICT | `SUNDAY.md` section 5.5: repo `davidpit1565/videos-ai` is public, CLAUDE.md "details age, location and workplace"; recommendation to make private, "waiting for a decision" | kept as is; [ASK 9] |
| R74 | Success bar 5,000-10,000 views per reel | not in CLAUDE.md | 31.10, David, `style-research-31-10.md` item 5; NEXT_SESSION 31.10 | KEEP-EVERY-VIDEO (MISSING) | | added |

Count: 78 rows (R20b, R20c, R24b, R40b added). Merged/duplicated: R20/R20b/R51, R21/R31, R32/R53, R37/R38. OBSOLETE count: 0 by the strict method (no rule was explicitly cancelled by David in any file); R61 and R45 are the closest and are marked CONFLICT (strong).

## 2. What the proposal changes (every change with source)
1. Removed to history, content unchanged: stories behind R08, R09 (screenshot clause), R10, R25, R26, R35, R36, R40 list, R43 failed-deploy hashes, R45, R49, R50, R53 incident list, R55, R56, R67.
2. Added: R20b (8-year-old test; `hooks-guide.md` 548), R20c (three-word rule; `hooks-guide.md`, SUNDAY 28.10), R74 (success bar; `style-research-31-10.md`).
3. Rewritten, not just trimmed: R21+R31 (default vs per-episode exaggeration: CLAUDE.md 155 vs 227, NEXT_SESSION step 4), R61 (length, per `experiments.md` 8.10 and 81 final cut), R59/R60 (colour and measurement wording).
4. Kept with `[ASK n]` marker (decision belongs to David): R12, R17, R24, R24b, R25, R28, R45, R46, R50, R61, R73.
5. Not changed: R06, R71, R72 (verbatim, verified programmatically), all never-fabricate/secrets/privacy rules.
6. Sync note: `SUNDAY.md` line 36 lists one more David rule from 28-30.10 that is in no rule file: "send files to the phone as downloadable files (the embedded view is silenced)". I left it out of the proposal as tooling, not a video rule. Also "do not draw ChatGPT's answer, only real recordings" (28-30.10) is overridden for 81 only (plan, 31.10 night): see [ASK 3].
7. Outside CLAUDE.md, same drift noticed (not edited): `hooks-guide.md` checklist item 5 still enforces hook-type rotation; `export/produce.sh` design-variety check still fails on a repeated colour (conflicts with a fixed identity if David says yes to ASK 1).

## 3. ASK DAVID (yes/no, in Hebrew when asked)
1. Is the light + lime look the fixed identity for ALL future episodes (replacing "a different colour each episode")? If yes, the design-variety check in `produce.sh` must be switched off or changed.
2. Are the old length rules (45-75 s, "not under 30 s") retired, so each episode is as short as it needs to be (81 is 25 s, the fix within about 10 s)?
3. From now on is the default a drawn chat re-created with the exact real words and an on-screen "re-created" label, instead of a real screen recording (this replaces the v4 standard and the 28.10 "do not draw ChatGPT's answer" rule)?
4. Is the standing rule "every episode uses real photo backgrounds" (1.10) retired for the new series?
5. Is the closing dropped for every episode (no "The setup's in the link in bio.", no tomorrow-line), or only when no next episode exists?
6. Should the rule "never the same hook type two episodes in a row" be dropped (the series now repeats one format)?
7. May a topic also come from copying a proven viral structure with our own text (as in 81), instead of only from `demand-report.md` and content-memory?
8. Is "no swear words in hooks" a standing rule for all hooks (81 uses the milder "freaking"; his note says "hook without the swear word")?
9. Should age, workplace and city be removed from `CLAUDE.md`, since the repo is public (open since `SUNDAY.md` section 5)?
10. Must every video made with HyperFrames also pass `export/produce.sh` and `check.sh` before it is published (81 was published with those gates marked not run)?
