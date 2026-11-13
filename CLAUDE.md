# Actually Works — how this repo works

An AI-content channel and an AI-services business, run by David: 18, based in Flemish
Belgium, employed elsewhere and building this alongside. Two engines, and the paid one feeds
the free one — the full reasoning is in `plan/business-model.html`.

## Talking to him

- **He writes Hebrew, the videos are English.** Answer in Hebrew. **Every message to him is in Hebrew, without exception (David, 5.11.2026)**: status updates, short notices after a background agent or a GitHub/Vercel notification, reports and questions alike, whenever he writes in Hebrew. English only for things that stay English (scripts, captions, code, file names, quoted on-screen text). Content, captions and
  scripts are English (4–5 a week) plus Flemish (1 a week, for clients).
- **Explain by the `explain-steps` skill.** Numbered clicks, interface labels in both
  languages, the boring path over the clever one, optional steps marked as optional. When he
  says he did not understand, the step assumed something — replace the route, do not repeat
  it louder.
- **Spread the work over parallel agents (David, 1.11.2026).** When a job splits into independent parts (research, build, voice, checks), start agents for each part at once instead of doing them one after another. Limits that stay: one voice/TTS render at a time (each needs 4-5 GB, parallel ones were killed for memory), no Firecrawl while its quota is high, no agent publishes, merges or touches secrets, and every agent report is checked before it is passed on as fact.
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

## העברת סשנים (25.10.2026, David)
כשהסשן ארוך או שמשימה גדולה הסתיימה: (1) עדכן את `SUNDAY.md` ואת `NEXT_SESSION_PROMPT.md` (מצב והדבר הבא); (2) פתח בעצמך סשן חדש עם הכלי `create_session` (מקור: הריפו הזה, ענף main), הפרומפט הקבוע: "קרא את CLAUDE.md, SUNDAY.md ו-NEXT_SESSION_PROMPT.md במלואם ובצע את 'הדבר הבא' בראש NEXT_SESSION_PROMPT.md", ועוד הוראה מיוחדת אם יש; (3) אמור ל-David בעברית איך קוראים לסשן החדש ומה הועבר אליו. ברירת מחדל: הסשן החדש קורא ומדווח ולא פועל עד ש-David אומר, כי כל פעולה עולה לו קרדיטים. הסשן החדש נראה ברשימת הסשנים באפליקציה, לא בצ'אט הנוכחי. אסור למחוק או לארכב סשן שיש לו תזכורת מתוזמנת או ענף לא ממוזג. סשן שנפל בגלל גבול ההקשר לא מעביר לבד: לכן מעבירים בצורה יזומה.

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
- **A logo badge is the icon alone — never a text caption underneath it.** Decided
  5.10.2026, David's direct instruction, after episode 58 shipped with a small
  uppercase label ("whatsapp · photo touch-up · march 2026") under the WhatsApp logo
  badge — a pattern copied as-is into episodes 55, 56 and 57 too, none of which were
  asked for a caption either. The logo mark itself already identifies the product; the
  text underneath it is restating what the viewer can already see. Fixed in episode
  58's build (the `.logolabel` div/CSS/JS removed from `reel-58.html/-timed/-kar`) —
  episodes 55-57 were not touched retroactively, since that wasn't asked for, but they
  carry the same pattern and are candidates if he wants it applied there too.
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
  side by the end of it. Write it per `explain-steps` — numbered clicks, English interface labels only (David, 16.10.2026:
  NO Hebrew on any visitor-facing page; `export/check_setup_guide.py` fails on it. Labels in both languages are for chat answers to him, not for the site), the boring path, what happens after each step — and it goes on the
  episode's own site page (`/e/N`), not just spoken narration a viewer can't pause and
  copy from. Applies to every future reel/episode, whichever content pattern it uses.
  Enforced, not just written down: `export/produce.sh` runs `export/check_setup_guide.py`
  before shipping and refuses to ship an episode with no `studio/lib/articles.ts` entry, or
  one whose `steps[]` is missing or placeholder-thin — a caption existing was already a hard
  stop for the same reason, this closes the matching gap for the setup guide itself.
- **Evidence check on hooks, 20.10.2026: run the `viral-hook-lab` skill (`.claude/skills/viral-hook-lab/`) when writing an opening line.** Research (`channel/hook-research-20-10.md`) found no proven hook formula and no traceable per-second hook data, so every hook is a hypothesis: log its type and its 72-hour readings (reach, retention, sends, saves) in `content-memory.md`, and do not cite untraceable statistics ("65% leave in 3 seconds", the Zeigarnik effect, the 8-second attention span).
- **Read `channel/hooks-guide.md` before writing any episode's opening line. Never repeat
  the same hook type two episodes in a row, and never ship a hook that only passes the
  "dry-sentence test" by accident.** Decided 2.9.2026, after he flagged twice, in the same
  day, that the opening line kept reading as a flat, informational sentence — even after a
  type-rotation fix, the replacement line still failed on tone. A hook is not just a true,
  on-topic first sentence: it has to create real pull (fear, identity, stakes, curiosity),
  not just state a fact. `hooks-guide.md` has the sourced taxonomy, the dry-sentence test
  itself, a log of which type each recent episode used, and the two rejected drafts that
  failed this exact check — read those before assuming a new draft clears the bar.
