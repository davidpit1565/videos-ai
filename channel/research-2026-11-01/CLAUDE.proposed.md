# Actually Works — how this repo works (proposed, 1.11.2026 cleanup)

An AI-content channel and an AI-services business, run by David (18, Flemish Belgium, employed elsewhere `[ASK 9]`). Two engines, the paid one feeds the free one: `plan/business-model.html`. Full history of every rule below: `channel/research-2026-11-01/rules-history.md` (nothing was deleted, only moved).

## Talking to him
- He writes Hebrew, the videos are English. Answer in Hebrew. Content, captions, scripts: English (4-5 a week) plus Flemish (1 a week, for clients).
- Explain by the `explain-steps` skill (numbered clicks, interface labels in both languages in chat, boring path, optional steps marked). If he did not understand, replace the route, do not repeat it louder.
- Say the honest thing once, then do the work.
- Before any stretch of mechanical work (script from a decided template, publishing, caption/doc edits, builds, renames), tell him in one line to switch to the cheaper Sonnet tier. Keep Opus for debugging, architecture, anything where being wrong costs a day. `/fast` is not cheaper; switching mid-session does not reclaim cached context. The bigger lever is session length: after days, say so and start a fresh session from `SUNDAY.md`.

## העברת סשנים (25.10.2026, David)
כשהסשן ארוך או שמשימה גדולה הסתיימה: (1) עדכן את `SUNDAY.md` ואת `NEXT_SESSION_PROMPT.md` (מצב והדבר הבא); (2) פתח בעצמך סשן חדש עם הכלי `create_session` (מקור: הריפו הזה, ענף main), הפרומפט הקבוע: "קרא את CLAUDE.md, SUNDAY.md ו-NEXT_SESSION_PROMPT.md במלואם ובצע את 'הדבר הבא' בראש NEXT_SESSION_PROMPT.md", ועוד הוראה מיוחדת אם יש; (3) אמור ל-David בעברית איך קוראים לסשן החדש ומה הועבר אליו. ברירת מחדל: הסשן החדש קורא ומדווח ולא פועל עד ש-David אומר, כי כל פעולה עולה לו קרדיטים. הסשן החדש נראה ברשימת הסשנים באפליקציה, לא בצ'אט הנוכחי. אסור למחוק או לארכב סשן שיש לו תזכורת מתוזמנת או ענף לא ממוזג. סשן שנפל בגלל גבול ההקשר לא מעביר לבד: לכן מעבירים בצורה יזומה.

## Rules that do not bend
- **Never fabricate.** No invented clients, testimonials, results, prices, metrics. An assumed number says ASSUMPTION next to it. What research could not confirm is listed as unconfirmed. A number or fact shown on screen is verified from the source (photo, official page), not from memory.
- **Verify the product is real before the first line of any script, every time** (live web search: current name, behaviour, limits). Episode 18 was built on a retired name.
- **Secrets live only in Vercel environment variables.** Never in chat, git, files, logs. The PIN is never written anywhere.
- **Nothing ships untested silently.** What was built but not run says so in plain language in its file. Audio that was measured but not heard is reported as exactly that.
- **Privacy:** never publish where he lives; never use a photo from his own window or home (ChatGPT can narrow a photo to a street); people in photos only far away or from behind; the face pre-check applies and, if the tool is unavailable, say so instead of skipping silently. Never publish his name, email or phone number visible in a recording (cut it).
- **Measure, don't guess.** Real numbers from the studio, not memory. Voice decisions: measurement and his ear; if they disagree his ear wins and it is written down.
- **Standing authorization:** once a direction is approved, keep iterating and verifying without re-asking; come back only for a new judgment call or when ready to ship. A found problem is still reported plainly.

## Every video (content)
- **Topic:** chosen from `channel/demand-report.md` and `content-memory.md` (what really performed), not picked fresh `[ASK 7]`.
- **Hook:** read `channel/hooks-guide.md` first; run the `viral-hook-lab` skill. Every hook is a hypothesis: log its type and the 72-hour readings in `content-memory.md`. Do not cite untraceable statistics.
  - Product and claim in the first three words (David, 28.10); the viewer must FEEL it in 3 seconds as something happening to them; must pass the dry-sentence test.
  - 8-year-old test (David, 31.10): every line, starting with the hook, in the plainest English, no idioms, no slang, terms explained in the same breath. Plain, natural, spoken language throughout.
  - Never the same hook type two episodes in a row `[ASK 6]`.
