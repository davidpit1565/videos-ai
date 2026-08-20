# Episode 03 — "The Explainer"

**Why this episode exists:** it came out of a real failure. I told him to click "the sliders
icon" in Gmail. He could not find it, said so, and I repeated the same route in more words.
The fix was a rule set, and the rule set is the product.

**Format:** reel 52s (9:16) + long video 8–12 min · English · Flemish version for LinkedIn
**Ships:** the Explainer prompt → `/p/explainer`

---

## The reel — narration cues

| In | Out | Line | On screen |
|---|---|---|---|
| 0.30 | 3.20 | Ask AI how to change one setting. | phone, a settings screen |
| 3.46 | 7.10 | You get a paragraph that assumes you can already see it. | a wall of text, greyed |
| 7.60 | 10.60 | "Click the sliders icon." Which icon? | one line, `sliders icon` boxed in ember |
| 10.90 | 14.20 | It is explaining from its screen. Not from yours. | split: its screen / your screen |
| 14.50 | 18.00 | One paste fixes it. | the prompt block, brass rule |
| 18.30 | 22.40 | Now every answer is one click per step. | numbered steps appearing, 1 · 2 · 3 |
| 22.70 | 26.20 | The button named the way it appears — in both languages. | `See all settings` / `הצג את כל ההגדרות` |
| 26.50 | 30.00 | Where it is on the screen. Top right, not "somewhere". | arrow to the top-right corner |
| 30.30 | 34.00 | And what you should see after each step. | a checkmark per step |
| 34.30 | 38.20 | The honest part: it still cannot see your screen. | ember card |
| 38.50 | 42.60 | So when a label does not match, you say so — and it finds another route. | two paths diverging |
| 42.90 | 46.40 | It never repeats the same route louder. | the old paragraph, crossed out |
| 46.70 | 49.60 | Comment "explainer" and it is in your DMs. | CTA |
| 49.90 | 52.00 | Setups that actually work. | brand card |

**Flashes:** `the fix` 7.4 · `the rules` 14.2 · `honest` 34.0 (ember) · `take it` 46.4

**Hook alternatives to test:** (1) as above — names the moment of being stuck; (2) "AI explains
like someone who already knows where the button is."; (3) "I got told to click an icon that
does not exist. Here is the fix." Test 1 against 3.

## The long video — what happens on screen

1. **The failure, unedited.** The real exchange: my instruction, his "I did not understand",
   my useless repeat. Thirty seconds, no defence.
2. **Why it happens.** A model answers from a description of an interface, not from your
   screen. It has no idea whether your Gmail is in Hebrew.
3. **Build the prompt live, one rule at a time.** After each rule, ask the same question again
   and show the answer changing. This is the whole video: eleven rules, eleven visible
   improvements.
4. **Where it still breaks** — three real cases:
   - an app one version behind, labels do not match → what to say to it
   - a task with no menu path at all (gestures) → it will invent one; catch it
   - it stops naming positions after a long chat → paste the rules again
5. **Install it permanently** — Custom instructions, both screens, the exact toggle.
6. **The n8n version** for the ones who want it in a workflow rather than a chat.

## Caption to post

```
I told someone to "click the sliders icon."
He couldn't find it. So I explained again,
in more words. Same route. Still useless.

That's how AI explains by default: from its
own screen, not from yours.

Eleven rules fix it. One paste:

• one numbered step per action
• the button named exactly as it appears —
  in English AND in your language
• where it is on screen, not just its name
• never point at an icon it can't describe
• the boring menu path, not the shortcut
• what you should see after each step
• and when you say you're lost, a different
  route — not the same one louder

Honest part: it still can't see your screen.
When a label doesn't match, tell it — that's
the step where it earns its keep.

Comment "explainer" and I'll DM you the whole
thing.
```

**Hashtags:** `#chatgpt #aitips #promptengineering #aitools #productivity #howto #claude #tech`

## What to check after it's live

Saves-per-view against episode 01. This one is a utility people keep — if the save rate is not
higher than 01, the format is wrong, not the topic.
