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
- **Measure, don't guess.** Demand comes from real view counts (`channel/demand-report.md`),
  voice decisions from measurement *and* his ear — and when they disagree, his ear wins and
  the disagreement gets written down.
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
- `audio/speak_language.py` does the same voice in 23 languages. Flemish needs its own
  reference recording — `record/flemish-script.md`.

## Standing rule: everything we build becomes an episode

He said it plainly — every skill, agent, or tool we develop here is itself content. When a
new one is finished, add it to the idea list in the studio with the angle already written:
what it does, the one screen that proves it, and the number that makes it real. Nothing gets
built and quietly filed.

Already queued this way: `explain-steps`, `voice_doctor.py` (an agent that hears what is
wrong with a voice and fixes it), `retime.py` (why editors squeeze audio and why that is
backwards).

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
- **`channel/motion-recipes.md` has five verified motion upgrades — word-by-word builds,
  a per-word text highlight (fixes a real line-wrap bug in the naive one-box version),
  a staggered contradiction reveal, zoom-through scene transitions (every episode today
  hard-cuts between scenes with zero transition, which `hyperframes-animation`'s own
  rules call a non-negotiable gap), and one GPU-tier fragment-shatter hero beat reserved
  for a single real reveal per episode.** Verified in isolated demos David approved one
  at a time, then extracted into a real shared module, `export/motion-kit.js`
  (`window.MotionKit`), re-verified with its own frame capture. **`video/reel-template.html`**
  is the real starter build to copy for a new episode — it wires in recipe 4
  (zoom-through transitions) universally, verified clean end-to-end with
  `export/safe_check.js`. Recipes 1-3 (hook word-by-word, quote highlight, scoreboard
  stagger) are still NOT wired into it — they need a word-splitter that preserves
  existing inline markup (`<br>`, `<span class="box">`) instead of mangling it, which
  doesn't exist yet. Don't claim a future episode uses recipes 1-3 until that lands.
- Reels render with `FRAMES=1 ./export/render.sh <build> 1080 1920 <seconds> <vo.wav> <out.mp4> [music.wav]`
  — frame-by-frame capture, because recorded playback drifted up to two seconds.
- Music is generated to the exact length: `python3 audio/build_music.py <seconds> <out.wav>`.
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