- **Packaging:** an everyday thing already happening to the viewer, AI as the substance, never swapped for a non-AI topic (working direction, one outlier, not confirmed).
- **Setup path:** every episode has a full, exact, English-only step-by-step on its `/e/N` page (`studio/lib/articles.ts` `steps[]`), per `explain-steps`; `export/check_setup_guide.py` enforces it and fails on Hebrew.
- **Logos:** every app/site/product the episode names gets its real, current logo/icon on screen, sourced from the official site or Wikimedia, never redrawn. Logo badge = icon alone, never a caption under it.
- **Handle:** `@actually_works.ai` (with the underscore), unless the screen would be covered.
- **Closing:** `[ASK 5]` (current practice: ep 81 has no closing line; older rule: locked "The setup's in the link in bio." then a tomorrow-line naming a real next episode; never promise a next episode that does not exist).
- **Success bar (David, 31.10):** 5,000-10,000 views per reel; below that it is not success.

## The voice
- Profile `audio/voice/profile/` (`profile.json` default exaggeration 0.50, cfg 0.30; per episode about 0.72-0.78 for energy, about 0.64 and re-roll on lines the accent check flags, hook/beats higher).
- Run `python3 audio/script_lint.py --cues <build>` before narration. His voice softens unstressed -ER, -LE/-BLE, -LY, R+cluster, flapped T: reword, never respell; end lines on hard consonants.
- A flagged line goes through `audio/line_doctor.py`; approved takes are locked in `audio/voice/profile/canonical-lines.json` and loaded byte-for-byte.
- `audio/voice_doctor.py` on everything with his voice (`BAD` blocks delivery). `audio/voice_quality.py <narration-r.wav> <cues.json> --music <music.wav> --vol <MUSIC_VOL>` on every episode before shipping (pitch range 4.9-8.4 st sounds right to him, line endings, steady tone, music audible on a phone speaker). It is measured, not heard: say so.
- Two-voice episodes, answer scenes, `ACCENT_SKIP`: see history file (situational).
- Flemish: `audio/speak_language.py`, needs `record/flemish-script.md` reference.

## Look (every video)
- **Safe area (Meta, 1080x1920):** nothing in the top 14% (269 px), bottom 35% (672 px), 6% each side (65 px). `node export/safe_check.js <build> [--tiktok] [--tol 10]` before every render. `data-decor` marks decoration.
- **Nothing we add may cover what the viewer needs to see** (David, 18.10): check every frame, not just the numbers.
- **Motion is smooth, never robotic** (David, 1.11): long eased curves, overlapping movement, soft fades and scale, no stepped rhythm, nothing jumps; check by looking at the rendered motion.
- Captions word by word (`export/karaoke.py`), 2-3 word chunks, spoken word lit in the series accent colour; never a full sentence at the bottom.
- Start on the proof/action from frame 0 (key state or stake visible). Short, punchy lines.
- Colour, theme, fixed identity: see "Current series design direction" below.

## Audio and music
- Music only from the real licensed library: `python3 audio/pick_real_track.py <seconds> <out.wav> --mood <mood>` (`FORCE_TRACK=<file.mp3>` pins one), never `audio/build_music.py` for anything shipped. After any change of duration regenerate the music at the exact length and pass it as the last argument of `render.sh`. Verify with `audio/check_music_bed.py` AND by which script made the file.
- Master -14 LUFS, true peak -1 dBTP. Music about 18-20 dB under the voice and ducking (phone-speaker band check: `voice_quality.py`).

## Pipeline and gates
- `export/produce.sh <episode> <build.html> <duration> [accept_words] [bpm] [mood]` is the one entry point (lint, render, gate, captions, design check, ships to `studio/public/reels/`). Do not build a third one. A video made another way (e.g. HyperFrames) still passes the same gates before publishing `[ASK 10]`.
- `./export/check.sh <build.html> <narration.wav> [rendered.mp4]` (voice_doctor, safe_check, qa.py) must pass before anything goes to him. After ANY fix, run the whole check again until a full run is clean. Then watch the rendered file in full, twice; a fix after a clean viewing restarts both viewings.
- Render: `FRAMES=1 ./export/render.sh <build> 1080 1920 <seconds> <vo.wav> <out.mp4> [music.wav]`. The picture follows the narration (`export/retime.py`), never the reverse.
- Length: set per episode, hook-to-fix as early as possible `[ASK 2]` (old rule 45-75 s, not under 30 s; ep 81 is 25.3 s).

