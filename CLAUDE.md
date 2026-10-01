# Actually Works — how this repo works

An AI-content channel and an AI-services business, run by David: 18, based in Flemish
Belgium, employed elsewhere and building this alongside. Two engines, and the paid one feeds
the free one — the full reasoning is in `plan/business-model.html`.

## Talking to him

- **He writes Hebrew, the videos are English.** Answer in Hebrew. Content, captions and
  scripts are English (4–5 a week) plus Flemish (1 a week, for clients).
- **Explain by the `explain-steps` skill.** Numbered clicks, interface labels in both
  languages, the boring path over the clever one, optional steps marked as optional. When he
  says he did not understand, the step assumed something — replace the route, do not repeat
  it louder.
- **Say the honest thing once, then do the work.** He acts on straight answers; he has
  redirected several times when told a plan would not hold.

## Say it out loud when the work turns mechanical

He asked to be reminded, so this is the reminder and it is not optional: **when a stretch of
work is mechanical, tell him to switch to Sonnet 5 for it — before starting, in one line.**

Mechanical means the answer is already decided and what remains is execution: writing an
episode script from the slate's template, publishing, caption edits, doc updates, running a
build and reporting the number, renaming things. Sonnet 5 is roughly 2.5x cheaper and the
difference does not show on that work.

Keep Opus for the opposite: debugging, architecture calls, and anything where being wrong
costs him a day. The three most expensive catches on 21.8 were all of that kind — a metric
that measured position instead of a phoneme, a check that ran before the transform it was
protecting against, and a diagnostic asserting the presence of a variable that was absent.
None was caught by a tool.

Two things he should not be told to do, because they do not help: `/fast` is Opus with faster
output, not a cheaper tier; and switching mid-session does not reclaim what the session
already accumulated. **The bigger lever is session length** — on 21.8 a three-day session had
read 194M cached tokens against 572k actually written, a factor of 340. A fresh session
pointed at `SUNDAY.md` costs far less than a tier change. Say that too, when a session has
been running for days.

## Rules that do not bend

- **Never fabricate.** No invented clients, testimonials, results, prices or metrics. If a
  number is an assumption, it says ASSUMPTION next to it. If research could not confirm
  something, it is listed as unconfirmed, not smoothed over.
- **Before writing any script, verify the product is still real — every time, automatically,
  not just when something feels off.** Episode 18 was first built around "ChatGPT agent
  mode," a name OpenAI had already retired days earlier in favor of "ChatGPT Work" — caught
  before shipping, but only because it got checked, not because checking was already the
  default. AI-tool features and names change fast enough that a script written from memory
  or an old episode's assumptions can be stale within weeks. A live web search for the
  current name, current behavior and current limits comes before the first line is written,
  not after a version is already built.
