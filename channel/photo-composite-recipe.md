# Photo-composite recipe — real full-res photo backgrounds, verified this session

David's own words on the current state: "much better!!" — confirmed, real approval of
this whole direction, not a tentative "keep trying." This file documents what got built
and verified this session, matching the style/rigor of `channel/motion-recipes.md`, so a
future episode built from `video/reel-template-photo.html` doesn't have to rediscover any
of it.

**Status: the direction is approved and productionized.** A real word-overlap bug found
in `export/safe_check.js` this round is fixed and re-verified (see "The word-overlap bug,
fixed" below). The real starter template is `video/reel-template-photo.html`, wired to the
real `export/karaoke.py` pipeline, not hand-authored placeholder timing. Nothing here
picks which real episode ships first in this style — that is a separate content-demand
decision (`channel/demand-report.md` + `channel/content-memory.md`), not this file's job.

---

## 1. The fixed headline zone — why it's fixed, not per-photo

Round 1 of this style let the headline land wherever each photo's own clutter happened to
leave room (26cqw / 29cqw / 76cqw padding-top depending on the scene). That read as
sloppy scene to scene, even though each individual placement was defensible on its own
photo. The fix: **every scene shares the SAME zone** — `.pad{padding:27cqw 10cqw 0}` (≈
291.6px top padding on 1080×1920, just inside the platform's own 269px top-safe line),
`h2{font-size:8.4cqw}` — verified consistent across three real, genuinely different
photos this session (a cool night phone shot, a warm daylight kitchen shot, a warm evening
living-room shot). The photo's own gradient (see `.photogradient` below) absorbs each
photo's different brightness/clutter in that band; the TEXT POSITION does not move to
chase it.

**The one documented exception, and how it stayed honest instead of silently moving the
zone:** the evening/voice photo's face sat 259px inside this exact zone (measured via real
Adobe face detection, not eyeballed) in an earlier round. Rather than quietly shrinking or
relocating the zone for that one photo, the photo itself was fixed — Adobe's
`image_generative_expand` (outpaint 280px on the top edge) + `image_crop_to_bounds` pushed
every real pixel, including the face, down 280px inside the frame, and real face detection
was re-run on the RESULT to confirm the conflict was actually gone (22px of clear margin,
not assumed). See `video/test-photo-composite-v4.html`'s own header for the full worked
pipeline. **This is the standing rule: if a real photo's subject conflicts with the fixed
zone, fix the photo (re-generate/re-crop, then re-verify with real detection), don't move
the zone or the fix stops meaning anything the next time a different photo has the same
problem.**

---

## 2. One accent color per episode, not one per scene — the real comparison behind it

Round 4 of the combined three-scene demo (`video/photo-composite-demo.html`) originally
switched the accent hue per scene, matching each photo's own palette (`--ember` for the
cool night photo, `--rust` for the warm daylight photo, `--rose` for the warm evening
photo) — the idea was that each photo's own mood deserved its own matching color.