## Shipping
- Studio production reflects only `main`: when `check.sh` is clean and nothing needs his judgment, mark the PR ready and merge; ask first only for a real judgment call or a change to what an episode claims.
- **Merging is not shipping.** After a merge that carries a reel: (1) read `https://api.github.com/repos/davidpit1565/videos-ai/commits/<merge-sha>/status` until Vercel is `success` (`failure` = no new deploy; a later main commit deploys it); (2) compare `content-length` of `https://www.actually-works.com/reels/reel-N.mp4` with `git cat-file -s origin/main:studio/public/reels/reel-N.mp4`. Builds also fail when the database is unreachable (1.11: deleted Supabase project), and local builds pass without it.
- Then send the phone notification (section below).

## Content memory — the weekly loop
- `channel/content-memory.md` (patterns, hypotheses) and `channel/experiments.md` (deliberate tests only). Real per-episode numbers live in the studio's tracked state, not in markdown. Never invent a metric.
- "Plan next week"/"what should we learn": read content-memory, read the real numbers, separate FACT / HYPOTHESIS / UNKNOWN, report what happened, guesses (labelled), what to repeat, what to test, what to stop. A pattern becomes Confirmed only after two independent episodes. No numeric virality score; STRONG / PROMISING / WEAK / UNCLEAR with reasons.

## Everything we build becomes an episode
Every skill, agent or tool we finish goes onto the studio idea list the same day, angle written (what it does, the one screen that proves it, the number that makes it real). Nothing is built and quietly filed. (No public catalogue page of skills/prompts; `/p/[slug]`, `/s/[slug]` stay.)

## The studio app (short)
- `studio/`: Next.js on Vercel (root `studio`), Supabase over `POSTGRES_URL`. Branch deploys off (`studio/vercel.json`); production builds on merge. Never "Redeploy" an old deployment. If merges stop deploying, check Vercel's "Skip deployments when there are no changes" toggle first.
- Public pages are declared once in `studio/lib/routes.ts` (`SITE`/`STUDIO`/`CRON`); `npm run check:routes` fails the build on an undeclared route. Site is English LTR (never Hebrew on any visitor-facing page); the studio is the Hebrew RTL island.
- `/api/track` records Instagram and Beehiiv changes daily.
- Cloud container suspends when a turn ends: run long stages while a turn is active and keep loops resumable.

## Phone notification when a reel is ready (David, 25.10.2026)
When a reel is ready (check.sh passed, merged, deploy verified), send a real phone notification with the PushNotification tool: one line, the episode number and that it is ready. Do this for every new reel. The studio's own "reel ready, not published" reminder pushes were removed the same day at his request (they were not built well); do not re-add them without asking.

## Claude may read the studio (David, 25.10.2026)
The studio is gated against the public, not against Claude. When David has given the PIN in the chat of the current session, read real numbers with `POST /api/unlock` (json `{"pin": ...}`, keep the cookie) and then `GET /api/state` on https://www.actually-works.com. The PIN is never written into a file, a commit, a PR or a log. If no PIN was given in the session, ask for it once. Fields: `state.episodes[]` (views, reach, likes, saves, shares, publishedAtPrecise), `state.snapshots[]` (followers). Watch time and reach by follower type are NOT_AVAILABLE for this account.

## Current series design direction
TODO (design agent): fixed visual identity (palette, type, components) — replaces per-episode colour? `[ASK 1]`
TODO (design agent): theme and accent (starting point from David 1.11: light base + lime, ChatGPT-logo wheels, phone frame, blue user messages)
TODO (design agent): format default: drawn chat re-created with exact real words and a label, vs real screen recording `[ASK 3]`
TODO (design agent): photo backgrounds yes/no `[ASK 4]`; closing scenes / closing line `[ASK 5]`
TODO (design agent): length and structure (ep 81 test: about 25 s, fix within about 10 s, structure borrowed from a viral reel with our own text; result unknown until the 72-hour reading)
TODO (design agent): captions style and motion kit (HyperFrames pipeline, wiring into produce.sh gates)
