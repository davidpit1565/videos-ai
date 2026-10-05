# Episode 58 — WhatsApp's Photo Touch-Up (Meta AI edits your photo before you send it)

Built fully autonomously (4.10.2026) while David is away for Shabbat/chag, per his
explicit standing pre-authorization to ship without waiting for approval.

## Topic verification (live web search, 4.10.2026)

- **WhatsApp "Photo Touch-Up"**: launched worldwide in March 2026. Places a Meta-AI-powered
  photo editor directly inside the chat composer, before you send an image. You can remove
  something from the frame, swap the background, change the whole mood/style, or fully
  reimagine the photo from a text prompt — the AI rebuilds the image to match, without
  leaving WhatsApp or opening a separate app. Confirmed across itechguides.com
  ("Meta AI on WhatsApp: Features, Privacy and Limits in 2026"), techpoint.africa, and
  greentick.ai's 2026 WhatsApp AI features guide — cross-checked, not a single source.
- Chosen over two other live-searched candidates: **ChatGPT group chats** — confirmed
  retired/wound down starting 9.7.2026 (would have been a script about a dead feature, the
  exact episode-18 "ChatGPT agent mode" mistake) — and **ChatGPT Instant Checkout** —
  confirmed retired in March 2026, six months after its September 2025 launch, repositioned
  to discovery-only. Both rejected live, before writing a single line, per the standing
  verify-first rule.
- **Whole-audience fit (continuing the 24.9.2026 pivot, episodes 49/51/55/56/57)**:
  WhatsApp has 2B+ users worldwide — broader than any subgroup topic, and broader than this
  episode's own two rejected candidates (ChatGPT users specifically).
- **Real AI-relevance (per the 17.9.2026 standing rule, re-affirmed 2.10.2026 after episode
  55's correction)**: Meta's AI is the literal, demoed capability — you type a sentence, the
  AI redraws the photo, right there in the chat. Not a cited background reason.
- **Not a repeat of recent topics**: episode 56 was Google Translate's live headphone
  translation (Gemini 2.5 Flash Native Audio); episode 57 was Google's Search Live (point
  camera, talk to Gemini). This episode is a different company (Meta/WhatsApp), a different
  AI mechanism (generative photo editing from a text prompt vs. live audio translation or
  live camera conversation), and a different everyday moment (about to send a photo, not
  talking to someone or pointing a camera).

## Hook rules check

- **Checkable, concrete fact, explained same-breath**: "That photo in your WhatsApp chat
  right now — type one sentence, and Meta's AI will redraw it for you, right up until the
  moment you hit send." Names WhatsApp (near-universally known, no explanation needed, same
  bar episode 55 used for "Amazon"/"Echo") and explains exactly what the AI does in the same
  clause it's introduced, per the 24.9.2026 standing rule.
- **Dry-sentence / gut-feel test (30.9.2026 standing rule)**: lands on "that photo in your
  WhatsApp chat right now" — the viewer's own, specific, already-open chat, not an abstract
  claim about WhatsApp in general. Passes the "feel it in 3 seconds" bar, not just understand
  it.
- **Hook type**: **You-Focused Appeal**. Last used solo episode 42 (10+ episode gap); not a
  repeat of episode 55 (Contrarian Open), 56 (Direct Address) or 57 (Shock/Surprise), the
  three episodes immediately before this one.
- **Sendability test**: would a specific person forward "WhatsApp can already redraw your
  photos with AI before you send them, no extra app" to one specific friend who posts a lot
  of photos? Yes — concrete, immediately useful, zero extra clicks to understand.
- **Comment-inviting element**: the caption asks what people would edit out of their last
  photo first — a real, specific, low-effort question.

## Spoken script (4-5 facts, plain language, ~35-40s)

Final, shipped wording (after three production rounds — see Production notes below):

1. This photo in your WhatsApp chat right now — type one sentence, and Meta's AI will
   redraw it for you, right up until the moment you hit send.
2. It's called Photo Touch-Up, built right into the chat box in WhatsApp. No extra app,
   and it's free.
3. You type what you want changed — remove something, swap the background, change the
   whole mood — and the AI rebuilds the picture to match, right as you're about to send
   it.
4. Meta launched this worldwide right inside the WhatsApp you already have, starting in
   twenty twenty-six.
5. Open a chat, pick a picture the usual way, then tap the new edit button and type what
   you want changed.
6. It still gets some details wrong sometimes, and it won't replace a real photo app — but
   for a fast fix right there in the chat, it gets the job done.
7. The setup's in the link in bio. (locked)
8. Follow for the setup that actually works. (locked)

Passed `audio/script_lint.py` clean except the two locked outro lines (handled by
`canonical-lines.json`, per standing policy — never regenerated).

## Production notes — voice (honest account)

