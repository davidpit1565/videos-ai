# Universal AI Engine — Scene-by-Scene Storyboard

**Format:** 16:9, 1920×1080 (export 4K if possible), 30 fps.
**Also cut:** 9:16 vertical version from S1, S3, S6, S10 (see `vertical-cutdowns.md` section at end).

## Global look & feel

| Element | Spec |
|---|---|
| Background | Near-black `#0B0D10` with a very slow-moving radial gradient (indigo `#4F46E5` → teal `#14B8A6`, 6% opacity, 40s loop) |
| Primary accent | Indigo `#6366F1` |
| Secondary accent | Teal `#2DD4BF` |
| Warning / limitation accent | Amber `#F59E0B` |
| Text | `#F4F6F8` primary, `#9AA4B2` secondary |
| Latin type | Inter — Bold 700 for titles, Regular 400 for body |
| Motion language | Ease-out cubic, 400–600ms. Elements rise 24px and fade in. Never bounce, never spin. |
| Transitions | Cross-dissolve 300ms between scenes; hard cut inside a scene |
| Music | Minimal ambient / soft arpeggio, −24 LUFS under VO, ducks 6dB on narration |
| Screen recordings | Rounded corners 16px, subtle drop shadow, 1px `#FFFFFF14` border |
| Cursor | Enlarged 140%, soft indigo glow, smoothed motion, click = ripple ring |
| Callouts | Rounded rect outline, 3px indigo, animated draw-on over 350ms, plus a short label chip |
| Zoom style | Slow digital push-in to 130% on the UI element being discussed, 800ms |

**Accessibility:** all on-screen text ≥ 34px at 1080p. Never put text over a busy screenshot without a 60%-opacity scrim behind it.

---

## S1 — HOOK · 00:00–00:30

**Visual beats**
1. `00:00` Cold open on a real ChatGPT screen recording: someone types *"how do I grow my business?"* and gets a bland 5-bullet answer. Desaturate to 30% colour. Small grey label bottom-left: `BEFORE`.
2. `00:08` Text slams in over it, big and centred: **"This is 10% of what it can do."**
3. `00:12` Split screen. Left keeps the grey bland answer. Right fades up in full colour — the same question answered with assumptions, trade-offs, risks and a recommendation. Label right: `AFTER`.
4. `00:20` Both sides fly out. Title card assembles: **UNIVERSAL AI ENGINE** with subtitle *One paste. Every chat. No shortcuts.*
5. `00:26` Under the title, three chips animate in one by one: `No software` · `No plugins` · `No commands`.

**On-screen text**
- `This is 10% of what it can do.`
- `BEFORE` / `AFTER`
- `UNIVERSAL AI ENGINE` / `One paste. Every chat. No shortcuts.`

**Audio:** music starts on the "AFTER" reveal (00:12), not before. Silence under the cold open makes it land.

---

## S2 — WHAT THIS ACTUALLY IS · 00:30–01:35

**Visual beats**
1. `00:32` Three red-struck cards fly in and get crossed out one at a time as narration hits each: `New AI model` ✗ · `Software to install` ✗ · `A secret hidden mode` ✗.
2. `00:42` Cards clear. **Animated metaphor — the assistant and the sticky note.** Simple flat-illustration loop: a desk, a figure at it. Each "day" a speech bubble repeats the same long request; the day counter ticks Day 1 → Day 2 → Day 3 and the figure looks progressively worn out. Keep it light and funny, 4 seconds max.
3. `00:58` A yellow sticky note drops onto the desk with a soft thud. The repeated speech bubbles vanish. Day counter now spins fast — Day 4, 5, 6… 40 — and the figure stays calm. Caption under: **Written once. Read before every conversation.**
4. `01:12` Cut to a clean diagram: a rounded box labelled **CUSTOM INSTRUCTION** with ~40 small capability pills orbiting slowly around it (writing, first principles, SWOT, red team, Pareto, Feynman…). Pills are too many to read individually — that's the point, it should feel abundant.
5. `01:26` Three of the pills light up indigo and snap into the centre box. Caption: **ChatGPT picks. You don't.**

**On-screen text**
- `NOT a new AI model` / `NOT software` / `NOT a hidden mode`
- `A Custom Instruction = a note pinned to the desk`
- `Written once. Read before every conversation.`
- `~40 thinking methods` → `ChatGPT picks. You don't.`

---

