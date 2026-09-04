# Hooks — researched, not guessed

David flagged it directly (2.9.2026, after episode 22's hook): the opening line has been the
same shape too often — a plain declarative claim, negated. This file exists so the next
script doesn't default to that shape again just because it's the one already in muscle
memory. Read this before writing any episode's first line.

**The rule this file exists to enforce: never the same hook type two episodes in a row.**
Pick deliberately from the categories below, based on what this specific episode's content
actually is — not whichever type got used last.

## The dry-sentence test — required before a hook ships

He said it plainly, twice now (2.9.2026): a hook is not just a true, on-topic first
sentence — a flat, informational statement is not a hook even when it technically matches
one of the categories below. The first version of episode 22's hook ("If it failed right
now, would you even know?" — before that, "Your automation says it worked. It didn't.")
demonstrated the failure mode directly: two lines that classified as *different* categories
in the table below, and still read as the same thing, because neither one actually pulled
on anything the viewer feels.

Before a hook ships, ask honestly: **does this create real pull — fear, identity, stakes,
curiosity that itches — or does it just state a fact in a short sentence?** A hook can be
calm and still land (not every hook needs to shout), but it has to make the viewer feel
seen, worried, or genuinely curious — not just informed. If the honest answer is "it's just
informative," it fails this test regardless of which category it technically fits, and it
does not ship. Reread the "why it works" column for the chosen category and check the draft
line actually does that thing, not just that it's shaped like the example.

## The real research (sourced, not invented)

Two independent, cited analyses, both current as of 2026:

- **OpusClip, TikTok, Q1 2026, 34,000+ clips analyzed** — [opus.pro/blog/tiktok-hooks-that-go-viral-2026](https://www.opus.pro/blog/tiktok-hooks-that-go-viral-2026)
- **OpusClip, Education & Tutorials genre specifically, 89,939 clips analyzed** —
  [opus.pro/research/best-video-hooks-education-and-tutorials](https://www.opus.pro/research/best-video-hooks-education-and-tutorials)

The education-genre numbers matter more for us than the general-TikTok numbers — this
channel is a tutorial channel, not lifestyle/comedy, and the two genres do not perform the
same hook types identically (education skews toward Direct Address/Question far more than
TikTok overall does).

### The categories, with real examples and real reasoning

| Type | What it looks like | Why it works (as stated by the source) | Education-genre share |
|---|---|---|---|
| **Direct Address / Question** | "Have you ever wondered why X actually works?" / "What if everything you know about X is wrong?" | Most effective type *for this specific genre* | 66% of education clips — the dominant type |
| **You-Focused Appeal** | "You've been doing X wrong — here's the right way" | Names the viewer's own mistake directly | 16% |
| **Contrarian Open** | "Everyone says X. It's wrong." / "Stop doing X. Here's what works instead." | "The brain can't leave a contradiction unresolved" — a stated cognitive bias, not a guess | strong on general TikTok too |
| **Shock / Surprise** | "I was today years old when I learned X." / "Nobody is going to tell you this about X." | 6% of education clips, but high per-clip average | 6% |
| **Problem / Solution Setup** | "Struggling with X? Try this instead." | Directly names the viewer's pain point | 5% |
| **Product / Outcome Showcase** | "This AI tool just edited a week of work in 3 minutes." / before-and-after in frame 1 | Highest average views of any type on general TikTok (~6,037 avg in the source's sample) — "zero setup, zero context required, the payoff is the opening frame" | rare in education specifically |
| **Expert / Authority** | "After 400 [things], here's what I've learned." | Authority signal → curiosity gap → payoff promise, in one line | rare (credibility-building, not curiosity-building) |
| **The Specific Number** | "I wrote 3,247 cold emails. Here are the 4 that worked." | Numbers are "involuntary attention-grabbers" — implies real measurement | cross-genre |
| **Story / Anecdote Teaser** | "So this happened when I tried X…" | Narrative pull, less common, works when the story itself is the proof | less common |
| **Imperative Command** | "Stop scrolling if you're trying to X." / "Listen — this changed how I think about X." | Breaks the passive scroll state by demanding an action | cross-genre |

**Honest caveat, stated plainly:** "top 3 categories account for 88% of education hooks" is
a *frequency* stat, not a performance ranking — it says what creators reach for most, not
what wins most. Don't read popularity as proof.

## Cross-checked against our own real numbers

`channel/content-memory.md`'s 30.8.2026 grid (real Instagram view counts, our own account) already
lines up with this research in a way worth naming — HYPOTHESIS-level, same caveat as
everywhere else in this repo (16 episodes is not enough to confirm anything, but the direction
agrees with independently-sourced research, which is worth more than either alone):

| Episode | Hook | Type (this taxonomy) | Views |
|---|---|---|---|
| 2 | "What an AI agent actually is" | Direct Address / definitional question | **940 — highest measured** |
| 7 | "Your n8n agent has no idea it's wrong" | Contrarian Open (names the tool directly) | **658 — 2nd highest** |
| 1 | "One paste, and ChatGPT stops giving you the obvious" | You-Focused / Product-Outcome | 662 |
| 8 | "A check said it passed. It lied." | Mistake Warning, but opened with "Last time:" (a callback the viewer hasn't seen) | **139 — lowest measured** |

The two strongest performers are the two types the sourced research also ranks highest for
this exact genre (Direct Address/Question, Contrarian). The weakest is confounded by the
"Last time:" callback problem already documented in `content-memory.md` — can't cleanly
credit the hook type alone for that one. Still: two independent signals pointing the same
direction is the strongest thing in this file.

## Picking a hook for a specific episode — by content shape

`content-memory.md`'s "Pattern shapes worth trying" already names the story shapes this
channel uses. Each pairs naturally with different hook types — pick from the shape's own
row, and rotate within it so two episodes of the same shape don't also share a hook type:

- **The Impossible Test / Break the AI** (claim → live attempt → result) → **Contrarian Open**
  ("Everyone says X. We tried it.") or **Product/Outcome Showcase** (open on the result
  itself, explain how you got there second).
- **AI vs. Reality** (a claim from online → real test → verdict) → **Direct Address/Question**
  ("Does X actually do what everyone says?") or **Shock/Surprise** if the real result
  genuinely surprised you.
- **Build It** (idea → build → obstacle → result) → **Story/Anecdote Teaser** or
  **Expert/Authority** if the build itself demonstrates real hours put in.
- **Human vs. AI** → **The Specific Number** (a real measured comparison) or **You-Focused
  Appeal** if the comparison lands on something the viewer does themselves.

## Hook-type log — so the next script doesn't repeat the last one

Update this after every episode ships. The one rule this file exists to enforce: **check the
last row before writing the next hook, and pick a different type.**

| Episode | Hook | Type |
|---|---|---|
| 18 | "ChatGPT can use a website now" | Product/Outcome Showcase |
| 19 | "Claude keeps your files now" | Product/Outcome Showcase |
| 20 | "ChatGPT was going to buy things for you — then they quietly killed it" | Shock/Surprise (a claim that turned out false) |
| 21 | "Can an AI browser actually run your errands?" | Direct Address/Question |
| 22 | "If it failed right now — would you even know?" | You-Focused Appeal, posed as a question |
| 23 | "22 episodes. One file keeps us safe." | Expert/Authority (the "After N things, here's what I learned" shape) |

**Rejected drafts for episode 22, both failed the dry-sentence test, kept here so the same
flat shape doesn't get proposed again as if it were new:**
- "Your automation says it worked. It didn't." — technically Contrarian Open/Mistake
  Warning, read in practice as a flat statement with no pull on the viewer.
- "If it failed right now, would you even know?" (first pass, third-person framing) — still
  informational in tone even after adding a question mark; the fix was making it land on
  "you" specifically, not just posing a question.

Episodes 19-20 both leaned on the same Product/Outcome shape back to back — not flagged as a
mistake at the time because this file didn't exist yet, but exactly the pattern this log is
meant to catch going forward. 21 and 22 already varied (Question, then Contrarian) — next
episode should reach for something *not* in {Product/Outcome, Direct Address/Question,
Contrarian Open} to actually rotate, e.g. Shock/Surprise, The Specific Number, or
Expert/Authority, whichever the content genuinely supports — never force a type the episode's
own content doesn't earn.
