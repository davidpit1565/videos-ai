# Prompt for ChatGPT — visual design directions for our Instagram Reels channel

I run an AI-content Instagram channel called **Actually Works** (handle: `@actually_works.ai`,
with the underscore). The public site is `https://actually-works.com`. Please look at both
the Instagram profile and the site yourself before answering, so you're reacting to the real
current look, not just my description of it.

## What the channel is

Short vertical (9:16, 1080x1920) Instagram Reels, 30-75 seconds each, about AI tools and AI
news. Each episode: a hook line, 1-3 sourced facts/stats shown as on-screen cards, a single
"payoff" (usually a copy-paste prompt or a concrete technique), then a call-to-action and
outro. Every episode also gets a page on the site under `/e/<number>` with a written setup
guide.

## The current visual system, exactly as it is today

- **Background**: near-black (`#050709` / `#0A0E14`), with soft large blurred color blobs in
  the background and a subtle film-grain overlay and vignette.
- **Typography**: `Archivo` (weight 800-900) for headlines, `Assistant` for body text/ledes,
  `IBM Plex Mono` for small citation labels (source name + date, uppercase, letter-spaced),
  `Inter` for minor UI text.
- **Two-color accent system per episode**: every episode picks a "brass" (primary accent)
  and "ember" (secondary accent) hex pair, plus a "mood" word (e.g. urgent/tense/confident/
  drive/bright/neutral) that also picks the background music track. These are meant to vary
  episode to episode.
- **Structure/motion**: word-by-word animated headline reveals, citation cards that fade/scale
  in as white cards with a colored top border, "scoreboard" rows for stat comparisons (a
  label + a big number, with a glow/shake effect on the "worse" number), a hero quote card
  style for the main payoff, zoom-through transitions between scenes (camera push effect),
  and word-by-word animated captions ("karaoke" style, 2-3 words per chunk, spoken word lit
  up) sitted in the bottom third of the frame.
- **Hard layout constraint** (Instagram's own published safe-area numbers for 9:16 at
  1080x1920): no text or key visual element may sit in the top 14% (269px), bottom 35%
  (672px), or within 6% (65px) of either side — the usable box is x: 65-1015, y: 269-1248.
  The bottom third specifically is reserved because Instagram's own UI (username, caption,
  audio label, buttons) draws over it.

## The actual problem

The "brass"/"ember" color pair is supposed to be a source of variety, but it keeps landing
in the same narrow hue family — mostly crimson-red plus amber/gold — especially recently.
Here are the last dozen episodes' actual accent pairs, in order:

- ep41: `#22C55E` / `#A855F7` (green/purple)
- ep42: `#3B82F6` / `#F87171` (blue/coral)
- ep43: `#8B5CF6` / `#F97316` (purple/orange)
- ep44: `#0EA5E9` / `#EC4899` (sky-blue/pink)
- ep45: `#10B981` / `#EF4444` (green/red)
- ep46: `#FACC15` / `#4338CA` (yellow/indigo)
- ep47: `#14B8A6` / `#FB7185` (teal/rose)
- ep48: `#7C3AED` / `#F59E0B` (purple/amber)
- ep49: `#C2410C` / `#0891B2` (burnt-orange/cyan)
- ep51: `#E11D2E` / `#F59E0B` (crimson/amber)
- ep52: `#DC2626` / `#FBBF24` (crimson/amber)

Episodes 48, 51, and 52 in particular all read as "red + amber/gold" despite technically
different hex values — a viewer scrolling the feed sees the same two-color feeling three
times in the last five episodes. The automated check that's supposed to catch repetition
only compares each new episode against the immediately previous one, so it never catches
this kind of cluster-level repetition across several episodes.

## What I actually want from you

I'm not looking for a new color pair — that's a band-aid. I want a small number (3-5) of
genuinely different **visual/structural design directions** we could build future episodes
in — different enough in typography, color philosophy, layout metaphor, and motion character
that they'd feel like different "outfits" for the channel, not just a palette swap on the
same skeleton. They should still:

- Work within the safe-area constraint above (this is non-negotiable — Instagram's UI will
  cover anything in the bottom third).
- Read clearly at small size on a phone screen, with heavy word-by-word captions overlaid.
- Feel premium/intentional, not like a generic "AI content" template — look at the actual
  feed and site first so you're not just describing something we already do.
- Be buildable as an HTML/CSS/JS reel (we build these as static HTML pages, animate with
  vanilla JS, and render to video with a headless-browser frame-capture pipeline — so avoid
  proposing anything that depends on a specific design tool's runtime, keep it to real CSS/
  web-standard techniques).

For each direction, describe: the core visual idea in one line, the color/typography
approach, how motion/transitions would feel different from what we have now, and why it
would still work for a 30-75 second vertical video with dense on-screen captions.
