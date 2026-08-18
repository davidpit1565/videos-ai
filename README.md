# Universal AI Engine — video tutorial production package

A complete, beginner-oriented tutorial explaining how to install and use the Universal AI
Engine Custom Instruction in ChatGPT. Target runtime **~14:00**, 13 chapters.

## What's here

```
brand/house-style.md         ← the channel's visual identity. Read this first
video/short-instagram.html   ← the 62-second Reel, playable in a 9:16 frame
video/tutorial.html          ← the 13:40 long-form tutorial, playable with chapters
script/short-instagram-EN.md ← Reel narration, timings, caption copy, hook A/B tests
script/narration-EN.md       ← long-form narration with pause marks + voice direction
storyboard/storyboard.md     ← 13 scenes: visual beats, on-screen text, motion, timings
storyboard/screen-recording-guide.md  ← exact shot list, capture settings, privacy pass
storyboard/visual-prompts.md ← image / motion / voice generation prompts
captions/universal-ai-engine-EN.srt   ← timed subtitles for the long-form
assets/custom-instruction-EN.txt      ← the paste-ready instruction
assets/custom-instruction-EN-optional-v2.txt  ← optional hardened variant
assets/README-instruction-variants.md ← what v2 changes and why
assets/guaranteed-vs-model-behaviour.md ← the accuracy guardrail for the limitations section
```

Everything is **English only**.

## The two playable videos

Neither of these is a storyboard — both run on a real timeline and can be screen-recorded
straight to a finished cut.

**`video/short-instagram.html`** — the 62-second Reel in a true 9:16 frame. Burned-in captions
sized for muted, one-handed viewing, a cursor that walks the real setup path, and the brass wipe
between each of the seven sections. Record the frame at 1080×1920 to export.

**`video/tutorial.html`** — the 13:40 long-form cut. 13 chapters with seeking, a scrubber,
live typing, a building comparison table, an orbiting capability cloud and toggleable captions.
Keyboard: `space` play/pause, `←`/`→` skip 5s.

**The mock interfaces are illustrations, not screen recordings.** They're built to read as real
— the interface uses Inter while all graphics use Archivo, which is the detail that sells it —
and they're labelled on screen. For a produced video, swap them for real captures per
`screen-recording-guide.md`.

## If you're producing the real video

1. Record BLOCK I-1 in the screen-recording guide **first** — the "before" shot needs Custom
   Instructions switched off, and you can't easily get it back once you've saved them.
2. Record everything else in one session so the theme and window size stay consistent.
3. Cut to the storyboard timings; the `.srt` files already match those timings and can be
   loaded straight into Premiere / Resolve / CapCut as a subtitle track.
4. Re-time the captions to the final voice-over — the current timings are distributed by
   character count within each scene, which is close but not frame-accurate.
5. Hebrew voice-over: record a native speaker rather than synthesising. The script is full of
   English loanwords (ChatGPT, SaaS, red team, SWOT) that Hebrew TTS still mishandles.

## The one thing not to soften

Scene 12 draws a line between what Custom Instructions **guarantee** (your text is stored and
delivered into every new chat — mechanical, reliable) and what is merely **very likely** (that
the model follows every line every time). Keep that distinction if you re-edit. The language to
use, and the language to avoid, is in `assets/guaranteed-vs-model-behaviour.md`.
