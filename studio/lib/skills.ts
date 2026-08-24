/** The Claude Code skills this project actually built and uses — the standing rule from
 *  CLAUDE.md is that every skill, agent, or tool built here is itself content, with an
 *  angle already written. Inlined for the same reason PROMPTS is inlined: this deploys
 *  from `studio/` alone, and `.claude/skills/` lives outside that root, so reading it off
 *  disk at request time would break in production even though it works locally. */
export type Skill = {
  slug: string;
  title: string;
  /** one line, what it does for the reader */
  blurb: string;
  /** which episode explains it, when one exists yet */
  episode: number | null;
  /** the exact SKILL.md content — what gets copied or downloaded */
  body: string;
};

export const SKILLS: Skill[] = [
  {
    slug: "explain-steps",
    title: "explain-steps",
    blurb:
      "The rule this whole channel is built on: one numbered step per click, the interface's own words in both languages, and the step that breaks gets the same screen time as the one that works.",
    episode: null,
    body: `---
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
   English or in Hebrew, and you do not know which: \`"See all settings"\` (\`"הצג את כל
   ההגדרות"\`). Same for buttons, tabs and checkboxes.
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
so the failure and the fix get the same screen time as the happy path.`,
  },
  {
    slug: "voice-doctor",
    title: "voice-doctor",
    blurb:
      "Judges a cloned narration before it ships — measures the ending energy, the sibilance, the gaps between lines — instead of asking a person to describe what sounds wrong.",
    episode: null,
    body: `---
name: voice-doctor
description: Judge and repair David's cloned narration before it reaches him. Use whenever narration is generated, an episode is rendered, a voice profile is built or changed, or he says the voice sounds wrong — "swallowed", "cut", "no space", "sounds Indian/English", a named letter (R, T, D, S), or a specific word that never comes out right. Also use before delivering any audio or video with his voice in it.
---

# Voice doctor

He should not have to describe what he heard. Measure it, name it, fix it, and
show him the numbers.

## The rule

**Never deliver narration or a rendered video without running the doctor on it
first.** One command:

\`\`\`bash
python3 audio/voice_doctor.py audio/voice/<ep>.wav          # cheap, per line
python3 audio/voice_doctor.py audio/voice/<ep>.wav --deep   # per word, needs whisper
\`\`\`

Exit status is 1 when something is scored \`BAD\`. A \`BAD\` finding is not a note —
it is a defect he will hear, and it gets fixed before the file is sent.

## What each measurement means, and what it earned its place from

| Metric | What it catches | Where it came from |
|---|---|---|
| \`gap\` | Two lines talking over each other, or no room to breathe | He said "words are cut, not enough space between sentences". The measurement found 7 overlapping lines in episode 02, up to −0.60s |
| \`rate\` | Syllables per second; above ~6.5 the model elides endings | \`build_voice.py\` already re-rolls a line over this rate |
| \`end\` | High-frequency energy in the last 120 ms of real sound — the R, T, D he hears swallowed | "harder never comes out right". Whisper transcribed it perfectly, so intelligibility was never the defect |
| \`sib\` | 4–9 kHz against the 300–3400 Hz body — a dull or hissing S | He asked for the S to be fixed |
| \`lvl\` | A line quieter than the rest | Found two in episode 02 |

## Thresholds — what is real and what is not

- **An overlap is absolute.** A negative gap is two voices at once. No judgement
  needed.
- **\`MIN_GAP = 0.30s\`** and **\`MAX_RATE = 6.5\`** are the only other fixed numbers.
- **Everything else is judged against this narration's own median**, with a robust
  (MAD-based) fence. A line is flagged for being unlike the rest of *his own*
  delivery, not for missing a number invented in advance.
- **Known limit, say it out loud when reporting:** the per-line \`end\` spread is
  wide because lines end on different sounds — a line ending in a vowel measures
  lower than one ending in a T, and that is not a fault. When an ending is the
  question, run \`--deep\` and compare words with words. Do not present the per-line
  \`end\` column as a verdict on a single line.
- An earlier version of this work used a fixed −18 dB ending threshold. It was
  uncalibrated — the real median across 30 words was −22.6. Never re-introduce a
  fixed floor without the measurement that justifies it.

## The repair ladder — cheapest fix first

1. **Overlap or run-on** → the cause is fitting speech into fixed video slots.
   Build the narration naturally and move the picture to it:
   \`\`\`bash
   python3 audio/build_voice.py --cues video/<build>.html --out audio/voice/<ep>.wav
   python3 export/retime.py video/<build>.html audio/voice/<ep>-cues.json --out video/<build>-paced.html
   \`\`\`
   Never reach for \`--fit\` to solve pacing; \`--fit\` is what caused it.
2. **A word arrives soft** → change the word, do not fight the model.
   \`python3 audio/script_lint.py\` names the class (unstressed -ER, -LE/-BLE, -LY,
   R+cluster, flapped T, final -TH, -ENT) and offers a replacement. This is what
   worked: \`harder\` → \`think hard\`, \`reversible\` → \`something you can undo\`.
3. **The word cannot change** (the brand line "setups that actually work") →
   \`audio/line_doctor.py\` generates candidates across seeds and respellings, ranks
   them by ending energy, and stores his pick in
   \`audio/voice/profile/line-choices.json\` so future renders reproduce the approved
   take instead of re-rolling the dice.
4. **A whole sound is wrong across the board** (accent, not one word) →
   \`audio/phoneme_audit.py\` over 30 carrier sentences, and if it is really the
   reference and not the text, rebuild the profile from a better excerpt with
   \`audio/build_reference.py\`.

## Two things measurement cannot decide

- **Accent.** There is no score for "sounds Indian" or "sounds English". When he
  judges accent, his ear wins and the number loses — that already happened once:
  the similarity metric preferred a 28.8s reference, he picked the 18.4s one, and
  the stored profile is his. Record the disagreement in
  \`audio/voice/profile/profile.json\` rather than overruling it.
- **Which take he connects with.** Generate options, announce them, let him pick,
  then lock the pick.

## Reporting to him

Give the numbers, in Hebrew, in a small table, with what changed and what is still
open. Never say "improved" without the before and after figure beside it. If a
defect he named is not reproducible by measurement, say that plainly and ask for
the second and the word — do not quietly re-render and hope.`,
  },
];

export function skillBySlug(slug: string): Skill | null {
  return SKILLS.find((s) => s.slug === slug) ?? null;
}
