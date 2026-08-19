# Episode 02 — "What an AI agent actually is"

**Format:** 9:16 · 1080×1920 · 52 seconds · English
**Build:** `video/reel-02.html` · **Style:** house style "Brass on Ink"
**Voice:** the stored profile — `python3 audio/build_voice.py --fit video/reel-02.html --out audio/voice/ep02-cloned.wav`
**Captions:** burned in, middle third, always on (assume muted playback)

**Why this episode is second:** measured demand puts "ai agents explained" at a median of
124,549 views against 11,880 for the custom-instructions topic episode 01 sits on
(`channel/demand-report.md`). It is also the gateway — episodes 03 onward assume the viewer
knows what a loop is.

---

## Narration + timing

The cues in the build are the script. Each node of the loop lights while the narration is on
that word, so the animation cannot drift away from the sentence.

| In | Out | Line | On screen |
|---|---|---|---|
| 0.30 | 3.20 | Everyone says *agent*. | `Everyone says **agent**.` |
| 3.46 | 7.16 | Almost nobody can tell you where the chatbot ends. | `…where the chatbot ends.` |
| 7.60 | 10.30 | A chatbot *answers*. That's the whole job. | `A chatbot answers. An agent acts.` |
| 10.60 | 13.70 | An agent *acts* — it plans the steps itself. | Split: Answers / Acts, agent side brass |
| 13.96 | 17.36 | Then it uses real tools, checks the result, and goes again. | Split holds |
| 17.70 | 20.80 | Same three steps, on a loop. *Plan*. | Loop ring, node 1 lights |
| 21.06 | 23.50 | *Act* — with a tool that touches something real. | Node 2 lights; chips light in sequence |
| 23.76 | 26.30 | *Check* what came back. | Node 3 lights |
| 26.56 | 29.16 | That loop is the entire difference. | One fast cycle through all three |
| 29.50 | 33.00 | One test settles it. | `One test settles it.` |
| 33.20 | 37.36 | If it can't act *without you*, it's a chatbot with a better name. | `Can't act without you? It's a chatbot.` |
| 37.70 | 40.90 | The honest part: agents don't fail like chatbots. | `They fail confidently.` |
| 41.10 | 43.60 | They fail *confidently*, halfway through. | Three ember failure cards |
| 43.80 | 45.96 | So your first one gets something *reversible*. | Lede |
| 46.30 | 49.10 | Next: your first *n8n agent*, end to end. | `Next: your first n8n agent.` |
| 49.36 | 51.60 | Follow so it lands in front of you. | CTA |

## Section flashes

`the line` 7.10 · `the loop` 17.34 · `the test` 29.18 · `honest` 37.40 (ember) · `next` 46.00 —
0.32s each. They exist to break scroll inertia at the exact second a viewer would otherwise leave.

## Editing notes

- **The loop is the whole episode.** If one thing has to be legible at arm's length on a phone,
  it is the ring with three nodes. Everything else can be re-explained in the caption.
- **Don't let the chips light before "act."** The point of the animation is that tools belong to
  one step, not to the whole loop.
- **The failure cards are ember, never brass.** Brass is the thing that works; ember is the
  warning. Mixing them breaks the only colour rule the channel has.
- **Hard cut at 52.0s.** No outro card.

## Hook alternatives to A/B test

1. *"Everyone says agent. Almost nobody can say where the chatbot ends."* (current — names the
   viewer's private confusion without insulting them)
2. *"An AI agent is three steps. That's it."* (promises brevity; pulls people who bounced off
   longer explainers)
3. *"If it can't act without you, it's not an agent."* (leads with the test — starts arguments in
   the comments, which is its own reach)

Test 1 against 3. They pull different audiences, and the saves-per-view in the studio will say
which one earned the content rather than just the click.

## Caption to post

```
"AI agent" is used for everything now,
which is why nobody can define it.

A chatbot answers. That's the whole job.

An agent runs a loop:
1. plans the steps itself
2. acts — with a tool that touches
   something real (inbox, calendar, browser)
3. checks what came back, then goes again

The test that settles it: if it can't take an
action without you, it's a chatbot with a
better name.

The honest part nobody posts: agents fail
confidently. They email the wrong person
politely, stop halfway and report success, or
run the same paid action twice. That's why the
first agent you build should touch something
reversible.

Next episode: your first n8n agent, end to end,
no code.

Setups that actually work — including what
breaks → link in bio.
```

**Hashtags** (eight, all actually about the content):
`#aiagents #n8n #aiautomation #chatgpt #aitools #automation #nocode #productivity`

## What to check after it's live

Open the studio → Episodes → *משיכת מספרים מאינסטגרם*, link the post to episode 02, and read
**saves-per-view**. Against episode 01 it answers one question: does the agent topic earn the
audience, or did it just earn the scroll?