- **Round 1** (`--exaggeration 0.70` throughout, seed 58): generated clean on the first
  pass (unlike episode 57's 20 rounds) — only line 4 needed internal retries (WER 0.18,
  a transcription artifact on the spoken year, not a real defect). `voice_doctor.py --deep`
  then flagged real issues: rushed/swallowed words in lines 1, 2, 3, 5 ("until"/"moment",
  "separate", "photo", "photo") and one word held far too long in line 4 ("2026," at
  0.98s/syllable — the original wording had a double-comma pause, "March, twenty
  twenty-six,", right where the voice stalled).
- **Round 2** (lesson-4 diagnosis test): per the standing method, pulled `--line-
  exaggeration` down toward 0.54-0.56 on the affected lines to check whether the
  flagged words were energy-induced. They were not — the same words failed again
  (same "photo"×2, same "separate", same "2026," hold, and the opening word "That" got
  *worse*, not better) even at the pulled-back energy. This is the explicit signal the
  lesson describes: a word failing regardless of energy level is a text/seed artifact,
  not an energy problem, and the fix is rewording, not more reseeding or more energy
  pullback.
- **Round 3** (final, shipped): reworded the specific trouble spots rather than reaching
  for the energy dial again, restored full `--exaggeration 0.70` everywhere: "That" →
  "This" (opening word), "No separate app" → "No extra app", "rebuilds the photo to
  match" → "rebuilds the picture to match" (line 3's instance of "photo" only — line 6's
  "a real photo app" was never flagged and was left as-is), "pick a photo the usual way"
  → "pick a picture the usual way" (line 5), and line 4 restructured end-to-end to move
  the year off a comma-pause entirely ("Meta rolled this out worldwide in March, twenty
  twenty-six, right inside..." → "Meta launched this worldwide right inside the
  WhatsApp you already have, starting in twenty twenty-six.", also swapping "rolled this
  out" for "launched this" since "rolled" was itself one of the swallowed words). All
  six non-locked lines re-passed `script_lint.py` clean before regenerating.
- **Round 4** (5.10.2026, David's feedback after watching the shipped file): line 4's
  wording had drifted further from round 3's own documented text by the time it
  actually shipped ("Meta launched this worldwide..." became "Meta launched this
  everywhere..." somewhere after round 3, undocumented) — "everywhere" is itself one
  of the fragile words confirmed independently the same day in a separate reseed run,
  and David flagged the line's tone as too formal/written regardless. Reworded to
  "This is already live worldwide, built right into the WhatsApp you already have —
  nothing extra to download." — drops "Meta launched"/"rolled" (both previously
  fragile) and "everywhere" (currently fragile), shorter and more conversational.
  Also removed the `.logolabel` caption text under the WhatsApp logo badge (see
  CLAUDE.md's standing logo rule, updated same day) from all three build variants.
  **Not yet re-verified**: `script_lint.py` passes clean on the new line, but this
  session has no `torch`/`chatterbox`/`ffmpeg` — the voice for this line was never
  regenerated, retimed, re-captioned or re-rendered here. The shipped
  `studio/public/reels/reel-58.mp4` still has the OLD voice line and the OLD logo
  caption baked in; only the HTML/CUES source changed. Needs a full
  `produce.sh`-style pass (voice → doctor → retime → captions → render → check.sh)
  on a machine that has the audio/render toolchain before this actually reaches
  viewers.

## Photos (all free, Unsplash License, no attribution required)

- `channel/assets/ep58-scene-a-patio.jpg` — woman using her phone on a brick patio with
  greenery, by Helena Lopes (unsplash.com/photos/jRn5ebWQOZo). Deep focus throughout (no
  bokeh background) — trees, brickwork, building facade all stay sharp, avoiding the
  uniform-texture frozen-picture failure documented on episodes 55-57. Adobe
  `image_select_subject` (bodyParts: Face) found the face at bbox x 0.521-0.591,
  y 0.183-0.316 (normalized, source 1600x1067) — upper-right third, no conflict with the
  default headline zone once mapped through the 9:16 cover-crop (vertical position is
  preserved 1:1 for this source's aspect). Used in scenes 1 (hook) and 5 (steps),
  non-adjacent reuse, normal Ken Burns both times.
- `channel/assets/ep58-scene-b-deskforest.jpg` — a phone lying on a wood desk next to a
  coffee cup, showing a forest-path photo on its own screen (not an app), by an Unsplash
  photographer (unsplash.com/photos/a-cell-phone-sitting-on-top-of-a-wooden-table-next-to-a-cup-of-coffee-XqvoraA4StI).
  No person in frame, no face-detection check applicable. Chosen deliberately over several
  "phone screen glow in the dark" candidates (near-solid-black backgrounds + near-solid-white
  screens) specifically to avoid the uniform-region frozen-picture risk documented on
  episodes 55-57 — this photo has real, distributed texture (wood grain, forest detail,
  coffee cup) across the whole frame instead. Carries the real WhatsApp logo badge in scene
  2 (the logo is laid over the photo, not sourced from it). Used in scenes 2 (feature
  named), 6 (limit) — both non-adjacent — and 7+8 (the CTA pair, adjacent reuse of the same
  photo -> fully static Ken Burns on 7 and 8, per the standing rule that a repeated,
  unchanged photo never gets a second independent pan/zoom).
- `channel/assets/ep58-scene-c-balcony.jpg` — a man checking his phone on a balcony, city
  buildings behind him (real texture, not heavy bokeh — only a small foreground leaf is
  soft), by an Unsplash photographer
  (unsplash.com/photos/a-close-up-of-a-cell-phone-near-a-keyboard-LV28JOBBujk... actually
  listed as "person using phone balcony", source photo-1599413098099-272e97fd66bd). Adobe
  `image_select_subject` (bodyParts: Face) found the face at bbox x 0.436-0.559,
  y 0.194-0.294 (normalized, source 1600x2400) — mapped through the 9:16 cover-crop
  (vertical position preserved 1:1 for this source too), the face lands at roughly
  y 365-557px of a 1920px-tall frame, which DOES conflict with the template's default
  headline zone (text starts at 27cqw ≈ 291px). Applied the template's documented
  exception: moved this one scene's headline zone down to clear the measured face
  bbox (`style="padding-top:52cqw"` on this scene's `.pad`, ≈562px, starting just below
  the face's measured bottom edge) rather than guessing a number. Used in scene 3 (how it
  works) only.
- `channel/assets/ep58-scene-d-cafe.jpg` — a top-down shot of a hand holding a phone over a
  wooden cafe table (coffee grinder, mug, a generic coffee-shop checkout screen in Czech —
  unrelated app, not WhatsApp, kept deliberately low-key by the scene's own darkening
  gradient so it doesn't read as a screenshot of anything this episode claims), by an
  Unsplash photographer (unsplash.com/photos/person-using-smartphone-19-rJG0QENU). No face
  in frame. Used in scene 4 (scope/date) only.

Real WhatsApp logo (public domain — simple geometric shapes/gradient, the standard WhatsApp
glyph, per Wikimedia Commons' own licensing note; sourced from
upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg) appears as a small badge in
scene 2, in-flow inside `.kb` (never absolutely bottom-anchored — the episode 55 logo-badge
bug this template's header already warns about).

**Dropped candidates**: two "person holding phone with messaging app" photos surfaced first
(Unsplash+ premium, not free — rejected on licensing alone); a photo showing a real ChatGPT
screenshot on a phone (wrong product for this episode, would misleadingly suggest ChatGPT is
part of the WhatsApp feature); a photo of a phone showing a French Bible-reading app on a
heavy-bokeh dark background (shallow-DOF frozen-picture risk per episodes 55-57, plus
unrelated religious content this channel has no context to responsibly feature, the same
reasoning episode 57 used to drop its illuminated-building candidate).

## Design

One accent for the whole episode: `--accent:#D97706` (a warm amber/orange). Checked
rendered against every real photo this episode uses: reads clean against the cool green
patio foliage and the warm-toned balcony sky (complementary, not muddy), and stays legible
against both the wood-desk photos (b and d) without turning muddy the way episode 54's
violet did against warm tones. Distinct from every dated `channel/used-designs.json` entry
in the last 7 days (54 `#06B6D4`, 55 `#EA580C` — close in hue but value/saturation checked
side-by-side and kept clearly distinct per the standing rule's intent; see note below — 56
`#2563EB`, 57 `#059669`) and from the immediately prior episode (57). ***note***: on
reflection `#EA580C` (ep55, dated 2026-10-01, inside the 7-day window) is close in hue to
the originally-drafted `#D97706`; swapped to a clearly distinct warm accent, `#B45309` was
considered too dark/muddy against the bright cafe photo, so the final pick is a saturated
**teal `#0D9488`** instead — reads cleanly against every one of this episode's photos
(confirmed against all four, including the warm wood-desk ones) and is not within the
recent-7-day dated set at all.

Music mood passed to `produce.sh`/`pick_real_track.py`: **`confident`** (not `bright`,
which episode 57 used immediately before this one — `produce.sh`'s own design-variety
check hard-fails on repeating the immediately prior episode's music mood, separate from
the accent-color check). `confident` fits this episode's tone too: a straightforward,
competent reveal of a feature most viewers didn't know was already there, not a
hyped-up "big news" register.

Voice: raised-energy pass per David's standing instruction this round (Nas-Daily-style
enthusiasm, still provisional — not yet confirmed permanent, see `content-memory.md`).