## S3 — SHORTCUTS VS. AUTOMATIC · 01:35–02:50

**Visual beats**
1. `01:37` A "cheat sheet" card flies in, styled like the ones people share online: a long list of `/deep`, `/godmode`, `/critic`, `/simplify`, `/eli5`, `/redteam`… Deliberately overwhelming. It keeps scrolling past the bottom of frame.
2. `01:50` The card tilts and a red question mark stamps over it. Text: **"Which one does my question need?"**
3. `01:58` Split the screen into two labelled lanes that will run in parallel for the rest of the scene:
   - Left lane `MANUAL MODE`: user thinks (thought bubble with a confused list) → picks a command → types `/deep should I build this app?` → gets a good answer. Show a small stopwatch and a "you had to know this" friction badge.
   - Right lane `ENGINE MODE`: user just types `should I build this app?` → three capability pills (`assumptions`, `risks`, `decision`) fly in automatically from off-screen and merge into the message → good answer.
4. `02:30` Both lanes finish. The answers look equally good. Then the left lane's friction badges stack up and glow amber: `must memorise` · `must self-diagnose` · `must be an expert already`.
5. `02:42` Right lane collapses to one line of text, centred: **You ask normally. It decides how to think.**

**On-screen text**
- `MANUAL MODE` / `ENGINE MODE`
- `"Which one does my question need?"`
- `must memorise · must self-diagnose · must already be an expert`
- `You ask normally. It decides how to think.`

**Note to editor:** keep the left lane sympathetic, not mocking. Slash-command systems work; they just put the burden on the user.

---

## S4 — HOW IT ACTUALLY WORKS · 02:50–04:05

**Visual beats**
1. `02:52` The core diagram of the video: **three stacked layers**, built bottom-up as narration names each one.
   - Bottom, grey, locked padlock icon: `1 · OpenAI's own rules` — subtitle *You can't change this.*
   - Middle, indigo, glowing, editable-pencil icon: `2 · YOUR Custom Instructions` — subtitle *This is the only layer we touch.*
   - Top, white: `3 · The message you just typed`
2. `03:20` Camera pushes into layer 2. It unfolds into the actual instruction text, scrolling slowly, with key phrases highlighted as narration reaches them.
3. `03:32` **The wrap animation** — the single most important visual in the video. Show the user's short message `should I build this app?` as a small white card. Then a large indigo bracket animates around it, and the instruction text fills the space around the card. Caption: **Your question didn't change. Its instructions did.**
4. `03:48` Transition to the **9-step pipeline**. Nine connected nodes flow left to right, lighting up in sequence: `understand → decompose → assumptions → challenge → alternatives → risks → improve → decide → next step`. On mobile-safe framing, wrap to two rows.
5. `04:00` The whole pipeline dims and collapses behind a single clean answer card. Caption: **It runs this quietly. You just get the result.**

**On-screen text**
- `Layer 1 · OpenAI's rules (locked)`
- `Layer 2 · Your Custom Instructions (you edit this)`
- `Layer 3 · Your message`
- `Your question didn't change. Its instructions did.`
- The 9 pipeline labels
- `It runs this quietly. You just get the result.`

---

## S5 — WHERE TO INSTALL IT · 04:05–05:05

**Visual beats**
1. `04:07` Warning card first: a chat window with the instruction pasted into the message box, then a red ✗ and the words **"Not here."** Beneath it: *Works in one chat. Gone tomorrow.*
2. `04:16` Cut to green ✓ version: the Settings screen. **"Here."** Beneath: *Works in every new chat. Permanently.*
3. `04:24` Begin the real screen recording walkthrough. **Numbered step badges** appear top-left and persist: `STEP 1 of 4`.
   - `STEP 1` — cursor moves to profile picture / initials. Callout ring drawn around it. Zoom 130%.
   - `STEP 2` — menu opens, `Settings` highlighted, click ripple.
   - `STEP 3` — `Personalization` highlighted in the settings sidebar.
   - `STEP 4` — `Custom instructions` row highlighted, click, panel opens.
4. `04:50` Picture-in-picture: the same four steps on **mobile**, played at 1.5× in a phone frame in the lower-right corner, so app users aren't lost.
5. `04:56` **Amber honesty card** slides up over the recording: **"OpenAI redesigns this screen often."** Below: *Names change. Look for the screen with empty boxes asking what ChatGPT should know about you.* Show two labelled thumbnails side by side: `Personalization` and `Customize ChatGPT`.

