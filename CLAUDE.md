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

## Rules that do not bend

- **Never fabricate.** No invented clients, testimonials, results, prices or metrics. If a
  number is an assumption, it says ASSUMPTION next to it. If research could not confirm
  something, it is listed as unconfirmed, not smoothed over.
- **Measure, don't guess.** Demand comes from real view counts (`channel/demand-report.md`),
  voice decisions from measurement *and* his ear — and when they disagree, his ear wins and
  the disagreement gets written down.
- **Secrets live only in Vercel environment variables.** Never in chat, never in git. The
  publication id is public; the API key is not.
- **Nothing ships untested silently.** If something was built but not run — the n8n workflow,
  for instance — the file says so in plain language.

## The voice

- Profile: `audio/voice/profile/` — reference chosen by his ear, settings locked in
  `profile.json` (exaggeration 0.50, cfg 0.30).
- **Run `python3 audio/script_lint.py --cues <build>` before generating narration.** His
  voice softens word endings — unstressed -ER, -LE/-BLE, -LY, R plus a cluster, flapped T.
  Swap the word; respellings were measured and do not help.
- A line he flags goes through `audio/line_doctor.py`, which ranks candidates by the energy
  left in the last 90 ms of the target word. The approved take is locked per line.
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

## Building and rendering

- The picture follows the narration, never the reverse. Build the voice at its own pace,
  then `export/retime.py <build> <cues.json> --out <build>-paced.html` moves every timing
  in the build to match. `--fit` on build_voice is only for a cut that genuinely may not
  move; using it for pacing is what produced seven overlapping lines in episode 02.
- Reels render with `FRAMES=1 ./export/render.sh <build> 1080 1920 <seconds> <vo.wav> <out.mp4> [music.wav]`
  — frame-by-frame capture, because recorded playback drifted up to two seconds.
- Music is generated to the exact length: `python3 audio/build_music.py <seconds> <out.wav>`.
- Nothing with his voice in it is delivered before `audio/voice_doctor.py` runs on it, and a
  `BAD` finding blocks the delivery. `--repair` levels and evens sibilance, iterating until
  a pass finds nothing.
- The long cut stays on the recorded path; 24,000 screenshots costs more than the drift.
- After any render, verify sync by finding the brass flash cards and comparing them to the
  times the build declares.

## The studio app

- `studio/` — Next.js on Vercel, root directory `studio`, Supabase over `POSTGRES_URL`.
- Branch deploys are off in `studio/vercel.json` (`git.deploymentEnabled`); the free plan's
  100 builds a day are counted before any ignore step runs. Production builds on merge.
- Never "Redeploy" an old deployment: it rebuilds that old commit, and any commit from before
  `studio/` existed fails with "The specified Root Directory studio does not exist".
- `/api/track` reads Instagram and Beehiiv and records only what changed. Cron runs it daily.
- Public pages (`/join`, `/p/*`) must not inherit the studio's Hebrew chrome.