- **Every app, site, or product an episode names gets its real logo or icon on screen —
  standing, every episode, whichever visual style it uses.** Decided 30.9.2026, David's
  direct instruction, pointing at episode 52's real ChatGPT icon as the example: a small
  detail, but it visibly lifted that episode and should not have been situational — it
  applies every time a script names something with a real, findable brand mark, not just
  when it happens to come up. This holds whether or not the episode uses background
  screenshots or real-photo compositing — a fully synthetic scene still gets the real logo,
  not a drawn stand-in. Sourcing is not guesswork: search the web and pull the actual current
  logo/icon (official site, Wikimedia Commons, the product's own press/brand page) the same
  way episode 52's ChatGPT SVG was sourced — never invent, redraw, or approximate a brand
  mark from memory. When a real product screenshot is the more natural fit than a logo alone
  (showing an actual interface, not just naming a brand), get that screenshot directly —
  live web search, open the real page or app, capture the actual screen — rather than
  treating a generic AI-generated stand-in as good enough.
- **Measure, don't guess.** Demand comes from real view counts (`channel/demand-report.md`),
  voice decisions from measurement *and* his ear — and when they disagree, his ear wins and
  the disagreement gets written down.
- **Every episode's topic is chosen from the data, not picked fresh each time — standing
  from episode 25 on.** Before writing a script: check `channel/demand-report.md` for
  measured search demand, `content-memory.md` for which past hooks/formats actually
  performed (the studio's real view counts, per-episode), and pick the highest-demand,
  best-fitting angle that hasn't already been covered from that exact angle — not just
  "what sounds interesting." Decided 5.9.2026 after episode 2 (agent-vs-chatbot,
  623 views) and episode 7 (n8n agent reliability, 372 views) turned out to be the two
  strongest performers by a wide margin, both landing on the single highest-demand
  keyword in the report ("n8n ai agent tutorial," 233k median monthly searches) — the
  data already pointed at the next topic before anyone had to guess at one.
- **Secrets live only in Vercel environment variables.** Never in chat, never in git. The
  publication id is public; the API key is not.
- **Nothing ships untested silently.** If something was built but not run — the n8n workflow,
  for instance — the file says so in plain language.
- **Every episode ships with a full, exact setup path the viewer can actually follow —
  standing, not optional, from episode 21 on.** Decided 2.9.2026, alongside choosing the
  "live test / escalate until it breaks" format for episode 21: watching isn't enough, a
  viewer has to be able to install or replicate whatever the episode shows on their own
  side by the end of it. Write it per `explain-steps` — numbered clicks, interface labels in
  both languages, the boring path, what happens after each step — and it goes on the
  episode's own site page (`/e/N`), not just spoken narration a viewer can't pause and
  copy from. Applies to every future reel/episode, whichever content pattern it uses.
  Enforced, not just written down: `export/produce.sh` runs `export/check_setup_guide.py`
  before shipping and refuses to ship an episode with no `studio/lib/articles.ts` entry, or
  one whose `steps[]` is missing or placeholder-thin — a caption existing was already a hard
  stop for the same reason, this closes the matching gap for the setup guide itself.
- **Read `channel/hooks-guide.md` before writing any episode's opening line. Never repeat
  the same hook type two episodes in a row, and never ship a hook that only passes the
  "dry-sentence test" by accident.** Decided 2.9.2026, after he flagged twice, in the same
  day, that the opening line kept reading as a flat, informational sentence — even after a
  type-rotation fix, the replacement line still failed on tone. A hook is not just a true,
  on-topic first sentence: it has to create real pull (fear, identity, stakes, curiosity),
  not just state a fact. `hooks-guide.md` has the sourced taxonomy, the dry-sentence test
  itself, a log of which type each recent episode used, and the two rejected drafts that
  failed this exact check — read those before assuming a new draft clears the bar.
- **The viewer has to feel the problem in the first 3 seconds, not just understand it.**
  Decided 30.9.2026, David's own words: understanding a claim intellectually is not the
  same as feeling it — the hook has to land as something the viewer recognizes happening
  to their own body/life/people they care about, right away, or there's no real reason not
  to keep scrolling. This is the actual mechanism behind "create real pull" in the rule
  above and the "sendability" test elsewhere in this file: a viewer who feels the problem
  is the one who stops, watches for the solution, and is the one who forwards it to a
  specific person it could actually happen to. Check every hook against this before
  assuming a checkable-fact opener (per the "500+ club" finding) is automatically enough —
  a checkable fact that doesn't land in the gut still isn't a strong hook.
- **Every episode must be fully understandable, to literally anyone, from the first second
  — not just to a viewer already into AI, and not only by the time the video ends.**
  Decided 24.9.2026, David's own words: this applies to every future video from now on, not
  just one episode. The hook itself has to carry enough plain-language context that someone
  with zero prior exposure to the topic, the company, or AI in general immediately knows
  what's being claimed — a named feature or product gets explained in the same breath it's
  named, never assumed familiar. This is a stricter, standing version of the comprehension
  check already described in `hooks-guide.md`'s dry-sentence test: check the *entire* script
  against it, not just the opening line, and check it from second one, not "does it resolve
  by the end." A script that only makes sense in hindsight, or only to a technical/AI-literate
  viewer, fails this regardless of how strong its hook or claim otherwise is.

## The voice

- Profile: `audio/voice/profile/` — reference chosen by his ear, settings locked in
  `profile.json` (exaggeration 0.50, cfg 0.30).
- **Run `python3 audio/script_lint.py --cues <build>` before generating narration.** His
  voice softens word endings — unstressed -ER, -LE/-BLE, -LY, R plus a cluster, flapped T.
  Swap the word; respellings were measured and do not help.
- A line he flags goes through `audio/line_doctor.py`, which ranks candidates by the energy
  left in the last 90 ms of the target word. The approved take is genuinely locked per
  line — `audio/voice/profile/canonical-lines.json` maps a line's exact text to a
  pre-polished clip, and `build_voice.py` loads that clip byte-for-byte instead of
  regenerating, for every episode. Both closing lines ("Follow for the setup that
  actually works." and "The setup's in the link in bio.") are locked this way already —
  add a new line to the manifest the same way once he approves a take for it.
- **Standing order for the two locked closing lines, every episode: "The setup's in the
  link in bio." always comes second-to-last, "Follow for the setup that actually works."
  is always the true final line.** Confirmed from episodes 49/51/52/53; episode 54 first
  shipped with these reversed — a real bug, caught by David watching the picture, not by
  any automated check. Verify the CUES order and the matching scene text before shipping,
  the same way the handle text gets checked against this file rather than the last episode.
- **The two closing-CTA scenes always share ONE locked background photo — but that
  photo is chosen per episode, from that episode's own real photos (or newly
  sourced to fit), never a single file hardcoded across every future episode.**
  Decided 30.9.2026 after episode 54 first shipped with its ending repeating one
  scene's photo three times running — fixed first with a dedicated cross-episode
  asset (`channel/assets/canon-closing-photo.png`), which David then corrected
  (1.10.2026, his own words): a fixed file reused identically forever is "the same
  thing, not according to the video" — the two closing scenes must still read as
  this episode's own ending, not a franchise slate. Episode 54 now points its
  closing scenes straight at its own `ep54-scene-a-videocall.png` (the same photo
  scene 1 opens on — a deliberate bookend, not a leftover default); the canon file
  was removed. Pick a fitting photo per episode, lock it across both closing
  scenes (still static Ken Burns per the rule below — they're one continuous shot),
  and never repeat whatever an earlier scene in that same episode already used.
- **A photo-composite scene reusing the SAME photo file as the scene right before it holds
  Ken Burns fully static (scale 1.00, no pan) — never re-zoom/re-pan on a photo that never
  actually changed.** Decided 1.10.2026, David's own words after watching episode 54's
  picture a second time: a second independent Ken Burns animation on an unchanged photo
  reads as the photo resetting/jumping, not continuing — confirmed on episode 54's two
  repeated-photo pairs (scenes 2→3 and 5→6, both reusing the same file back to back) before
  fixing it. Only a scene whose photo is actually new relative to the one before it gets its
  own entrance motion.
- `audio/speak_language.py` does the same voice in 23 languages. Flemish needs its own
  reference recording — `record/flemish-script.md`.

## Standing rule: everything we build becomes an episode

He said it plainly — every skill, agent, or tool we develop here is itself content. When a
new one is finished, add it to the idea list in the studio with the angle already written:
what it does, the one screen that proves it, and the number that makes it real. Nothing gets
built and quietly filed.

Already shipped this way: `explain-steps` (its own content post), `voice_doctor.py`
(episode 11), and `retime.py` (episode 24 — "Editors squeeze the picture to fit the audio.
We do the opposite."). Nothing currently queued and unshipped as of episode 24 — the next
tool or skill this repo builds goes on this list the same day it's finished, not after.

The public `/skills` and `/prompts` browsing pages on the site were removed (28.9.2026,
David's direct instruction): they listed every skill and prompt the repo had ever built, but
nothing kept that list current per episode, so it drifted out of sync with what was actually
still true — the same "stale content presented as current" problem the "never fabricate"
rule exists to prevent. This does not change the rule above: a new skill or tool still
becomes an episode, angle written the same day it ships. It only means there is no longer a
standing site page that browses the full list — the episode itself, not a catalogue page,
is where it gets shown. (The per-episode detail pages, `/p/[slug]` and `/s/[slug]`, are
unaffected and still serve the individual prompt/skill an episode actually points to.)

## Content memory — the weekly loop

Two files carry this, deliberately kept to two: `channel/content-memory.md` (patterns,
hypotheses, winning/losing formats) and `channel/experiments.md` (deliberate tests only —
"we changed X to test Y," never every episode). Real per-episode performance — views,
saves, save-rate, engagement — lives in the studio's own tracked state (`/api/track` pulls
it daily from Instagram and Beehiiv), not in a markdown file; `/api/agent` already answers
questions against it under the same rule as everywhere else in this repo: never invent a
metric, say plainly when there isn't enough data yet. `channel/demand-report.md` is a
separate, one-time thing — YouTube search-demand research, not live episode performance.
Don't conflate the two.

When he says "plan next week" or "what should we learn from this," do it without needing
a slash command: read `content-memory.md`, check the studio's real numbers (ask him to
paste the studio's data or a relevant `/api/agent` answer if this session can't reach it
directly), separate FACT from HYPOTHESIS from UNKNOWN, and report: what happened, what
might explain it (labeled as guesses, not conclusions), what pattern is worth repeating,
what's worth a deliberate experiment next, and what to stop doing — only if there's
actually enough evidence to say so. Update the two files with anything that changed. A
pattern moves from *Current hypotheses* to *Confirmed* only after showing up in two
independent episodes, not one good week — 12 published episodes is not enough volume to
overfit a rule to a single video.

Skip a numeric virality score (no "Hook: 9/10, Score: 87") — it fakes precision the
data doesn't support. STRONG / PROMISING / WEAK / UNCLEAR, with the reasoning stated, is
honest about what we actually know.

## Building and rendering

- **Studio production only reflects `main` — merge, don't just push.** Branch deploys are
  off (`studio/vercel.json`), so a shipped reel sitting on an open PR is invisible to him no
  matter how clean the build is. He said this directly, more than once, after builds he
  couldn't find in the studio: once `check.sh` passes clean and there is nothing left for a
  human to weigh in on, mark the PR ready and merge it — don't leave it as an unmerged draft
  waiting to be asked. This applies to episode-shipping PRs and routine site fixes alike;
  still ask first for anything that's actually a judgment call (a design direction with no
  clear right answer, a change to what an episode claims).
- **Standing authorization exists — don't re-ask for something already approved.** Said
  directly 30.9.2026, after repeated rounds of stopping mid-iteration to check in again on
  work whose direction he'd already signed off on: once he's approved a direction (a visual
  style, a fix, a feature), keep iterating and verifying it on your own — real checks, real
  screenshots, honest disclosure of what still doesn't work — without pausing each round to
  ask again. Bring it back to him only for an actual new judgment call (a real creative
  decision, a genuinely ambiguous tradeoff, something no automated check can settle) or once
  it's ready to actually ship. Don't confuse this with permission to skip disclosure — a
  found problem still gets reported plainly — it removes the need to ask "can I continue?"
  when nothing new is actually being decided.
- **An episode's accent color has to actually suit that episode's content and its real
  photos/scenes — not just avoid repeating the immediately prior episode, and not the
  same exact color twice in one week even with other episodes in between.** Decided
  30.9.2026, David's own words, after episode 54 shipped with a violet accent
  (`#9333EA`) that looked muddy and hard to read specifically against that episode's own
  warm-toned real photos — legible by the numbers, but visually wrong, and only caught
  because he looked at the actual frames, not because any automated check flagged it.
  Before locking a color: look at it rendered against every real photo/background the
  episode actually uses (photo-composite's warm skin tones read very differently than a
  cool office backdrop, and a color that pops on one can go dead on the other), not just
  its contrast ratio against the fixed text color. Pick something that suits the topic's
  actual tone too, not a rotation for its own sake. `export/produce.sh`'s design-variety
  check enforces the mechanical half of this: it still fails on an exact repeat of the
  immediately prior shipped episode's color/mood, and now separately fails if the same
  exact color appears in any *dated* `channel/used-designs.json` entry from the last 7
  days, even with a different episode in between — add a `"date"` field (`YYYY-MM-DD`,
  UTC) to every new entry going forward so that check has something to compare against;
  older undated rows are skipped, not guessed at. The check cannot judge whether a color
  actually suits the content or a given photo's tones — that part is still a real look,
  every time, not a box to check off after the fact.
- **`export/produce.sh <episode> <build.html> <duration> [accept_words] [bpm] [mood]` is the
  one pipeline entry point**, script_lint through render, gate, captions-must-exist, the
  design-variety check against the last episode's palette, and shipping the file itself to
  `studio/public/reels/`. `export/make_reel.sh` is an older, incomplete duplicate built
  without knowing this one existed — it stops before shipping. Don't build a third one.
- **The real handle is `@actually_works.ai` — with the underscore.** `channel/launch-plan.md`
  and `channel/instagram-automation.md` had it wrong (no underscore) for a while and every
  reel's on-screen `.handle` div copied that mistake. Check the handle text in any new
  build against this line, not against the last episode's file.
- The picture follows the narration, never the reverse. Build the voice at its own pace,
  then `export/retime.py <build> <cues.json> --out <build>-paced.html` moves every timing
  in the build to match. `--fit` on build_voice is only for a cut that genuinely may not
  move; using it for pacing is what produced seven overlapping lines in episode 02.
- **`channel/motion-recipes.md` has six verified motion upgrades — word-by-word builds,
  a per-word text highlight (fixes a real line-wrap bug in the naive one-box version),
  a staggered contradiction reveal, zoom-through scene transitions (every episode today
  hard-cuts between scenes with zero transition, which `hyperframes-animation`'s own
  rules call a non-negotiable gap), one GPU-tier fragment-shatter hero beat reserved
  for a single real reveal per episode, and spoken-word emphasis on a fixed headline.**
  Verified in isolated demos David approved one at a time, then extracted into a real
  shared module, `export/motion-kit.js` (`window.MotionKit`), re-verified with its own
  frame capture. **`video/reel-template.html`** is the real starter build to copy for a
  new synthetic-style episode — recipes 1-3 (hook word-by-word, quote highlight,
  scoreboard stagger) and recipe 4 (zoom-through transitions) are all wired in and
  verified clean end-to-end with `export/safe_check.js`, via a markup-safe word-splitter
  (`MK.splitWordsSafe`) that preserves existing inline markup (`<br>`,
  `<span class="box">`) instead of mangling it. **`video/reel-template-photo.html`**
  (the real-photo-composite style) has no separate caption track at all — recipe 6
  drives the fixed headline's own words from real spoken-word timing
  (`export/headline_sync.py`) instead, so the headline is never shown twice. **Recipe 6
  shipped for real on episode 54** (1.10.2026) — see `motion-recipes.md` for the two
  real bugs applying it to a live episode surfaced (a word-overlap glue at peak
  emphasis, fixed with a smaller peak scale plus permanent word spacing) and the known,
  accepted tradeoff (a long, slow-Ken-Burns scene can read as a `qa.py` "nearly still"
  warning once the old caption's incidental motion is gone — a measurement artifact at
  native frame rate, not a motion deficit). Recipes 1-3 have not shipped in a real
  episode yet; the next synthetic-style episode built from `reel-template.html` is
  their first real test end to end, per `motion-recipes.md`'s own standing.
- Reels render with `FRAMES=1 ./export/render.sh <build> 1080 1920 <seconds> <vo.wav> <out.mp4> [music.wav]`
  — frame-by-frame capture, because recorded playback drifted up to two seconds.
- Music is generated to the exact length: `python3 audio/build_music.py <seconds> <out.wav>`.
  **`render.sh`'s `[music.wav]` argument is the last positional argument and easy to
  silently drop** — confirmed the hard way on episode 54's own iteration rounds: every
  re-render across several rounds of fixes omitted it, so three shipped versions in a
  row had no music at all, and `check.sh` has no check that catches a silent music
  track, so nothing flagged it. If a build's duration changes (a re-time, a re-cut), the
  existing music file is now the WRONG LENGTH too — regenerate it at the new exact
  duration before the next render, don't reuse a stale file or skip it.
- Nothing with his voice in it is delivered before `audio/voice_doctor.py` runs on it, and a
  `BAD` finding blocks the delivery. `--repair` levels and evens sibilance, iterating until
  a pass finds nothing.
- The long cut stays on the recorded path; 24,000 screenshots costs more than the drift.
- After any render, verify sync by finding the brass flash cards and comparing them to the
  times the build declares.

## Frame layout — measured, not taste

Meta publishes the numbers for 9:16: keep text and key elements out of the **top 14%
(269px), bottom 35% (672px) and 6% of each side (65px)** on 1080x1920. The usable box
is x 65-1015, y 269-1248. The bottom third is where Instagram draws the username,
caption, audio label and buttons — a subtitle there is behind the interface, and ours
sat 413px inside it until it was measured.

- `node export/safe_check.js <build> [--tiktok] [--tol 10]` walks the real DOM at
  sample times, flags any visible text box outside the safe area, and flags two text
  boxes landing on each other. It waits 340ms after each seek because the build's
  reveals are 0.26-0.3s transitions. Run it before every render.
- Mark a purely decorative element `data-decor` and the checker leaves it alone — the
  watermark is meant to be lost to the platform UI.
- Captions are word-by-word: `export/karaoke.py <build> <deep.json>` aligns Whisper's
  word stamps onto the script (so "ChatGPT" stays one word) and emits 2-3 word chunks
  with the spoken word lit in brass. 80.2% of 13.5M short clips carry captions and
  78.6% animate them; a full sentence at the bottom of frame is the format's most
  common mistake, and ours repeated the scene's own headline word for word.
- Master to -14 LUFS, true peak -1 dBTP (YouTube turns anything louder down and never
  turns quiet content up). Music sits 18-20 dB under the narration and ducks.
- Length: 45-75s. Do not go under 30s. Buffer's 1.1M-video study and Socialinsider's
  11M-post set both put longer above shorter for this kind of content.

## Before a reel is sent

`./export/check.sh <build.html> <narration.wav> [rendered.mp4]` runs all three, and
nothing goes to him until it passes:

- `audio/voice_doctor.py` — pacing, rate, sibilance, endings, per line.
- `export/safe_check.js` — every visible text box against the platform safe area, and
  text boxes landing on each other.
- `export/qa.py` — the rendered file: resolution, pixel format, 48kHz stereo, length
  against the build's own DUR, frozen picture runs, black frames, a blank first frame,
  colour-card duration (under 0.45s reads as a glitch) and whether a card plays over
  speech, visual-change rhythm, loudness and true peak, loop seam.

Every one of those checks exists because a real defect reached him first. The card
duration check exists because he stopped the video on a 10-frame yellow card; the blank
first frame check because the hook faded in over 0.26s and frame zero was empty.

**Standing rule, as of episode 18: check → fix → re-check → only then send.** A targeted
fix after the gate already passed (a de-esser pass on one line, a re-cut clip) can break
something the first pass never touched, silently. `check.sh` runs again, in full, after
every such fix — not just the piece that changed — before the file goes to him. If that
re-check finds anything, fix it and run the whole check again. Repeat until a full run
comes back clean, then send. Never send on the strength of the first pass alone once a
fix has been made after it.

**Standing rule, as of episode 25: `check.sh` passing clean is necessary, not sufficient
— watch the actual rendered file yourself, twice, before it goes to him.** The automated
checks measure what they were built to measure; a garbled word, a leaked bit of debug
text, a layout glitch a viewer would spot in one second can still slip through numbers
that all read "ok". After `check.sh` passes: watch the rendered video in full, twice.
Only fully approve — and only then hand it to him — once both viewings come back clean.
If either viewing finds anything, fix it and watch the file twice again from scratch;
a fix made after one clean viewing isn't covered by it, the same reasoning as the
check → fix → re-check rule above.

## The studio app

- `studio/` — Next.js on Vercel, root directory `studio`, Supabase over `POSTGRES_URL`.
- Branch deploys are off in `studio/vercel.json` (`git.deploymentEnabled`); the free plan's
  100 builds a day are counted before any ignore step runs. Production builds on merge.
- Never "Redeploy" an old deployment: it rebuilds that old commit, and any commit from before
  `studio/` existed fails with "The specified Root Directory studio does not exist".
- **Vercel's own "Skip deployments when there are no changes to the root directory or its
  dependencies" (Settings → Build and Deployment → Root Directory) silently stopped every
  production deploy for almost a full day on 3-4.9.2026** — ten separate merges to `main`,
  several genuinely touching files under `studio/`, produced zero new deployments; the
  dashboard's Production Deployment stayed pinned to a merge from a day earlier with no
  error, no skipped-build entry, nothing to see without opening Settings directly. Disabled
  now. If episodes or site fixes stop appearing after merging again, check this toggle
  first, before assuming a Hobby-plan build-quota exhaustion (the two look identical from
  outside — no banner, no error, just silence).
- `/api/track` reads Instagram and Beehiiv and records only what changed. Cron runs it daily.
- **Which pages are public is declared once, in `studio/lib/routes.ts`** (`SITE` / `STUDIO`
  / `CRON`). The middleware and `app/shell.tsx` both import it. That list used to be
  duplicated in both files and drifted three times: `/api/subscribe` answered 401 to every
  visitor, then `/prompts` and `/search` redirected to the PIN gate, then those same two
  rendered inside the studio's Hebrew tab bar. `npm run check:routes` (wired as `prebuild`,
  so Vercel runs it) walks `app/` and fails the build on a route in neither list.
- The document is **English and LTR** — the visitor-facing site is the default. The studio
  is the Hebrew RTL island and declares that on its own container, so an English page can
  never inherit a right-to-left scrollbar.