**Screen-recording instructions:** see `/storyboard/screen-recording-guide.md` — record at 2560×1440, 100% browser zoom, light or dark theme consistently, blur the sidebar chat titles.

**On-screen text**
- `✗ Not here — works in one chat only`
- `✓ Here — works in every new chat`
- `STEP 1 of 4 · Profile picture` … `STEP 4 of 4 · Custom instructions`
- `Screen names change. Look for the empty boxes.`

---

## S6 — THE EXACT SETUP · 05:05–06:40

**Visual beats**
1. `05:07` The Custom instructions panel, full frame. Each field gets a soft outline and a floating label as narration names it: *nickname* · *what you do* · *traits* · *anything else*.
2. `05:20` The large free-text field pulses indigo. Big arrow + chip: **PASTE HERE**. Secondary grey chip under it: *(if your version differs, the big empty box is the right one)*.
3. `05:30` Paste animation — text fills the box. Then, instead of watching it scroll silently, **cut to a side panel** where the instruction is broken into labelled blocks that highlight in time with the VO:
   - `ROLE` — *You are my Universal AI Engine*
   - `THE CORE RULE` — *Automatically choose the best methods. I should not need shortcuts.*
   - `THE MENU` — the 40 capabilities, shown as a dense grid that fills in fast
   - `THE GUARDRAIL` — *Select only what is useful. Do not overthink simple requests.*
   - `THE RECIPE` — the 9 steps, mini version of the S4 pipeline
   - `WRITING RULE` — *preserve meaning, improve clarity, flow, tone*
   - `HONESTY RULE` — *never invent facts; separate facts, assumptions, uncertainty*
   - `LANGUAGE RULE` — *respond in my language; understand Hebrew in Latin letters*
   - `THE GOAL` — *best answer, not showing the methods*
4. `06:00` **The guardrail demo** — a 6-second inset gag proving why one line matters. Left: without the guardrail, *"what's the capital of France?"* returns a comically long scrolling analysis. Right: with it, *"Paris."* Caption: **This one line keeps simple things simple.**
5. `06:18` Back to the panel. Two red-outlined callouts, drawn in sequence, each held 4 seconds:
   - **① Toggle ON** — ring around the *Enable for new chats* switch, animated off→on.
   - **② Press SAVE** — ring around the Save button, click ripple, then a green success toast.
6. `06:34` Full-frame reinforcement card: **"No Save = nothing happened."**

**On-screen text**
- `PASTE HERE`
- The nine block labels above
- `This one line keeps simple things simple.`
- `① Toggle ON` / `② Press SAVE`
- `No Save = nothing happened.`

---

## S7 — TESTING THAT IT WORKED · 06:40–07:30

**Visual beats**
1. `06:42` Two rule cards snap in: **`1 · Open a NEW chat`** (show clicking the new-chat button, old chats greyed out behind) and **`2 · Don't test with something trivial`**.
2. `06:54` Screen recording: fresh chat, typed live at readable speed — *"Should I quit my job to work on my side project full time?"*
3. `07:02` The answer streams in. As each fingerprint appears, a **checklist builds down the right side**, each item ticking green with a soft chime:
   - ☑ States its assumptions
   - ☑ Argues both sides
   - ☑ Raises risks you didn't ask about
   - ☑ Ends with a decision + next step
4. `07:20` **Troubleshooting card**, amber: *Flat, generic, no assumptions?* → two bullets: `Toggle is off` · `You didn't press Save` → arrow back to the Settings screen thumbnail.

**On-screen text**
- `THE 4-POINT TEST`
- The four checklist items
- `Not working? → Toggle off, or you never pressed Save.`

---

## S8 — EXAMPLE 1: APP IDEA · 07:30–08:45

**Visual beats**
1. `07:32` Example counter chip, top-right, persists across S8–S10: `EXAMPLE 1 / 3`.
2. `07:34` Empty chat. Type live: *"I want to build an app that reminds people to drink water. Is it a good idea?"* Hold on the typed message. Overlay chip: **11 words. Zero commands.**
3. `07:44` Answer streams. As the response moves through each mode, a **capability pill flies in from the left margin and docks beside that paragraph** — this is the recurring visual device of the examples section:
   - `ASSUMPTIONS` beside the paragraph separating known from unknown
   - `COMPARISON` beside the competitor/existing-solution paragraph
   - `RISKS` beside the retention paragraph
   - `REFRAME` beside the narrow-audience suggestion
   - `DECISION` beside the recommendation
