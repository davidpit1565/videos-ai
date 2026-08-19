---
name: explain-steps
description: >-
  Use whenever explaining how to do something in a user interface, a tool, or a
  service — Instagram settings, Gmail filters, Vercel, Beehiiv, ManyChat, n8n, a
  browser, a phone. Also use when writing narration or captions for a tutorial
  video, since the channel's whole promise is the exact screen and the exact click.
  Trigger words: "how do I", "where is", "I can't find it", "explain in detail",
  "tasbir", "lo hivanti", "eh osim", "step by step", "לא הבנתי", "תסביר",
  "איפה זה", "איך עושים". Also trigger when a previous explanation was answered
  with confusion — that is the signal the step was written from the writer's screen
  and not the reader's.
metadata:
  version: 1.0.0
  owner: local
---

# Explain steps

The reader cannot see what you see. Every explanation is written from their screen.

## The rules

1. **One numbered step per action.** A step is one click, one field, one toggle. If a
   sentence contains "and then", it is two steps.
2. **Name the thing exactly as it appears, in both languages.** The interface may be in
   English or in Hebrew, and you do not know which: `"See all settings"` (`"הצג את כל
   ההגדרות"`). Same for buttons, tabs and checkboxes.
3. **Say where on the screen it is** — top right, bottom of the panel, middle of the page,
   left sidebar. "Click Settings" is useless if there are three things called Settings.
4. **Never point at an icon you cannot describe.** "The sliders icon" failed a real reader.
   Either describe it unmistakably (the gear ⚙️, the three dots, the profile picture) or
   route around it entirely.
5. **Give the boring path, not the clever one.** Menus are findable; keyboard shortcuts and
   hidden affordances are not. If there are two ways, describe the one with more clicks.
6. **Mark what is optional, and say so first.** "This part is only for tidiness — the
   address works without it" removes the fear of doing it wrong.
7. **Say what should happen after each meaningful step.** "A panel opens on the right." If
   it did not open, the reader knows immediately, at that step, and not five steps later.
8. **One warning at the point it matters,** not a list at the end. "Tick *Never send to
   Spam* — otherwise the verification mail disappears."
9. **No jargon without the plain word beside it.** Not "configure DNS" but "add two lines
   at the company you bought the domain from (DNS records)".
10. **When they say they did not understand, do not repeat it louder.** Find the step that
    assumed something, and replace that step with a different route.

## What this is not

- Not a list of features. A step-by-step exists to complete one task.
- Not a place for "it depends". Pick the path you would pick, say why in half a sentence,
  and move on.
- Not longer for the sake of it. Ten real steps beat three steps and a paragraph.

## In video scripts

The same rules, minus the numbers. On screen: the actual interface at the moment the
narration names it, the cursor moving to the thing before it is clicked, and the label
readable at phone size. Narration says what is being clicked, never "as you can see".

A tutorial that skips the step where it breaks is the thing this channel exists not to be —
so the failure and the fix get the same screen time as the happy path.
