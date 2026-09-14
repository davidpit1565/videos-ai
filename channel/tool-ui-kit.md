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

**ChatGPT** (`.tuk-chatgpt`) — light variant still reused from episode 1's own build
(`video/reel-01-v25.html`). **A dark variant added 14.9.2026** from two real
screenshots David sent directly (his own chatgpt.com, dark mode — the app's other
real default state, not a rare setting): near-black page background, a fully rounded
pill-shaped input/textbox (not a boxy rectangle), quick-action rows as rounded pills
with an icon, and message bubbles as dark-grey rounded rectangles rather than
full-width rows. Colors estimated by eye from the screenshots — no file existed on
disk to sample with PIL, unlike the n8n/Claude corrections above. Use `.tuk-chatgpt.dark`.

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

**Gemini** (`.tuk-gemini`) — **built 14.9.2026**, replacing the earlier "requested,
not built" state. Two real screenshots David sent directly (his own gemini.google.com:
the empty "Let's jump in" state, and a live chat with a generated-video reply) gave
real, current facts a third-party wikimedia screenshot couldn't: near-black background
(not Google's usual white Material look) with a subtle radial gradient, a rounded pill
input almost identical in shape to ChatGPT's, a 4-point rainbow "spark" glyph as the
logo, a solid blue "Upgrade" pill top-right, and message bubbles using the same
dark-grey rounded-rectangle language as ChatGPT's dark mode — not a distinct bubble
style of its own. Colors estimated by eye, same caveat as the ChatGPT dark variant.

**n8n** also gained two shapes this round from a third real screenshot (n8n.io's own
homepage, embedding a real workflow: a form trigger → AI Agent → "Is a manager?"
branch → two Slack nodes, with Anthropic/Postgres/Entra-ID/Jira hanging off the Agent
as small circular icons): a diamond-shaped true/false branch node (`.n8n-diamond`),
and a row of small circular sub-connection icons under a node (`.n8n-subrow` /
`.n8n-subicon`) for the model/memory/tool pattern every AI Agent node shows.

## Status

Wired into `studio/lib/templates.ts` / the studio's `/templates` page. All four kits
(n8n, ChatGPT, Claude, Gemini) now rest on at least one real, directly-viewed
screenshot. `video/reel-34.html` uses `.tuk-n8n` and inherits today's corrected (dark)
version automatically since it targets the class, not a hardcoded color.

Sources: n8n.io/brandguidelines; `blog.n8n.io/how-to-build-ai-agent/` (2 real
screenshots fetched and viewed, colors sampled with PIL); n8n.io's own homepage (1 real
screenshot, provided directly by David); this session's own review of
`video/reel-01-v25.html`; `anthropic.com/news/projects` (1 real screenshot fetched and
viewed); chatgpt.com and gemini.google.com (4 real screenshots total, provided directly
by David — colors estimated by eye, not pixel-sampled, since pasted images aren't saved
to a path this session can run PIL against).