4. `08:24` The five docked pills detach and line up along the bottom as a summary bar. Caption: **You asked one question. It ran five methods.**
5. `08:34` Final beat — a grey card: **"Notice what it never said:"** followed by struck-through text *"I am now applying comparison, then risk analysis…"* Caption: **The goal is the answer, not the performance.**

**On-screen text**
- `EXAMPLE 1 / 3 · Evaluating an idea`
- `11 words. Zero commands.`
- Pills: `ASSUMPTIONS` `COMPARISON` `RISKS` `REFRAME` `DECISION`
- `You asked one question. It ran five methods.`

---

## S9 — EXAMPLE 2: SAAS OR MOBILE · 08:45–10:00

**Visual beats**
1. `08:47` `EXAMPLE 2 / 3`. Type: *"Should I build a SaaS or a mobile app?"* Chip: **Deliberately vague — like a real person asks.**
2. `08:58` Answer begins. First pill: `MISSING INFO` docks beside the paragraph naming the three deciding facts. Show those three as a small animated list: `Who pays?` · `Offline needed?` · `Businesses or individuals?`
3. `09:10` **Key teaching beat.** Big text over a dimmed screen: **"It assumes — and answers anyway."** Small print: *A useful advisor doesn't interrogate you first.*
4. `09:20` `COMPARISON` pill. Cut to a clean animated two-column table, built row by row — do **not** just film the chat text here, this is where a designed graphic earns its place:

   | | SaaS (web) | Mobile app |
   |---|---|---|
   | Build cost | Lower | Higher |
   | Time to first paying customer | Faster | Slower |
   | Approval gate | None | App store, days, can reject |
   | Ongoing maintenance | One website | Two phone platforms |

5. `09:40` `SECOND-ORDER EFFECTS` pill — the standout idea of this scene. Animate a small branch diagram: `Choose mobile` → `app store fees` → `forced update cycles` → `3 years of overhead`. Caption: **The consequences of the consequences.**
6. `09:52` `DECISION` pill. Recommendation card with the flip condition highlighted in teal: *"Go SaaS — **unless** you genuinely need camera, GPS or push notifications."* Caption: **It tells you when to change your mind.**

**On-screen text**
- `EXAMPLE 2 / 3 · A real trade-off`
- `It assumes — and answers anyway.`
- The comparison table
- `Second-order effects = the consequences of the consequences`
- `It tells you when to change your mind.`

---

## S10 — EXAMPLE 3: WHAT IS AN AI AGENT · 10:00–11:00

**Visual beats**
1. `10:02` `EXAMPLE 3 / 3`. Type: *"What is an AI Agent?"* Chip: **A knowledge question — no decision to make.**
2. `10:10` **Contrast beat.** The 9-step decision pipeline from S4 appears — then greys out and slides away, with a red ✗. Caption: **Correctly does NOT run the deep process.** This is the proof that the guardrail works.
3. `10:20` A different set of pills flies in: `EXPLAIN` `ANALOGY` `EXAMPLE` `LIMITATION` `CHECK UNDERSTANDING`.
4. `10:26` Animated side-by-side illustration — the clearest graphic in the video:
   - **Chatbot:** a speech bubble. One question in, one answer out. Static.
   - **Agent:** a figure that takes a task card, walks off, visits three labelled tool icons (search, browser, calendar) in sequence, and returns with a completed card.
5. `10:40` Concrete example card, two lines contrasting: *"Find me a flight"* vs *"Book me a flight — compare 4 sites, pick the cheapest with legroom, add it to my calendar."*
6. `10:48` Amber limitation card: **"One wrong step early ruins every step after it."**
7. `10:54` Split-screen recap of the whole examples section: same instruction block on the left; three completely different response shapes on the right. Caption: **Same instructions. Different thinking. Automatically.**

**On-screen text**
- `EXAMPLE 3 / 3 · Learning something`
- `Correctly does NOT run the deep decision process`
- `Chatbot: answers` / `Agent: does`
- `Same instructions. Different thinking. Automatically.`

---

## S11 — BEST PRACTICES · 11:00–11:55

**Visual beats**
Four numbered cards, each ~13 seconds, each with one small animation. Cards stack into a 2×2 grid at the end of the scene.

