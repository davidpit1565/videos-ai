# Which instruction block should I paste?

| File | Use it if |
|---|---|
| `custom-instruction-EN.txt` | **Default.** Your original, unchanged. This is the one shown on screen in the video. |
| `custom-instruction-EN-optional-v2.txt` | You've used the original for a while and hit one of the four annoyances below. |

## What v2 adds, and why

Each addition targets a specific failure mode people run into after a week of daily use.
None of them change the system's philosophy — they're all guardrails.

**1. `Calibrate effort to stakes…`**
Reinforces the existing "do not overthink simple requests" line. In practice one sentence
about it isn't always enough: a 40-item capability menu creates a pull toward using it, and
casual questions can come back over-analysed. This makes the light path explicit rather than
merely permitted.

**2. `If key information is missing, state your assumption and answer anyway…`**
The most common complaint with reasoning-style instructions is that the model starts every
conversation by asking three clarifying questions. That's technically thorough and practically
exhausting. This makes "assume out loud and proceed" the default, and caps clarifying
questions at one.

**3. `Say plainly when you do not know or cannot verify something.`**
The original says *never invent facts* and *distinguish facts from assumptions*. This adds the
missing third behaviour: actively saying "I don't know." Prohibiting invention doesn't by
itself produce an admission of ignorance.

**4. `Default to prose… use bullets only when the content is genuinely a list.`**
Instructions that list many analytical methods tend to produce answers formatted as many
headed sections, even for a two-paragraph thought. This pushes back toward readable prose.

## What I deliberately did *not* change

- **The capability list.** It's long, and that's the point — it's a menu, not a checklist. Trimming it would narrow what the model reaches for.
- **`Do not reveal hidden chain-of-thought.`** Keep this. It's what makes answers read as finished thinking rather than a transcript of the model working.
- **The 9-step decision recipe.** It's well-ordered: `challenge` sits right after `assumptions`, which is exactly where challenging is useful.
- **The final line.** `The goal is the best possible answer, not showing the methods` is doing a lot of quiet work and should stay last, where it acts as a summary.

## One practical addition worth making yourself

Add two or three lines of personal context — role, language, what you're currently working on,
how you like answers. It reliably improves output more than any wording change to the
instruction itself, because it turns generic advice into advice about your actual situation.

Example:

```
About me: I run a small software business, solo, and I ship side projects.
I read English and Hebrew. Assume limited budget and no team unless I say otherwise.
```

## One line I generalised

Your original ended with:

> Respond in my language. Understand Hebrew written in Latin characters and reply naturally in Hebrew.

The shipped files say:

> Respond in my language. If I write my language using Latin characters, understand it and reply naturally in that language.

Same behaviour for you, but it works for every viewer of an English-language video rather than
reading as a personal note that got left in. If you'd rather your own copy name Hebrew
explicitly — which is slightly more reliable for Hebrew specifically — put the original line
back in your own Custom instructions. It's a one-line swap and nothing else depends on it.