**David's direct correction, made by actually watching the file across its own scene
transitions, not assumed either way:** watched back to back as one continuous video and
compared directly against a real shipped episode (any `reel-*-kar.html`; see
`channel/used-designs.json` — every real episode locks ONE brass/ember pair for its entire
runtime, however much its own scenes' moods vary), the per-scene switch reads as three
different videos stitched together, not one branded piece. The accent stops meaning "this
is @actually_works.ai" and starts meaning "whatever this scene's photo happened to be." A
real side-by-side render (same 3 scenes, same transitions, only the accent color changed
to a single `--brass` throughout) held up fine against all three photos — cool night-blue,
warm daylight kitchen, warm lamp-lit living room. **Chrome (progress bar, tap-to-play
ring, scrubber) AND the headline/caption accent both stay ONE color for the whole
episode's runtime**, same as every real shipped episode.

Per-scene color variety is still fine ACROSS separate episodes/demos — a different episode
can pick a different accent — just never switching mid-video. `video/reel-template-photo.html`
wires this in as `--accent` (a single CSS custom property), used by every scene's `.box`,
`.subs b.on`, `.prog`, and `.tapover`/`.ctl` chrome. Set it once per episode.

---

## 3. The mandatory face/subject-detection QA gate

**This is not optional — same standing as `export/check_setup_guide.py`'s gate in
`export/produce.sh`.** Every real photo used in this style must go through real face/
subject detection and `export/detect_photo_safe_zone.py` before its headline/caption
placement is finalized. The real sequence, from that script's own header:

```
1. mcp__Adobe__adobe_mandatory_init()                       # once per conversation
2. python3 export/detect_photo_safe_zone.py prepare <photo.png>
   -> prints the exact next Adobe upload + image_select_subject calls to run
3. (an operator/agent turn) upload the photo, run image_select_subject,
   get back a real normalized {x,y,w,h} face/subject bbox
4. python3 export/detect_photo_safe_zone.py recommend <photo.png> --bbox x,y,w,h
   -> real, PIL-measured brightness per candidate zone, a gradient-peak-alpha
      recommendation, and a plain flag if the subject conflicts with the fixed
      headline zone or the bottom:62cqw caption anchor
```

No guessing, no "looks about right" — every number in the recommendation is measured
against the actual photo's real pixels (PIL grayscale brightness) and the real detected
bbox, not assumed. If the recommendation reports a conflict, see section 1 above for the
real fix used this session (generative expand + re-crop + re-verify), not a workaround
that skips the check.

---

## 4. Real logos/screenshots for named products — how the standing rule applies here

CLAUDE.md's standing rule from this session: any named product or feature gets a real
logo or a real screenshot, never an invented or generic stand-in graphic. Applied to this
style specifically: **the photo IS the visual evidence** — a real phone screen, a real
laptop, a real device — so this style already satisfies the rule by using real photography
instead of a mocked-up UI card. The rule still applies inside a photo-composite scene the
same as anywhere else: if a scene's copy names a specific product (an app, a specific AI
tool), any UI chrome or logo shown ON SCREEN inside that photo (a phone's home screen, an
app icon visible on a laptop display) must be the real thing, not a redrawn approximation
— the same standard `hyperframes-animation`'s own rules and this repo's existing episodes
already hold synthetic-style scenes to.

---

## 5. Hybrid scenes — synthetic + photo-composite in one video, verified mechanically sound

`video/hybrid-synthetic-photo-test.html` proved this session that mixing the channel's
regular synthetic (all-CSS) scene style with a photo-composite scene in the SAME video is
mechanically sound: the transition between the two reads clean, nothing about the zoom-
through transition (recipe 4, `MK.zoomThroughTransition`) breaks or looks inconsistent
crossing from a synthetic scene into a photo scene or back. This means a real episode does
not have to be ALL photo-composite or ALL synthetic — a photo scene can be dropped into an
otherwise-synthetic episode for the one moment that benefits from real photographic
evidence, and vice versa. Not yet exercised in a real shipped episode; verified as a
same-session technical proof only.

---

## 6. The word-overlap bug, fixed this round

`node export/safe_check.js` flagged a real bounding-box "overlap" (~108-110px) between the
last plain word before the hook's climax phrase (e.g. "reading" or "for") and the boxed
climax phrase itself, on every hook scene in this style where the climax phrase wraps
across two lines (`test-photo-composite-v3.html`, `-v4.html`, `photo-composite-demo.html`
all showed it).

**Root cause, found by measuring, not guessing:** `MotionKit.splitWordsSafe()` correctly
treats the climax phrase (`.box`) as one atomic unit for animation purposes — the same
reasoning `channel/motion-recipes.md` recipe 2 already documents for highlight bars
("never draw one box across a wrapped phrase"). But `export/safe_check.js`'s own overlap
detector was measuring that atomic unit with a single `el.getBoundingClientRect()` — which,
for an inline element that wraps across two real lines, returns the UNION of both lines'
bounding boxes. That union's x-range spans the full width of BOTH lines even though each
individual line only occupies part of that width, so the union rect reads as overlapping
a sibling word that shares only the FIRST of those two lines — even when the two elements'
actual glyphs never touch.

