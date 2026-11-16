# Episode 99: opening design notes (15.11.2026)

Looked at frames 0, 0.5, 1 and 2 s of four reference reels David sent (scratchpad `refs10/`, read only) and of our own reels 86 and 89 (`origin/main:studio/public/reels/`). Nothing was copied 1:1: no frame, clip, layout or audio. These are observations by eye on downscaled frames, not measurements, except where a number is given for our own render.

## What is on frame 0, per reference
| Reel | Main object and size | Objects | Outline / shadow | Tilt | Background | Accent | Text on frame 0 |
|---|---|---|---|---|---|---|---|
| DfatglrzjiV (Graphify) | a plan card "OUT OF TOKENS 0%", about half the frame width | 2 (card + a green logo tile) | thick black outline on both; a soft oval ground shadow under the card | card about 15-20 degrees, tile about 20 | off-white paper with a fine dot grain, mostly empty | green tile, one orange word | the card's own words only; a 5-word caption bar arrives at about 0.5 s with one word in orange |
| DfSvS-CTqDA (9 repos) | a 3 x 3 grid of logo tiles, the grid about 80% of the width | 9 tiles + a small "0/9" strip | thick black outlines, hard offset shadows, each tile slightly off-square | 1-4 degrees each | off-white, dot grain | one orange star sticker, one hazard-tape strip | "0/9" only; caption bar at about 0.5 s |
| DfVPw9LTJEo (agents) | one orange block mascot, about 85% of the width | 1 + a small status pill | no outline (3D solid), soft floor shadow | none | white, tiled floor | the orange of the mascot | the pill only; caption bar at about 0.5 s |
| DbB-jGzxmjp (skit) | a stick figure at a laptop, about 60% of the frame height | 1 figure in a drawn room | thick ink outline on the figure, flat colours | none | a full drawn room | none | one caption bubble on top |
| ours 86 | a chat screen with a keyboard, full frame | many small parts | thin outlines | none | light | none at frame 0 | many small texts |
| ours 89 | a heavy two-word headline + a dark card | 3 | thin | none | light grid | none | headline |

Note on DbB-jGzxmjp: in its first 2 s the figure's head is a plain circle; I did not see a logo used as a head in the frames I looked at.

What the first frames have in common: one to three large things, a lot of empty light paper around them, thick black outlines, a tilt or a pose that says "something is happening", one accent colour, and almost no text before 0.5 s. Our reel 86 opens on a dense screen with many small parts; 89 opens on words.

## The five traits taken for the sword-duel opening
1. **Few, very large objects.** Three logo characters only; at frame 0 they span x 120-873, y 292-1206 (ink pixels measured on `ep99-v6.mp4`), each about 340-375 px tall.
2. **Thick ink outline + hard offset shadow.** Each logo sits on a white tile with an 8 px ink outline and a 10 px hard shadow in that brand's own colour (ink edge around it), ink arms and legs 14 px, bold white blades with an 8 px outline and a short swing trail, eyes sitting on top of the tile (the logo itself is untouched).
3. **Tilt and a mid-action pose at frame 0.** Gemini runs in at about -10 degrees, Meta AI at about +8, both blades raised; Claude on the right leans back, arms up, eyes wide. Nothing stands straight or still.
4. **Empty light paper, one accent per object, stickers used once.** The Miki paper background stays empty; no stickers at all in v6 (the hazard-tape strip of v5 confused the blind reader and was removed).
5. **No text.** Frame 0 and the whole duel carry no words: the logos name themselves. The first words on screen come with line 2.

Applied to the end scene as well: the same tiles as characters on a paper podium with ink outlines and hard shadows; the only texts are the facts (1 / 117 steps / same path / best possible 89; 3 / 171 steps; "in circles"; "stuck at start").

## Deliberately not copied
- The caption bar under the picture with one coloured word (their signature layout), the token card, the 3 x 3 grid and its shatter, the 3D block mascot, the room drawing.
- Star stickers (David, 15.11: no stars), any frame, clip, timing or sound of the references.
- Their text amount: we went lower (zero on frame 0) because David asked for no text there.

## Kept from our own rules
Miki style paper and ink, real logos (sources in `video/ep99/hf/assets/logos/SOURCES.md`), safe area x 108-972 / y 269-1248 with the right band at x 864, cartoon only (two halves slide apart on a clean cut, a white flash, motion lines; no blood), and the truth: Claude is whole again in line 2 and stands on step 3 at the end (out in 171 steps).

## v6 note (blind reader on v5, 15.11.2026)
Stop 3/5 on v5: read as a three-way fight, characters small and top-left, thin swords, the checkered strip confusing, the Meta AI mark a guess. v6: bigger characters filling the box, attackers left and Claude right, bold blades, eyes (angry brows on the two, wide eyes on Claude), strip removed, logo on the tile enlarged (112 to 130 px). The Meta AI mark is the real one from meta.ai (the ring); Meta's infinity mark is the company logo and is not in the repo: not swapped without a sourced file and David's word.

## v7 note (David on v6, 16.11.2026)
The opening looked dry and a bit empty. v7 adds ONE text item on top: the hook itself in the headline treatment of episode 89 (Inter Display Black caps, the small words in Medium at half size, every word ghost grey until it is spoken, then ink; colour only, no box). The duel sits under it; on "killed": flash, a short screen shake, the two halves fly apart and turn, orange debris, motion lines; the paper slides a little under the run. Frame 0 measured on `ep99-v7.mp4`: x 112-865, y 298-1224.
