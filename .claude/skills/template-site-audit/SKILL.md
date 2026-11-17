---
name: template-site-audit
description: Find and fix the tells of a templated, AI-built website (generic "why us" blocks, empty buttons, invented testimonials and numbers, purple gradients, decorative emoji, template pricing, broken Hebrew, not built for phones). Audit first, change nothing without approval. Use when asked "does this site look AI-made", "make the site less generic", or before a site redesign or rebrand.
---

# Template site audit

Source: a public Hebrew prompt by instagram.com/danaellag ("a site that screams vibe coding"), sent by David on 13.11.2026 and adapted to English here. For deeper design work use the `impeccable` skill (existing sites) or `frontend-design` (new pages).

## Step 0: ask before starting
Ask three short questions and wait: what the site is built on (Lovable, Wix, Next.js, other), who the customers are, and whether most visitors come from a phone or a computer. Skip a question whose answer is already known from the repo.

## Step 1: audit only, no code changes
Go through every page, component and text. Return a table: pattern | where (page, component, line) | what it says or looks like now | what to remove, change or improve. For a pattern that is not on the site write "not found".

Patterns to look for:
1. Generic "why us" section: "Why choose us?", "Our advantages", three cards of "Professional", "Personal service", "24/7".
2. Buttons that say nothing: "Get Started", "Let's go", "Learn more", the same button in every section.
3. Testimonials that look invented: first name only, no photo, no company, five stars for everyone, a strip of "client" logos with no real link.
4. Numbers with no source: "10,000+ happy customers", "98% satisfaction", "4.9 stars", running counters.
5. Empty marketing headlines: "The smart way to...", "The future of...", "An innovative solution", one word in a different colour or gradient.
6. Template design: purple, pink or blue gradients, glow behind elements, glass effect, every card with the same shadow and radius, everything centred.
7. Icons and emoji as decoration: sparkles next to every AI feature, a rocket next to "launch", emoji in headings, an icon on every row.
8. Template pricing: Basic / Pro / Premium, "Most popular" on the middle one, bloated feature lists.
9. Selling without showing: a first screen with a generic illustration instead of the product, the work or the people.
10. Broken Hebrew (when the site has Hebrew): punctuation on the wrong side, a space before a comma, long dashes, reversed brackets, English words and numbers jumping in a sentence, literal translation, left-aligned text.
11. Not built for the phone: text cut or running off the side, buttons too small for a finger, a menu that does not open, stretched images, pricing tables that scroll sideways.

## Step 2: stop
Wait until the owner says which rows to fix.

## Step 3: fix only what was approved
Remove:
- Numbers, testimonials, logos and ratings with no real source. Put `[to fill in: what is missing]` in their place so the owner fills it in. Never invent a replacement.
- Icons and emoji that explain nothing.
- Sections that repeat the same idea in other words.

Change:
- Main headline: what the business does, for whom, and what comes out of it.
- Buttons: the action and what you get ("Book a 15-minute call", "Get a quote within a day"). One main button per screen.
- "Why us": specific proof instead of general traits: how the work goes, a real client story, or what you do not do.
- Colours: neutral background, one text colour, one accent from the brand. No gradients.
- Pricing: packages by the real kinds of customers, or think the packages through with the owner.

Improve:
- The product or the work on the first screen: a real screenshot, a short video, or a photo of the work or the people.
- FAQ with the questions customers really ask: what it costs, how long it takes, what happens after.
- Hebrew pages: `dir="rtl"` and `lang="he"` on the html tag, punctuation attached to the word before it, a normal hyphen, `bdi` for English words and numbers inside a sentence.
- Phone first: check every page at 375 px and 768 px. Readable without zoom, buttons easy to tap, no sideways scroll, images not stretched, a menu that opens and closes on touch.
- Test for every sentence: could another business in the field write exactly the same sentence? If yes, rewrite it with a detail only this business can say.

## Output
A short list: what was removed, what was changed, what was improved, what is left to fill in. A change that was not seen working is marked "not checked" and is never presented as done.

## Before going live
1. Does someone who does not know the business understand within seconds what it does and for whom?
2. Is every number, testimonial and logo real, with a source?
3. Does every screen have one clear button that says what happens on click?
4. Was all the text read on a phone, with the punctuation in place?
5. Was the site opened on a phone and a tablet, with nothing cut or stretched?
