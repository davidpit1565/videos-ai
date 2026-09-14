# Tool UI kit — real apps, not our own invented box

Decided 14.9.2026, after comparing episode 1 (the one video that already recreated
ChatGPT's real settings menu — 666 views, our best performer) against episodes 32/33's
generic dark "termbox," which invents its own labels ("EXECUTION STATUS") instead of
showing what the real app actually looks like. Faceless-content research says the same
thing independently: the product should be the star, not our illustration of it.

`export/tool-ui-kit.css` gives every episode a faithful recreation of the specific tool
it's about, instead of one dark box reused regardless of subject. Each kit is self-
contained — its own background/ink/accent — so it drops into any episode's brass/ember
scene chrome without a color clash; the outer frame stays "actually works," the inner
screen looks like the real product.

## Sourcing — every color below is cited, none guessed

**n8n** (`.tuk-n8n`) — **corrected 14.9.2026.** The first version used n8n's brand
guidelines (n8n.io/brandguidelines: Mandy pink/red `#EA4B71`) plus a docs page
describing a light grey dotted-grid canvas with white node cards. David flagged the
whole kit as looking fake while watching it get built, so this time two real, current
screenshots were fetched and actually viewed (`blog.n8n.io/how-to-build-ai-agent/`,
image URLs under `storage.ghost.io/.../content/images/2025/04/`), and the colors below
sampled directly from those PNGs with PIL — not read off a docs illustration. The real
editor is **dark**: canvas `#3A3A3A` with a lighter dot grid, node cards `#494A4B`
with light text, sticky-note annotations in an olive-brown (`#5A4F25` body,
`#746855` banner) with a bold white heading and orange-red links, node parameter
panels on the same dark canvas with lighter `#5B5C5F` input/dropdown fields. The brand
pink still shows up — active tabs, links, the trigger icon — just not as the canvas
or card color the first version assumed.

**ChatGPT** (`.tuk-chatgpt`) — still reused from episode 1's own build
(`video/reel-01-v25.html`), which recreated the real Settings menu and Custom
Instructions panel before this kit existed and was itself checked against the live
app before shipping. **Not re-verified this round** — WebFetch on
`help.openai.com/en/articles/8096356` and `openai.com/academy/personalization/` both
403'd; no new screenshot was actually viewed, so this entry still rests on episode 1's
original check, not a fresh one.

**Claude** (`.tuk-claude`) — Anthropic's own shipped design tokens (cream `#F0ECE0`,
terracotta `#C96442`, coral `#D97757`, ink `#141413`), **plus a real screenshot viewed
14.9.2026** (`anthropic.com/news/projects`, the "Project knowledge" panel). That
screenshot added two facts the tokens alone missed: chat prompts/headings render in a
serif face (Georgia/Iowan-Old-Style stack here, real Claude uses a Copernicus-style
serif) — a distinctive part of the look the sans-only version was missing entirely —
and the actual interactive-element color (links, the "+" on an action row, file-type
chips) is a plain blue `#2C84DB`, not the terracotta; terracotta/coral are brand color,
not the color doing UI work. Every gray still carries the same warm/olive undertone,
never a neutral cool gray.

**Gemini** — requested 14.9.2026, not yet built. One real screenshot was located
(`commons.wikimedia.org/wiki/File:Google_Gemini_Screenshot_(2026).png`, third-party but
dated) confirming sidebar structure ("My Stuff," "Temporary Chats") and bottom input
placement, but no color/font/corner-radius detail was verified from it yet — next
session's work, not started.

## Status

Wired into `studio/lib/templates.ts` / the studio's `/templates` page. n8n and Claude
were corrected against real, viewed screenshots this round (sourced above); ChatGPT
still rests on episode 1's original build, unverified again this session; Gemini is
requested but not built. `video/reel-34.html` uses `.tuk-n8n` and inherits today's
corrected (dark) version automatically since it targets the class, not a hardcoded
color.

Sources: n8n.io/brandguidelines; `blog.n8n.io/how-to-build-ai-agent/` (2 real
screenshots fetched and viewed, colors sampled with PIL); this session's own review of
`video/reel-01-v25.html`; `anthropic.com/news/projects` (1 real screenshot fetched and
viewed); `commons.wikimedia.org` (1 third-party Gemini screenshot, structure only).
