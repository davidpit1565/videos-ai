---
name: viral-hook-lab
description: >-
  Use whenever writing, rewriting or judging the opening line (hook) of a short
  video — Reel, TikTok, Short — or deciding what to make next for reach. Gives an
  evidence-graded way to generate hook candidates, test them against hard gates,
  and log them so the next one is smarter. Trigger words: hook, opening line,
  first 3 seconds, scroll-stopper, viral, retention, "why didn't it work",
  "which opener", "הוק", "פתיח", "ויראלי", "השורה הראשונה". Also use before
  scripting any short video, since the hook decides what the video must deliver.
metadata:
  version: 1.0.0
  evidence-date: 2026-10-20
---

# Viral Hook Lab

A hook is a hypothesis about what makes a stranger keep watching. This skill
exists because the evidence is thinner than the internet suggests: **no source
in the 2026-10 research gives a proven formula, and most "hook statistics" online
are untraceable.** So the job is not to apply a recipe. It is to write
candidates that follow what is actually supported, check them against gates,
state the risk honestly, and measure the result.

Read `references/evidence.md` once if you have not (2 minutes). It lists what is
supported, what is contested, and the myths to refuse.

## What the evidence supports (and no more)

1. **Platforms reward behaviour after the video starts**: finishing, replaying,
   sending to someone (TikTok Newsroom; Instagram via Mosseri quotes in secondary
   sources: watch time, likes, sends per reach). Nobody publishes weights.
   → The hook must be a promise the rest of the video **keeps**. A hook that gets
   a view and loses the viewer at second 7 is a failure, not a hook.
2. **A concrete, specific question beats a vague tease.** Curiosity theory
   (Loewenstein 1994; Golman and Loewenstein 2018) says people feel the gap only
   when they have a specific question in mind. "You won't believe this" creates
   no gap; "Where was this photo taken?" does.
3. **Self-relevance helps, partially.** A cue that says "this is about you or
   someone you know" improves attention and memory, but only a minority of people
   notice self-relevant cues in a distracting stream. Do not rely on it alone.
4. **Surprise draws the eye** (Itti and Baldi), **negative or threatening framing
   raises arousal on average** (PNAS 2019) — but a sizable minority is unmoved.
   Pair them with a concrete question.
5. **Plain, easy-to-process wording** is judged more positively, and the curse of
   knowledge is real: the writer cannot hear what a stranger does not know.
   Explain any named product or term in the same breath.
6. **Many people watch without sound.** Make the first line readable on screen.
7. **Something to keep or send is what turns reach into saves and shares.** In
   our corpus of 43 successful ChatGPT TikToks the median save rate was 3.3% and
   share rate 0.85%; videos that teach a step get saves.

## Refuse these (contested or untraceable)

Zeigarnik "open loops make people remember" (did not replicate in a 2025
meta-analysis); the 8-second goldfish attention span; "65% leave in 3 seconds"
and any other exact first-seconds percentage; "47% of value in 3 seconds";
"sends are 3-5x likes"; "losses loom twice as large" as a video rule; any
"best length in seconds" without a named dataset. If you catch yourself citing
one, replace it with "unproven; test it".

## Inputs to collect (ask only for what is missing)

- Topic and the **payoff**: what the viewer will have or know at the end.
- What is **on screen** in the first second (the proof, a changing state, a real
  interface). A hook with no visual support is half a hook.
- Who it is for, in one phrase (age, situation), and the platform.
- The last 2-3 hooks used (do not repeat the same type twice in a row).
- Any proof limit: what you **cannot** claim (no result yet, one test only).

## Process

1. **Write the promise and the payoff in one sentence each.** If the payoff is
   weaker than the promise, fix the payoff or shrink the promise. Never write a
   hook the video cannot keep.
2. **Generate 8-10 candidates across different mechanisms**, not variations of one:
   - Specific question the viewer wants answered.
   - Personal stake / "this is about you" with a concrete object.
   - Demonstration: the result shown first, then the cause.
   - Experiment story: "I did X to Y" with the outcome withheld.
   - Contradiction of something the viewer believes (only if true and checkable).
   - Instruction with a visible payoff ("Do this once, then watch").
   Mark each with its mechanism. Do not invent statistics or fake urgency.
3. **Run the gates on every candidate** (fail any = discard or rewrite):
   - **Cold read**: understood fully on the first pass, at speaking speed, by a
     stranger who does not know the topic or the brand.
   - **Concrete**: names a specific object, person, number or action — not
     "this", "something", "a trick".
   - **Honest**: the video delivers what the hook promises, with limits stated.
     No invented results, no false scarcity.
   - **Stake or question**: the viewer can feel something lose-able, or a
     specific question they now want answered. A flat true statement fails.
   - **Mute test**: works as on-screen text with the sound off.
   - **First frame**: something already visible and changing, not a blank
     opener or a logo.
   - **Sendability**: can you name the one person who would forward it, and
     what they would say? If not, the payoff needs something to keep or send.
   - **Repeat check**: different mechanism from the last two episodes.
4. **Pick one primary and one alternate.** State the **risk** of the primary in
   one line (e.g. "needs the result to be striking; if the AI refuses, switch
   to alternate B").
5. **Write the measurement plan** before publishing: which numbers will judge
   this hook (views at 3 s or "viewed vs swiped away" if shown; share of
   viewers reaching 50%; sends per reach; saves) and the hour at which to read
   them (72 hours, not 4). A single video cannot confirm a pattern; a pattern
   needs two independent videos.
6. **Log**: hook text, mechanism, risk, the readings, and a one-line verdict
   (STRONG / PROMISING / WEAK / UNCLEAR with reasons). No numeric "virality score".

## Output format

```
PROMISE: …   PAYOFF: …   FIRST FRAME: …
CANDIDATES
 1 [mechanism] "text"  — gates: cold ✓ concrete ✓ honest ✓ stake ✓ mute ✓ frame ✓ send ✓
 2 …
PRIMARY: #  ALTERNATE: #
RISK: …
MEASURE: … at 72 h
EVIDENCE USED: (what from evidence.md it relies on, with grade)
```

## Judging an existing result

When a video under-performed, separate **reach** (did the hook stop them?) from
**retention** (did the payoff keep them?) from **action** (did anything make
them save or send?). Zero saves with healthy reach points at the payoff, not
the hook. A 7-second average watch with 40% completion on a 35-second video is
a retention problem. Do not blame the hook for a payoff problem. Say what the
data cannot separate (topic, music, posting time, chance).

## Ethics

Honest stakes only. No fabricated results, fake urgency, fake social proof, or a
hook the video breaks. Evidence on whether broken promises cost trust is mixed
(mostly news-headline studies), so treat trust as your asset anyway.