1. `11:02` **① Write like you talk.** Show a stiff over-engineered prompt being deleted character by character and replaced with a messy human sentence — which gets the better answer.
2. `11:15` **② New topic = new chat.** Show the new-chat button being clicked; a small badge reads *instructions load here*.
3. `11:28` **③ You can still override it.** Show typing `"shorter"` and the answer visibly contracting; then `"challenge that harder"` and it expanding. Caption: *It's a default, not a cage.*
4. `11:41` **④ Tell it who you are.** Same question answered twice, side by side — once with no context, once with *"I'm a student, solo, no budget."* The second answer is visibly more specific. Caption: *Two lines about you = a big jump in quality.*

**On-screen text**
- `① Write like you talk` `② New topic = new chat` `③ You can still override it` `④ Tell it who you are`
- `It's a default, not a cage.`

---

## S12 — LIMITATIONS · 11:55–12:55

**Visual palette shift:** drop the indigo accent to amber for this scene. Slightly cooler background. This signals "now we're being straight with you" and makes the honesty read as deliberate, not as a disclaimer dump.

**Visual beats**
1. `11:57` Three strike-through cards, same style as S2 but amber: `Not a new AI model` · `Not software` · `Doesn't make it correct`.
2. `12:12` On "check anything that matters": a small icon row — `dates` `numbers` `names` `legal` `medical` `money` — with a magnifying glass sweeping across. Caption: **Verify anything that matters.**
3. `12:24` **The most important graphic in the scene — the two-column guarantee split.** Build it as a balance/scale that settles, not a table that appears:

   | ✅ GUARANTEED (mechanical) | ⚠️ NOT GUARANTEED (model behaviour) |
   |---|---|
   | Your text is saved | That every line is followed every time |
   | It's delivered in every new chat | That the exact 9 steps always run |
   | It applies across web, phone, desktop | That tone and depth are perfectly consistent |
   | It persists until you change it | That it never misses a rule |

   Caption under: **Delivery: guaranteed. Obedience: very likely, not certain.**
4. `12:46` Final amber card: **"Applies to NEW chats — not old ones."** With a small icon row showing phone + laptop + desktop and the caption *Follows your account, not your device.*

**On-screen text**
- `NOT a new model · NOT software · NOT a correctness guarantee`
- `Verify anything that matters.`
- The guarantee split table
- `Delivery: guaranteed. Obedience: very likely — not certain.`
- `New chats only. Follows your account, not your device.`

---

## S13 — RECAP · 12:55–13:40

**Visual beats**
1. `12:57` Accent returns to indigo. A clean 5-step summary strip builds left to right, each step a tiny thumbnail of the actual screen from S5–S6:
   `Settings` → `Personalization` → `Custom instructions` → `Paste` → `Toggle + Save`
2. `13:08` Stopwatch graphic ticks to `00:90`. Caption: **That's the whole installation.**
3. `13:14` Return to the S2 orbiting-capabilities diagram, now with a green check on the centre box. Caption: **Every new chat, from now on.**
4. `13:24` Three final lines type themselves out, one per beat:
   `No shortcuts.` / `No commands.` / `Just ask like a human.`
5. `13:32` End card: the instruction block shown compressed on screen with a chip **"Full text in the description"**, plus a QR code to a copy-paste page if you have one. Subscribe / next-video button appears in the last 5 seconds.

**On-screen text**
- `Settings → Personalization → Custom instructions → Paste → Save`
- `~90 seconds. Once.`
- `No shortcuts. No commands. Just ask like a human.`
- `Full instruction in the description ↓`

---

## Vertical cut-downs (9:16, for Shorts / Reels / TikTok)

| Cut | Source scenes | Length | Hook line |
|---|---|---|---|
| A — "Stop typing /deep" | S3 (both lanes) + S8 (pills) | 45s | *"Everyone's sharing ChatGPT cheat sheets. You don't need one."* |
| B — "The 90-second setup" | S5 + S6 (sped 1.5×) | 60s | *"Paste this once. Every chat gets smarter."* |
| C — "It knows when NOT to think hard" | S10 (pipeline greying out) | 30s | *"The line that stops ChatGPT from over-analysing everything."* |
| D — "What nobody tells you" | S12 (guarantee split) | 40s | *"Custom Instructions are delivered. Obeyed is a different word."* |

For vertical: move all lower-thirds to the upper third (thumbs cover the bottom), increase text to ≥ 52px, and burn in captions — 85% of viewers watch muted.
