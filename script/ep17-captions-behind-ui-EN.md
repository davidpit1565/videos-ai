# Episode 17 — "Your captions are behind Instagram's interface"

**Format:** 45s reel (no long cut — one number, one fix)
**Blocked on:** nothing. The measurement already exists.

**The claim, which is measurable and almost universally got wrong:** on a 1080×1920 reel,
Instagram draws the username, caption, audio label and buttons over the **bottom 35% — 672
pixels.** A subtitle placed there is behind the interface. Ours sat **413px inside it** until
it was measured.

---

## The narration

| Line | On screen |
|---|---|
| Your subtitles are behind the app. | A real reel, subtitle half-hidden by the UI |
| Not *near* it. Behind it. | The same frame with the UI region shaded |
| Instagram draws its own interface over the bottom 35% of your video. | `672px` counted up from the bottom |
| That's 672 pixels of a 1080 by 1920 frame. | The safe box drawn: `x 65–1015, y 269–1248` |
| Top 14% goes too, and 6% of each side. | Three more edges shade in |
| Mine were 413 pixels inside it. | Our own before-frame, measured |
| Not guessed — measured, with a script. | The checker's output, real |
| One line of CSS moved them out. | `bottom: 24cqw` → `63cqw` |
| Every platform publishes these numbers. Almost nobody reads them. | The safe box, clean |
| Check yours. It takes a minute. | CTA |

## Why this one is a reel and not a long cut

It is a single number and a single fix. Stretching it to ten minutes would be padding, and the
measured data says short-form on this channel earns its place through **saves per view** — a
number someone saves to check their own video against. A 45-second reel with one number on
screen is more savable than a tutorial about it.

## The number on screen at the end

```
safe box   x 65–1015, y 269–1248
ours was   y 1571–1661
inside by  413px
```

## The honest note in the middle

The watermark is *supposed* to be down there. Anything purely decorative can live behind the
interface — that is why the checker has a `data-decor` flag. The rule is about text the viewer
has to read, not about every pixel.

Without that line the video overstates its own rule, and someone will move a logo for no
reason.

## Not in this reel

- TikTok's numbers. They differ, and mixing two sets of figures in 45 seconds produces neither.
- The checker's source. That is episode 20.
