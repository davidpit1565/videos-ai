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

**n8n** (`.tuk-n8n`) — brand colors from n8n's own brand guidelines
(n8n.io/brandguidelines): Mandy pink/red `#EA4B71`, Brand Black `#101330`, near-white
grey `#FCFCFD`. Canvas: n8n's own docs ("Navigating the editor UI") describe a grey
dotted-grid canvas with white node cards on it — not a dark canvas. A node with a
problem gets a small circular badge, which is what `.n8n-badge` recreates.

**ChatGPT** (`.tuk-chatgpt`) — reused from episode 1's own build
(`video/reel-01-v25.html`), which recreated the real Settings menu and Custom
Instructions panel before this kit existed; that build was itself checked against the
live app before shipping. Light UI, real menu row labels and chevrons, `#10A37F`
accent.

**Claude** (`.tuk-claude`) — Anthropic's own shipped design tokens: cream background
`#F0ECE0`, terracotta accent `#C96442`, coral `#D97757`, near-black ink `#141413`. The
signature detail worth keeping if this kit is ever extended: every gray in Claude's
real UI carries a warm/olive undertone, never a neutral cool gray.

## Status

Not yet wired into `channel/motion-recipes.md` or `studio/lib/templates.ts` — that's
next, once David has looked at a real render using this kit and signed off on it.
n8n is first because it's this channel's most-covered tool (episodes 2, 7, 25, 29, 32,
33). ChatGPT and Claude are built ahead of when we'll need them next, per his request,
so the next episode on either doesn't wait on this being built from scratch again.

Sources: n8n.io/brandguidelines; docs.n8n.io ("Navigating the editor UI"); this
session's own review of `video/reel-01-v25.html`; Anthropic's shipped Claude.ai design
tokens (cream/terracotta/coral/ink hex values), cross-checked across multiple
independent design-reference sites in the same session.