- **In the FIRST SECOND the viewer must already know what the video is about (David, 8.11.2026, after Miki watched episode 86: "in the first second I still don't understand what the video is about: 'Don't tell my teacher', no idea what it's about. This is the most important thing, and we miss it every time and tell ourselves it's good, but it isn't").** A hook that is a curiosity line without a stated subject fails this, even if it scores high on the rubric and even if the video later gets views (episode 86 got the most views we have had while failing this test, so views do not prove comprehension). Test, before building and again on the first rendered frame: show ONLY the first frame and the first spoken second to someone who has not seen the script (a fresh agent as the blind reader works) and ask two questions: "what is this video about?" and "would you stop scrolling, and why?" (added 8.11.2026 after a reel that states its subject at once but has no stake and does not make you stop). The first answer must name the product or situation (ChatGPT, GitHub, a school test...) AND the topic (an AI told a secret, an undo button for AI apps). The subject must be both SAID in the first words and SHOWN on the first frame (logo + a few big words), not left for line 2. Log the blind reader's answer in the episode script file.
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
- **Package every episode as an everyday thing that's already happening to the viewer —
  with AI as the substance inside it, never swapped out for a non-AI topic.** Decided
  6.10.2026, David's go-ahead after the episode 55 analysis (`content-memory.md`): 55
  (Alexa/Amazon — not really an AI topic, shipped by mistake) got 260 views, ~2x the
  run's median, from a second wave of non-followers — but gained 0 followers, 0 shares,
  0 saves. Reach from an off-topic video builds an audience that doesn't want what this
  channel or the business offers. So take the packaging, not the topic: a product nearly
  everyone owns or uses (phone, WhatsApp, Google, a smart speaker, their kid's phone), a
  short hook (~7-12 words) stating something that is already happening to them right now,
  and the AI mechanism as the actual content. Episodes 44 and 48 (177/185, both AI) were
  already built this way. This is a working direction, not a confirmed pattern — one
  outlier episode is not proof; `channel/experiments.md` tracks the test.
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

- **Every video, hook option and review page carries scores, and the scores are calibrated against results (David, 8.11.2026).** HOOK, VIRALITY, OVERALL and a PREDICTED VIEWS score on the scale in `channel/score-calibration.md` (200 views = 50, 10,000 views = 100, log scale; the goal is 10,000 views). After 48 h and 72 h the real views go into the same file next to the prediction and I adjust my scoring by the gap. This overrides the older "skip a numeric virality score" line in the Content memory section for hand-offs to David: give the numbers, with the reasoning in a line, and say they are judgements, not measurements.
- **Pre-publish gate, David 4.11.2026: every episode needs a hook score of at least 90 (goal 95) and a virality score of at least 85 on the written rubric, and the target is 1,000 views per episode.** The scores are my judgement against the rubric (personal and felt in 3 s, product named at once, one specific curiosity gap, every line a hook, a sendable ending, alive picture), not a measurement and not a promise. Under the bar: rewrite before building. Every episode logs its predicted score and its real views at 48 h in `content-memory.md`, so we learn whether the score means anything. Followers come after we reliably pass 1,000.

- **Anything David must hear or watch goes to him as a PLAYABLE page, not only as a file card (David, 4.11.2026).** In the app he can see audio and video files but cannot play their sound, and downloading each one is too much work. For every voice take, hook option or video review: publish a private Artifact page with `<audio controls>` / `<video controls>` elements (files as data: URIs, under 16 MB, so re-encode a smaller review copy of a video; 720 px wide, crf 27 is about 1.7 MB per 21 s) and give him the link. The sound only plays after he taps. Keep ONE page per episode and update it in place (same file path) instead of making new links. Say whether the file is a review copy.

- **Virality gate moves to the CONCEPT stage (David, 4.11.2026: virality is what makes a video explode, 85 or more is the minimum from now on).** A polished render cannot lift a weak concept: episode 84 sat at 65-70 after five rounds of polish. So score the concept BEFORE any scene or voice work, on this checklist, and do not build under 85: (1) a specific, surprising thing happening to the viewer's own account/phone, not a general warning; (2) a curiosity gap in the hook that only the video closes; (3) something worth SAVING (a path, a list, a setting) shown on screen as a screenshot-able card; (4) a named person to send it to; (5) a reason to watch twice (loop back to the hook, or a detail that is easy to miss); (6) a claim a stranger can check in 30 seconds. Write the score and the checklist result into the episode script file. If the concept is under 85, change the concept (angle, hook, payoff), not the polish.

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
  regenerating, for every episode. "The setup's in the link in bio." is locked this way —
  add a new line to the manifest the same way once he approves a take for it. ("Follow
  for the setup that actually works." is also still in the manifest, but is retired as the
  final line — see the next rule.)
- **The final line names tomorrow's episode — decided 6.10.2026, David's choice, replacing
  the locked "Follow for the setup that actually works." from episode 59 on (58 too, if it
  hasn't been published yet).** The research behind it (`content-memory.md`, 6.10.2026):
  a generic "follow for more" barely converts; a line pointing at one concrete next thing
  converts several times better, and this channel was gaining ~1 organic follower a month.
  Shape (revised 6.10.2026 — David called the first wording, `Tomorrow: <topic>. Follow so
  you see it.`, "childish and not professional", and asked for something fluent that pulls
  like Nas Daily's sign-off): one flowing spoken sentence that names tomorrow's topic as a
  promise, then a short follow clause that gives a reason — `Tomorrow, I'll show you what
  <company> does with <the thing>. Follow, so you get the full story.` No "Tomorrow:" label, no
  colon. Research behind it: Nas Daily's fixed sign-off ("That's one minute, see you
  tomorrow") works as a signature plus curiosity about the next video, and short-form
  sources rank open-loop teasers above a generic "follow for more" (vendor blogs — trust the
  direction, not the numbers). It is NOT locked: it's generated and checked like any other line (script_lint, voice_doctor,
  accent), every episode. **This means episode N+1's script is written — topic chosen from
  the data, product verified live — before episode N ships**, so N's last line can name it.
  The promise is binding (never-fabricate rule): if N+1's topic changes or doesn't publish
  the next day, re-render N's final line before N goes out. Standing order stays: "The
  setup's in the link in bio." second-to-last, the tomorrow line is the true final line —
  episode 54 once shipped these reversed, caught only by David watching. Verify the CUES
  order and the matching scene text before shipping.
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
  **Open, not yet designed**: David then clarified (same night) he does still want
  some standing, cross-episode treatment for these two scenes specifically — not the
  literal same photo file, but a consistent direction/design still to be figured out.
  Explicit instruction: leave episode 54's current closing scenes alone (they're
  fine as shipped), think about what that standing direction could be, apply it
  starting from a future episode once actually decided. Not a task to pick up
  casually — a real design call that needs his input, not a guess.
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

## The v4 style is the standard for every episode (David, 18.10.2026)

After watching episode 71 v4 he said it is "much better, much more engaging, I enjoyed every second", and that this direction applies to **all** future videos. What it means:
- **Real motion from the real screen recording**, not held stills: play the actual segments (menu opening, page sliding, the switch flip) at natural speed. A swipe that really takes 0.5s must take 0.5s on screen (`data-rt`/`data-dl` per scene: real-time seconds the source segment takes, and its start delay). Never slow-motion a segment to fill a line.
- **Start on the proof**: the first frame already shows the real screen with the key state tagged (red ON / green OFF tag), not an empty home screen.
- **Short, punchy lines with exclamation beats on the hook**; reword any word the voice swallows ("decides" → "controls", "Find" → "Tap") instead of fighting the model.
- **Voice**: exaggeration about 0.78 (hook/beats higher); lines the accent check flags go lower (0.64) and get re-rolled. His own verdict: clearly more excited, still occasional off moments ("Mine was on"). Enthusiasm is capped by the calm reference clip, so say that honestly.
- **Music**: energetic bed from the real library (now 69 tracks incl. the 54 new Pixabay ones). `FORCE_TRACK=<file.mp3>` pins the track when re-rendering an episode whose music he already liked.
- **Alive and scroll-stopping from the first frame to the last (David, 1.11.2026).** Something moves or changes on screen at all times; no frame sits still for more than about 2.5 s (the reference reel measures 17% still time, our episode 81 measured 50%). The opening stops the scroll, the payoff or the thing to copy arrives early (within about 10 s), and the end still gives a reason to stay to the last second. Targets measured from the reference reel are in `channel/research-2026-11-01/ref-reels.md`.
- **Copying a proven structure is fine (David, 1.11.2026).** Take the hook shape and beat order of a viral reel, put our own tested artifact in the middle, never promise what we did not test, never copy invented statistics, credit stories we retell. Reach depends mostly on the account and timing, so a copied script is not a guarantee: log it as an experiment in `channel/experiments.md`.
- **Later, not now (David, 1.11.2026):** videos about OUR OWN apps start only after we understand what makes our videos spread.
- **Nothing we add may cover what the screen is showing (David, 18.10.2026).** The `@actually_works.ai` handle sat on the keyboard and the answer in the first full-bleed screen episode. On full-bleed screen episodes the handle is dropped (the platform shows the account name anyway); any overlay (tags, rings, headline bars) must sit where the recording shows nothing the viewer needs. Check every frame for this, not only the safe-area numbers.
- **Motion is smooth, never robotic — standing for every episode from now on (David, 1.11.2026, after episode 81 v5).** Long eased curves (no linear or snappy easing), continuous overlapping movement, gentle camera/background drift, soft fades and scale instead of abrupt pops, no stepped rhythm (typed text at natural, slightly varying speed), nothing that jumps; settles are soft. Check it by looking at the rendered motion, not only the numbers. Colour stays light (the approved light + lime base) unless he says otherwise.
- **Two-voice dialogue episodes (72 on):** the second voice comes from voice box as WAV files (resample to 48 kHz mono 16-bit first, or the pipeline plays them double speed), is registered as canonical clips in `audio/voice/profile/canonical-lines.json` and left out of the accent check with `ACCENT_SKIP=<line numbers>` (`check.sh`, `check_accent.py --skip`). The on-screen text is the real output of the real chat; the voice only reads it.
- **Answer scenes in a dialogue episode (David, 21.10.2026):** the white headline bar with the spoken words lit as they are said (episode 72's style) plus ONE ring drawn around the real answer block, measured on the real frame, is what he approved. A moving per-word highlight box over the real text was tried on episode 74 and he rejected it ("not good, too prominent": the earlier style is better). Do not rebuild it. Hold the real frame still for the AI-voice lines only if the text is not scrolling; check where the frame stops moving (`channel/assets/ep<N>-screen/`) before placing a ring.
- **His own photos are a first-class source (episode 74).** He photographs on his phone and owns them. Never use a photo taken from his own window or home, and never publish where he lives: ChatGPT can narrow a photo to a street. Photos with people only far away or from behind; the face pre-check still applies (the Adobe tool was not available in the 74 session: say so instead of skipping it silently).
- **Verify a number on screen before it goes in a script.** Episode 74's claim "the answer is correct" rests on the photo itself (a MIZNON storefront and the number 22) plus public listings of the restaurant's address, not on David's memory of the street.
- The cloud container is suspended when a turn ends and background jobs die: run long voice/render stages while a turn is active (foreground or polled background), and keep loops resumable (`seeds.state`).

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
  **Merging is not shipping: verify it is live before saying "ready" (21.10.2026).** Vercel marked
  the deploy of episode 74's v4.2 merge as failed with no signal here; the studio kept serving an
  older cut for two hours until David noticed. After every merge that carries a reel: (1) read
  `https://api.github.com/repos/davidpit1565/videos-ai/commits/<merge-sha>/status` until the Vercel
  status is `success` (a `failure` means no new deploy: a later main commit has to deploy it); (2)
  compare `content-length` of `https://www.actually-works.com/reels/reel-N.mp4` with
  `git cat-file -s origin/main:studio/public/reels/reel-N.mp4`. The studio pages themselves are
  behind the PIN, so the file size is the proof you can read. Failed deploys on main this week were
  also seen on 94ebed4, f90ee52 and 506a793, each followed by a good deploy of the next commit.
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
- **One fixed series identity, with the product's own accent (David, 1.11.2026).** The base never changes: the light page, black heavy type, the layout, components and smooth motion of episode 81's design (spec: `channel/research-2026-11-01/design-system.md`). Only the accent and the small details follow the product or platform the episode is about (David: ChatGPT, Claude, Amazon, ...): its real logo colours as the accent (ChatGPT lime-green, Claude orange, Amazon orange), its real icons and marks as the badges and decorations, and drawn UI in that product's feel; a small per-episode change on the same base, not a new look. The agent working on an episode decides the details itself. This replaces the old "a different accent colour every episode" rule. `export/produce.sh`'s design-variety check still fails on a repeated colour and has NOT been updated yet: change it before the next HyperFrames episode goes through it. Look at the real frames; contrast numbers alone are not enough.
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
  shipped for real on episode 54** (1.10.2026) — see `motion-recipes.md` for the full
  account across its rounds, including a real index-misalignment bug in
  `headline_sync.py` once `.box` phrases started building word by word (never caught
  by eye, only by David reporting words popping early/late/missing) and the final,
  deliberately simple mechanism: `MK.animateWordEmphasis` is a plain color toggle —
  the exact same thing `karaoke.py`'s classic caption track has always done
  (`.subs b.on{color:accent}`) — applied uniformly to every word including `.box`
  ones, with no scale or brightness involved, on David's own direct instruction that
  it should be "the simplest thing, like every other video." Recipes 1-3 have not
  shipped in a real episode yet; the next synthetic-style episode built from
  `reel-template.html` is their first real test end to end, per `motion-recipes.md`'s
  own standing.
- **Black zig-zag wipes between scenes are rare, not the default (David, 3.11.2026, after his friend Roni said on episode 83: "too much transitions, these black things between the slides, it disturbs a bit").** Never one per scene. Use a hard black wipe only for a real big change of topic, at most once per video, and not in every video. Between ordinary scenes use soft dips or crossfades that never show two scenes' text at once. Episode 83's first cut had nine wipes in 29 s: that is the thing not to repeat.
- **Music is something we learn over time (David, 3.11.2026: "I am bad at choosing music, we improve each time").** Every episode logs its track, mood tag, measured bed level, and any listener verdict in `channel/music-notes.md`. Roni called episode 83's first bed (a corporate-technology track) "very generic": avoid corporate/inspiring stock-sounding beds, pick something with a character that fits the line's feeling, and keep the bed audible on a phone (300-3500 Hz). Source stays the real licensed library.
- **No real photo backgrounds (David, 1.11.2026; retires the rule from episode 55).** Episodes use the drawn light style of episode 81. Photos are allowed only inside a card or phone when they ARE the proof. The real-logo and real-product-screenshot rules stay as written above. The photo-composite template and its face pre-check stay in the repo for anyone who wants a photo episode.
- **Standing rule, effective episode 55 (1.10.2026, David's direct instruction): keep
  every spoken line in plain, natural, everyday language — not elevated or formal
  wording — across every future episode, not just when a line feels obviously stiff.**
  This is a sharper, standing version of `hooks-guide.md`'s existing "write for a
  person, not an AI-literate viewer" rule: it applies to word choice and sentence shape
  throughout the whole script, not only to jargon/comprehension. Before a script ships,
  reread every line and ask whether a person would actually say it out loud this way —
  if a word or phrase reads like it belongs in an article rather than a sentence a
  friend would say, simplify it, the same discipline already applied to jargon. This
  does not license losing precision or dropping a real caveat — episode 55's "send it to
  anyone who still has one of these in their kitchen" → "send it to someone you know who
  has one" is the shape of the fix: shorter, plainer, same claim.
- Reels render with `FRAMES=1 ./export/render.sh <build> 1080 1920 <seconds> <vo.wav> <out.mp4> [music.wav]`
  — frame-by-frame capture, because recorded playback drifted up to two seconds.
- **Music for a shipped episode always comes from the real licensed library
  (`audio/music-library/` + `audio/pick_real_track.py --mood <mood>`), never from
  `audio/build_music.py`'s synthesized output.** David said so directly, more than
  once, because the real tracks (Pixabay, free to use, no attribution, downloaded and
  listened to by him — see `audio/music-library/MANIFEST.md`) are more professional;
  `build_music.py` only exists for quick local iteration before a real track is picked,
  never for what actually ships. This is the THIRD documented incident of this same
  mistake shipping anyway: episodes 32/33 (a missing `MOODS` entry silently fell back
  to synthesized audio), episode 29 (the real track picked for "tense" read as
  thin/absent to the ear despite healthy loudness numbers — fixed by pointing "tense"
  and "suspense" at the same already-vetted track), and episode 54 round 2 (several
  re-renders used `build_music.py` directly out of habit, never touching the real
  library at all — caught only because David heard it and said so). Verify a music bed
  both ways before shipping: `audio/check_music_bed.py <music.wav>` (mean dB, peak dB,
  longest quiet stretch — catches "technically present but reads as absent") AND which
  script actually produced the file — a healthy loudness reading from
  `build_music.py` output is still the wrong file.
- Music is generated to the exact length: `python3 audio/pick_real_track.py <seconds> <out.wav> --mood <mood>`
  (same output contract as `build_music.py` — exact duration, fades, mono 48kHz — so
  it drops into `render.sh` the same way).
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
- Length: the shortest cut that holds the real content, about 25-45 s, no padding, and test it (David, 1.11.2026). The old "45-75 s" citation could not be verified: Buffer's length study was not found, and Socialinsider's 9.8M-Reels set (2026) is correlation only and puts 45-60 s highest by median views. Measure each episode's retention at 2 s, 5 s and the end (skip rate, average watch time) instead of trusting a number.

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

**Standing rule, 21.10.2026 (David's words: the voice must always sound good, no frequencies that sound bad, the highest quality, "as if we used the best microphones"): run `audio/voice_quality.py <narration-r.wav> <cues.json> --music <music.wav> --vol <MUSIC_VOL>` on every episode before it is shipped.** It measures what the older checks miss: each line's pitch range and where it ends (episode 74's hook swung 12.1 semitones and ended -4.4 below its median: every other check passed and David called the tone "really bad"; the lines he likes sit at 4.9-8.4 st), a steady tone in the voice, and whether the music bed can be heard on a phone speaker (episode 74's first track was an 85%-sub-bass drone: present in the file, inaudible on the phone; the bed should sit about -6 to -18 dB under the voice in the 300-3500 Hz band). A hook line that fails is re-rolled with several seeds and a lower exaggeration and chosen by these numbers, not by guess. It does not replace his ear: after it passes, say plainly that the audio was measured, not heard.

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
- **Studio reel file names (9.11.2026):** the studio reads the episode number from the digits in a file name in `studio/public/reels/`. Until 9.11 the `.mp4` extension counted, so a file with no digits in its name (`post-ai-image.mp4`) was read as episode 4 and sat at the top of the renders list. Fixed in `studio/lib/reels.ts` and `studio/scripts/prune-old-reels.mjs` (the extension is stripped first). Only `reel-N.*` files belong in that folder; the YouTube publish route (`/api/youtube/publish`) can only fetch what the deployed site still serves, and the build removes published and old reels from the deployment, so use `/api/yt-backfill?episode=N` (it reads the repo) for episodes.
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

## YouTube text and recurring failures (David, 3.11.2026)
- **YouTube titles and descriptions must not contain `<` or `>`.** YouTube rejects them with "invalid video description" (episode 52 stopped the whole upload queue on `Settings > Personalization > Memory`; 16 queued files had them). `studio/app/api/yt-backfill/impl.ts` now swaps them for `›` / `‹` on upload (PR #546). In new `channel/episode-NN-youtube.txt` files write the path with `›` or "then" instead of `>`. Instagram and the site accept `>`.
- **Standing order: when something fails because of a cause that will keep recurring (a platform rule, a character, a quota, a format), fix the root in the code, write the rule here the same day, and tell David in one line.** Do not just patch the single episode that hit it.
- YouTube uploads have a rolling 24-hour limit, not a reset at a fixed hour (3.11: 13 uploads at 00:18 UTC, still blocked at 08:48, uploads worked again at 00:41 on 4.11, then blocked after 10). Run the backfill about 25 hours after the last batch, not at 08:20 UTC; the Vercel cron at 08:20 UTC therefore mostly hits the limit. `/api/yt-backfill` and its daily 08:20 UTC cron stop on it by design; an upload that returns "exceeded the number of videos" is not a bug.

## Phone notification when a reel is ready (David, 25.10.2026)
When a reel is ready (check.sh passed, merged, deploy verified), send a real phone notification with the PushNotification tool: one line, the episode number and that it is ready. Do this for every new reel. The studio's own "reel ready, not published" reminder pushes were removed the same day at his request (they were not built well); do not re-add them without asking.

## Claude may read the studio (David, 25.10.2026)
The studio is gated against the public, not against Claude. When David has given the PIN in the chat of the current session, read real numbers with `POST /api/unlock` (json `{"pin": ...}`, keep the cookie) and then `GET /api/state` on https://www.actually-works.com. The PIN is never written into a file, a commit, a PR or a log. If no PIN was given in the session, ask for it once. Fields: `state.episodes[]` (views, reach, likes, saves, shares, publishedAtPrecise), `state.snapshots[]` (followers). Watch time and reach by follower type are NOT_AVAILABLE for this account.

## Whole frame alive, no wasted space (David, 9.11.2026: "you always forget this, don't forget")
- The main visual (screen/card/panel) is ENLARGED to fill the usable area (x 65-1015, y 269-1248), not a small block in the top with empty space below. No empty zones inside the safe box. Do NOT fill space with extra decorations: scale up what matters, and keep the whole picture moving. Blind readers flagged ep88 frame 0 for exactly this (panel small, bottom empty).
- Compaction: after every context compaction, no detail from David's messages may be lost: before a long stretch, write his standing instructions of the session into CLAUDE.md or the episode plan file, and re-read them after compaction.

## We build virality, not videos (David, 9.11.2026)
- Next videos need OVERALL 85-95/100 (honest, blind panel). If the honest score is below that, DO NOT make the video: report what was tried and why it falls short. "I don't need a video if you can't do it properly: the goal is going viral, not producing a video."

## Every reference reel: how do WE reach its level, faceless and our way (David, 9.11.2026)
- Whenever David sends a reel as a reference, analyse it AND answer: how do we reach that level of virality in this exact form, faceless and in our own format (drawn UI, calm cloned voice, no face)? Name what makes it spread, what we can copy structurally, what we cannot (face, trend, account size) and what the faceless version looks like beat by beat, with an honest score. Never stop at a description of the reel.

## Hook is visual first, little text (David, 9.11.2026)
- The hook must be mostly VISUAL: far less text, never more than 3 lines of text on screen at once. The idea has to be understood from the picture and motion, with the text only naming it. Check this on every frame 0 and every title card (this overrides any earlier frame that carried long headlines).

## Reference set = the 3 most viral episodes only (David, 9.11.2026)
- For judging what works and for planning new videos, the ONLY episodes that count are the 3 most viral ones, listed in `channel/canon-top3.md` (episodes 86, 80, 82 by Instagram views; database in `channel/episodes-database.json`). All other published episodes are forgotten as evidence, style, hooks or results; they stay only as a topic list in `channel/topics-covered.txt` so a topic is not repeated. Do not cite them when analysing or advising.

## Content funnel (Roni via David, 9.11.2026)
- Every video idea carries a funnel stage: TOP (viral formats, 80% of videos), MID (for our curious-about-AI audience, trust and value), LOW (CTA-heavy, needs a real offer). Think in the funnel whenever ideas or videos are prepared. Details and the rules per idea: `channel/content-funnel.md`.

## Think in formats, not clips (Roni via David, 9.11.2026)
- Every video is an episode of a named, numbered FORMAT with a locked template and one variable slot (the topic). Design the format first, then the episodes. Spec and candidates: `channel/formats-2026-11-09.md`.

## It must NOT look AI or Claude-like (Roni via David, 10.11.2026)
- Roni's central point: our videos look too AI, and viewers are tired of that look; it is a main reason they do not go viral. Clean drawn cards, flat clip-art, light base with lime accent and generic gradients are the 'AI/Claude look'. New videos must look REAL and handmade: real photographs, real textures (paper, grain, halftone), real logos and screenshots, unusual fonts. The reference for the look is the torn-paper collage reel DeJ_gTHs-FB. This overrides the drawn-UI/light-base style rules above for new videos until David says otherwise.

## Instagram caption limit (10.11.2026)
- Instagram refuses a caption over 2,200 characters ("The caption was too long": episode 88's 2,251-character caption failed at publish time). Check `wc -m channel/episode-NN-caption.txt` is under 2,200 BEFORE shipping an episode. YouTube text has its own limits (no `<` or `>`).

## Speak in the present tense (Roni via David, 10.11.2026)
- Spoken lines, captions and chat talk too much in the past tense. Use the present tense ("Facebook looks through your photos", "AI does this now") in scripts, hooks and captions; past tense only when the claim is truly about something that already happened (a test we ran, a dated announcement).

## When a reference link will not open, try again and use the skills (David, 10.11.2026)
- A link David sends (Instagram, TikTok, YouTube) is never "unreachable" after one failure. Retry: (1) run `pip install -q -U yt-dlp`, then `yt-dlp` again (the `video-download` skill has the recipes), at most a few tries a few minutes apart, because Instagram rate-limits anonymous requests per IP and the same link can work on the next try (DfiCR8sqgXi opened on retry); (2) Firecrawl does not support Instagram; try Exa or the playwright tools for the page text; (3) only after all of that say plainly what failed. Never analyse a reel that was not actually seen. Download into the scratchpad `refsN/<id>/`, never into the project.

## The surprise comes first in the hook (David, 10.11.2026, after episode 88)
- The word that carries the surprise or the threat sits in the first 3 words of the first sentence ("Your photos. Facebook is looking."), and the first sentence is about 4-5 words. Episode 88 opened "Facebook can look through photos you never posted." and "never posted" only came at the end: David saw it underperform (about 23 views early on; one episode, a hypothesis, see `content-memory.md`). Check every new hook against this before building.

## Duplicate check comes BEFORE the first idea is shown to David (10.11.2026)
- Before proposing any topic or prompt, grep `channel/topics-covered.txt` (and `content-memory.md`) for its keywords and say what was found. On 10.11 I proposed "What do you know about me? / ChatGPT Memory" as a new idea; it was already episodes 13, 52, 70 and 84. David: "you forgot our old videos." A proposal that has not passed this check is not shown. The proven winners (86, 80, 82) are a chat AI doing something odd in a short test, and episode 86 is a numbered series ("Can it keep a secret? #1"): extending a proven format with a new subject comes before inventing a new topic.

## The goal is virality, the score is only a label (David, 10.11.2026, overrides the 85/90 gates above)
- David: "the goal is virality, not the score." The hook/virality/overall scores (85, 90) no longer block building or publishing a video. Our own validity test (24 episodes, Spearman -0.23) showed my scores do not predict views, so they cannot be a hard gate. Keep writing honest scores and predicted views as labels, log them against the real 48 h / 72 h numbers in `channel/score-calibration.md`, and never inflate a score.
- What still blocks a video: fabrication, copyright or platform-rule risk (e.g. re-posting another account's artwork, flipped or retexted), a claim we did not test presented as a result, and comprehension: a blind reader must understand what the video is about from frame 0 (a blind reader who "would not stop scrolling" is a finding to fix if cheap, not a veto).
- Publish as numbered experiments: each experiment states what we test, and the real numbers decide what we repeat.

## Screen recordings from David: check the contrast first (David, 11.11.2026)
- Every time David sends a screen recording (ChatGPT dark mode or any app), measure the text/background contrast of the key lines BEFORE building, and remind him that it may need a lift (ask him if it is unclear). iPhone dark-mode recordings come out dimmed: on episode 92 the text peaked at 129/255 (a normal iPhone shows about 236) and the WCAG ratio was 3.8 on the user bubble, 5.4 on replies, 3.6 in the input box; after the fix 11.0, 18.1 and 10.4. David approved the lift ("if it still looks real") and said the result is much better.
- How: one gentle monotone curve, identical for R, G and B, blacks stay black, no tint, glow or sharpening; lift the bubble fill slightly. Check full-size frames that it still looks like a real recording, not retouched, and report the before/after ratios. Also speed the typing (about 6x plateau with eased ramps, letters still appear one after another, typos pass fast), but never paste text in instantly: the visible typing is what shows the chat is real.

## Trial Reels, Vercel build limit, Meta AI (David, 11.11.2026)
- **Trial Reels (Instagram's own Help Center, read 11.11.2026):** need a public account; professional (business or creator) 200+ followers, personal 1,000+; an account that is not eligible for recommendations loses them (check Account Status in the settings). A trial reel is shown to non-followers only, does not appear in the public profile until "Share to everyone" (profile, Reels tab, the reel, View insights), shows Views/Likes/Comments/Shares within 24 h, and should be a NEW reel (re-sharing known content can get limited reach). The "Trial" switch is in the Instagram APP's share screen; no source confirms it on the desktop website (David's PC "Create trial reels" entry opened a normal upload and published a normal reel; on his phone the switch did not appear even after an app update: cause unknown, his account is professional with 225 followers). Do not post the same video as trial and as a normal reel on the same day: graduate the trial instead.
- **Trial through the API (merged, PR #579, opt-in):** `POST /api/instagram/publish {"episode":N,"trial":"MANUAL"}` (or "SS_PERFORMANCE") sends Meta's `trial_params`; the trial is recorded in the episode `notes` as a `TRIAL ...` line, the row stays `testing`, no Facebook post, a second trial for one episode is refused. Same publish permission as a normal post, no token change needed (Meta developer docs). Graduating has no API: by hand in the app. Not yet proven on his account: the first call shows whether it is eligible.
- **Vercel build rate limit (11.11.2026):** the free plan stopped production deploys with "Deployment rate limited, retry in 24 hours" after the day's merges and a PR preview build. Every PR or merge to main costs a build: bundle changes into ONE merge per day, do not open PRs only to look at them, and after a merge check the Vercel status on the merge commit (a failed one deploys with the next successful commit). Upgrading to Pro lifts it (costs money: ask first).
- **Meta AI (David's in-app assistant) as a collaborator:** it has real read access to the account's insights (its numbers matched the studio), but it cannot hear audio (it said "no voice" on files that had the voice), it scores the same file 58-92 on different days, it sometimes reviews an older version than the one sent, and it invents chat lines ("You gave me a second chance and I STILL chose 100" as a ChatGPT reply, "I actually tried this yesterday and ChatGPT gave me 47 steps"). Rules: verify every quoted line against the real recording, never add an invented claim, keep David's first name out of published videos unless he says, keep real-chat openers (its own data: reels opening on a real chat keep viewers), and do not chase its scores: real 48 h numbers decide. When David pastes its notes, send agents to apply the sensible parts and report what was rejected and why.

## "Miki style" is the name of the style (David, 11.11.2026)
- The drawn style of episode 89 is called **Miki style** from now on. It is NOT the generic light-and-lime drawn cards of the other episodes: it looks higher quality, and in practice viewers watch it more (89: 600 views, 440 reach, 11 saves vs 0-2 saves on the other recent episodes; one episode, a hypothesis). New videos use Miki style unless David says otherwise; this sits next to Roni's "must not look AI" rule (10.11), and David's choice decides. Build recipe: `video/ep89c/`.

## Every rule David says gets saved the same day (David, 12.11.2026)
- "Every rule I tell you, save it." When he gives a rule or preference, write it into this file (or the file it belongs to) in the same turn, with the date, so it survives a new session. No waiting to be asked.
- **Numbering (12.11.2026):** the dog-and-cat reel is not a numbered episode (files parked in `channel/parked-dogcat/`, not deleted). The essay-flagged-as-AI reel is episode **93**; its build folder is still `video/ep94/` (internal name; `video/ep93/sfx` belongs to episode 89, keep it).
- **Music rules experiment (12.11.2026, one week):** see `channel/experiments.md`. The rules came from Meta AI as a hypothesis (it cannot hear audio, and judged "Hip Hop 03" by its name only); they are tested, not law. Each episode logs track, type, measured level and views in `channel/music-notes.md`.
- **Trial Reels are David's to post by hand when he chooses (12.11.2026):** he may publish a trial earlier than scheduled; before any API trial or scheduled publish, check with him that he has not already posted it by hand. The studio PIN is never saved anywhere: he gives it in chat each time it is needed.

## Times to David are always Belgium time (David, 12.11.2026)
- Every clock time in a message to David is Belgium time (CET, UTC+1 in winter; CEST, UTC+2 in summer), never UTC. Convert before writing. UTC only inside files and commands when a tool needs it. Example: the Vercel limit ends about 02:36 UTC on 13.11 = about 03:36 Belgium time.

## Trial-first pipeline (David, 12.11.2026)
- **The plan (his words, saved):** from now on a new reel goes out as a TRIAL first and is moved to everyone ("Share to everyone") about 3 days (72 h) later, so the profile never goes empty: we also keep posting regular reels to the profile until there is always a reel that has already had its 3 days in trial. Trial reels first, regular reels continue in parallel, until the queue is full. It is a TEST, not a proven method: the first trial (ep91) got only about 130 views on Instagram (about 350 with Facebook), and he took it out early; how trials work and how the algorithm treats a reel after "Share to everyone" are still unknown. Measure it (see `channel/experiments.md`, 12.11.2026) before trusting it.
- **His hypothesis (not a fact):** reels that already proved themselves (over 1,000 views) would explode more as trials and then add the followers' views after graduation. Caution written next to it: re-posting an already published reel as a trial is a duplicate of a reel on the profile; Instagram's Help Center says a trial should be a NEW reel and re-sharing known content can get limited reach. So the plan is to apply the winning FORMAT to NEW topics, not to re-upload old reels, unless David decides otherwise after seeing data.
- **Graduation has no API** (by hand in the app). After David says a trial is posted, schedule a phone reminder (`send_later` + PushNotification) for 72 h later, and write `TRIAL-MANUAL <date time>` into the episode notes; when he graduates it, `TRIAL-GRADUATED <date>`.

## Choose what is VIRAL, not what is new; rotate the AI (David, 12.11.2026)
- "Don't look at what is new, look at what is viral." Topic choice starts from what already spreads (our own winners' FORMATS, and reels with a high outlier multiple), not from a feature announcement. A new-feature explainer is the weakest class we have (explainers: median 237 views, see `channel/score-calibration.md` recalibration 12.11).
- **Rotate the subject AI:** Claude, ChatGPT, Gemini, Meta AI, and general AI topics in turn, never the same product twice in a row if avoidable; each new reel should carry more interesting content than the last. The proven series format ("Can it keep a secret?") rotates its AI naturally.
- **The ig-* skills (installed 12.11.2026 in `.claude/skills/`, source and rules in `.claude/skills/ig-SOURCE.md`):** `ig-caption` (shows what the feed shows before "... more", lints the caption; works, ran on ep94), `ig-human` (strips AI-sounding wording), `ig-reel` (hook formulas, `hookscore.py`, `beats.py`), `ig-viral` (outlier multiple = views / that account's own median), `ig-audit`, `ig-profile`. **Measured on our own reels: `hookscore.py` does NOT predict our views (Spearman -0.23, n=8: it ranked "AI broke your app? Git brings the file back" 81 and "ChatGPT, don't tell my teacher!" 49).** Use it as a checklist, never as a gate. Our own `export/check_caption.py` stays.

## Brand direction, AI hot radar, news reels (David, 13.11.2026)
- **Goal right now: followers and very large reach** ("tens of millions of views"); money later (systems for companies; earning from the reels themselves is an open question, not researched). His full brand answers: `channel/positioning-2026-11-09.md` (block of 13.11.2026). The channel covers EVERYTHING about AI, from self experience, not one product.
- **Tone: exciting / enthusiastic**, in the direction of @juanbergman; reference accounts @mavgpt, @tylermommsen, @eilon.grouper, @juanbergman (all four are face brands; research in `channel/brand/brand-research-2026-11-13.md`). The cloned voice is capped by its calm reference clip: say so, and ask for a more energetic reference recording when it matters.
- **Logo:** v1 (check card / aw / switch / stamp) rejected as "not professional at all"; do not iterate on it. v2 directions (tick ligature, highlight A, wink; black/white + signal yellow #FFE600, Archivo Black) are in `channel/brand/logo-v2/`. Nothing goes on the profile or the app until David picks; app/site rebrand = ONE merge after the choice. No trademark or similarity search has been done yet: do it for the chosen mark.
- **AI hot radar (scheduled task "AI hot radar", every 2 days at 07:19 Belgium, a fresh read-only session each time):** finds what is hot in AI in the last 48 h, checks primary sources, checks `topics-covered.txt`, appends up to three ranked topics to `channel/hot-radar.md`, pushes a notification. It never builds, publishes or merges. After the first week tell David what it cost and whether to keep the cadence.
- **News reels are an occasional EXPERIMENT, not the base** (about 1 in 5): hot-AI-news reels may need a different, more news-like reel form; test it now and then and log it in `channel/experiments.md`. David: if a format shows virality of 90/95+ we move the branding toward it. Best case: a hot topic PLUS our own real test of it.
- **Wordmark rule (David, 13.11.2026):** the wordmark with one word in white and the second word inside a filled coloured block on black reminded him of the Pornhub logo: "not good at all". NEVER put a word inside a filled coloured box or bar (any colour, dark or light background), in the logo, the site, or reel titles. Yellow may be the swipe on the A mark or a thin underline stroke, not a box around a word. Check every new brand asset for resemblance to well-known logos BEFORE showing it. Wordmark options without a box: `channel/brand/wordmark-v3/`.

## Voice: avoid R clusters, keep it tight (David, 13.11.2026, after episode 96)
- In the cloned voice the R in clusters (THR, TR: "three", "trust", "Anthropic") sounds a bit Russian and gets swallowed. Swap such words in scripts when a plain alternative exists ("twenty years" instead of "2003", "let" instead of "trust"); a brand name can stay on screen and be spoken as "the company". The accent check does not catch this: his ear decides.
- No needless gaps: build the voice with `--gap 0.06 --long 0.15 --max-speedup 1.45` and short lines; the hook must be punchy (three short beats worked: "Black hole math. Stuck for twenty years. AI finished it.").
- Hook choice: a stake over time ("stuck for twenty years, AI finished it") beat a flat report ("this AI solved two physics problems") with both blind readers. Compare hook options with blind agents before building.
- Voice re-rolls: check each line against its own text with Whisper and re-roll only the lines that are wrong (roll script pattern of ep96 v7), never all seeds at once.

## Logo status (David, 13.11.2026, night)
- Round 3 (mascots: A-character, raised eyebrow, plug, red button) is REJECTED: "the earlier examples were much better". The live candidates are the three v2 directions in `channel/brand/logo-v2/` (A = AW with the check, B = A with the marker swipe, C = the wink); he leans to A (the AW). Full kits for all three, dark and light, go in `channel/brand/logo-kit-ABC/`. No word inside a filled box (rule above). Nothing goes on the profile, site or app until he picks; then ONE merge.
- **Logo decided: direction A (the AW with the yellow check), David, 13.11.2026.** Dark or light is still open (profile picture, site, app); decision image in `channel/brand/logo-A-final/decide-dark-vs-light.png`. After he decides: final images, then update the profile on Instagram, YouTube and Facebook (he uploads; give him the files and the steps), and the site + studio rebrand in ONE merge. Site audit to fold into that merge: `channel/brand/site-audit-2026-11-13.md` (public Hebrew on unknown URLs, no follow action, phone header, gradients).
- **Decided (David, 13.11.2026, about 03:30 Belgium): logo A with the DARK avatar** (white AW, yellow check, black disc) for the profile picture on Instagram, YouTube and Facebook; files in `channel/brand/logo-A-final/` (avatar-A-dark-1080.png, YouTube banner and Facebook cover, dark). The site is probably LIGHT and comes after the profile is done. Profile tips from the Israeli Instagram-tips creator he follows: `channel/brand/ig-profile-tips-2026-11-13.md` (take only what fits an English, worldwide, faceless AI channel).
- **Rebrand shipped (David, 13.11.2026, PR #582, merge cef0e233, deploy success):** public site LIGHT, studio stays DARK (his decision), logo A, black/white + signal yellow, Archivo Black headings, English 404 for unknown public paths, no Hebrew on public pages. Notes: `channel/brand/rebrand-notes.md`. Still open: studio pages behind the PIN were never seen visually; episode 89's stored title starts with "TITLE: " (needs a one-field fix in the studio data, David's go-ahead not yet given in so many words); five solid black buttons remain (he has not said whether buttons count as "a word in a filled box"). Flow (his app) IS on the App Store: https://apps.apple.com/us/app/id6807543350.

## New formats, not the same chat test again (David, 13.11.2026, said twice)
- David is bored of the "AI does something odd in a short chat test" reels (secret, caving, deleting, ghost) and of explainers: "you keep coming back to reels we already did, it is getting boring." Do NOT propose that class as the default next video, even though it has the best median (580). The data rule "extend a proven format" does not override this: bring genuinely NEW formats, with proof from the outside (small accounts with huge AI videos, per the 13.11 virality model in `content-memory.md`), checked against `topics-covered.txt` first. A chat test may still be proposed only as one clearly marked option when it adds something new.

## Contest reels need virality design, not just the content (David, 13.11.2026, after episode 97 v3)
- A real, good result is not enough: "the content is maybe good, the virality is not." Showing four equal boxes one after another is boring. Design the viral mechanic before building: a reason to guess or choose (comments), one big stage instead of a grid, a reveal that saves the best for last, a payoff in the last second. Have a strategist agent redesign the concept first (done for ep97: `channel/episode-97-v4-plan.md`), then a builder agent codes it.
- A hook that STARTS with a digit ("4 Claude AIs...") reads as a list item ("4.") and not as part of the sentence; put the subject first or spell it so it flows ("Claude has four models. See the difference."). The hook must say the point (what is compared) in one clear short sentence, not a long label.

## Pre-publish checklist from the 2027 algorithm reel (David, 13.11.2026; HYPOTHESIS, not measured by us)
Source: reel DfrsIhMtotI by @ekkobuild (talking head, no data, no source; analysis and Instagram cross-check in `channel/algorithm-2027-notes.md`). His claims: context (viewers scroll if they do not understand), promise-and-payoff (foreshadowing), simplicity (one theme) drive reach; daily posting, trending sounds, a twist and authenticity do not move a single video. Instagram's own words found: Mosseri 22.1.2025 "top three signals ... watch time, likes and sends"; percentage watched and raw seconds watched both count (25.2.2025); sends per reach "in my experience" correlates most with reach; hashtags do not significantly increase reach; no statement found on the first 3 seconds.
Check every reel before publishing, in this order (J = my judgement before, M = measured after): 1 subject clear at frame 0 and in the first second (J); 2 a promise in the hook paid off by about 10 s (J); 3 one theme only, no side claims (J); 4 retention at 48 h: skip rate and average watch (M); 5 a named person plus a reason to send it (J, then sends per reach, M); 6 a reason to watch to the end or twice (J); 7 likes per reach (M); 8 one saveable card (M); 9 original, full resolution, no watermark (J); 10 short caption. Not worth effort for reach: trending sounds, daily posting for its own sake, hashtag research, twist quotas. Our own 48 h / 72 h readings decide whether any of this holds.