**Verified with real screenshots and per-fragment coordinates, not assumed:** captured
`video/test-photo-composite-v3.html` at the exact flagged timestamp (1.2s) and read each
word's real `getClientRects()` (one rect per rendered line, not the union). The boxed
phrase's line-1 fragment (`x495.9-939.2, y393.5-499.5`) sat entirely to the RIGHT of
"reading"'s rect (`x140.7-471.4, y392.4-500.9`) — a real ~24.5px gap between them, not a
collision — and the boxed phrase's line-2 fragment (`y502-608`) sat a full line below
"reading" with no vertical overlap either. The screenshot shows exactly what the numbers
say: "reading" and "more than" sit side by side on the same visual line with real
whitespace between them; there is no visible collision.

**The fix**, in `export/safe_check.js`: the clash (overlap-with-a-sibling) check now
compares `el.getClientRects()` — one rect per real rendered line — instead of the single
bounding-box union, exactly the same principle `buildHighlightBars()` already uses for
highlight bars in `export/motion-kit.js`. The safe-area (platform-UI-band) check is
untouched and still uses the full bounding rect, correctly, since a single wrapped line
poking past the platform's margin is still a real violation even if a sibling line is
clean — only the sibling-vs-sibling overlap check needed the per-line fix.

Re-ran `node export/safe_check.js` on all four files after the fix
(`test-photo-composite-v2/v3/v4.html`, `photo-composite-demo.html`): all four now report
"overlaps: none over 10px," with the two previously-flagged rows gone and no new ones
introduced. `video/reel-template-photo.html` (the new starter template) was also checked
clean end to end with placeholder content.

**A note on due diligence:** an earlier pass this session characterized this exact flag as
"confirmed real, not a measurement artifact" (distinguishing it from a DIFFERENT flag that
had already been dismissed as one). Re-measuring this round with per-fragment
`getClientRects()` and a real screenshot shows that characterization was itself
incomplete — this flag was the same class of union-rect artifact, just triggered by a
different element pairing than the one already dismissed. Recorded here plainly per this
repo's "measure, don't guess" rule, rather than smoothed over.

---

## 7. Not yet built — the honest gap

**Per-sentence / per-few-sentences photo swapping** — a different real photo landing on
each new sentence or two within a single scene, instead of one photo per whole scene — was
discussed this session but is **not implemented anywhere**, including in
`video/reel-template-photo.html`. Every scene in every file this session produced still
shows exactly one photo for its whole duration.

The honest cost, already established this session: building it for real means roughly
**4x the per-scene work** this recipe already documents per photo (source/license a photo,
upload it, run real Adobe face/subject detection, run `detect_photo_safe_zone.py`,
re-derive the gradient peak and Ken Burns direction from the real measured result)
multiplied by however many sentences a scene would need to cover instead of once per
scene. This is a real, deliberately-not-yet-built future idea, not a hidden limitation —
flagging it here so a future session doesn't assume it exists because the rest of the
style is this far along.

---

## Files this recipe covers

- `video/test-photo-composite-v2.html`, `-v3.html`, `-v4.html` — the three individually
  approved single-scene proofs (night/phone, day/laptop, evening/voice), each with its own
  photo, Ken Burns direction, and gradient re-derived from its own real measured pixels.
- `video/photo-composite-demo.html` — all three combined with zoom-through transitions,
  one accent color for the whole runtime (the round-5 correction above).
- `video/hybrid-synthetic-photo-test.html` — the synthetic+photo mixing proof (section 5).
- `export/detect_photo_safe_zone.py` — the mandatory QA gate (section 3).
- `export/motion-kit.js`'s `MK.kenBurns()` — the photo drift motion helper.
- `export/safe_check.js` — the overlap-detection fix (section 6).
- `video/reel-template-photo.html` — the real starter template a new episode copies,
  wired to `export/karaoke.py`'s real Whisper-aligned captions (not hand-authored
  timestamps), the fixed headline zone, the one-accent rule, Ken Burns, and per-scene
  zoom-through transitions resolved the way `photo-composite-demo.html` fixed (never
  independent pairwise calls — see that template's own `renderScene()` comment for the
  clobbering bug it avoids).
