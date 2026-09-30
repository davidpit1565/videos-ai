# Episode 53 — script, ready to produce

## Topic
Applicant Tracking Systems (ATS) — resume-screening software most employers now run before
a person ever opens an application. The widely-repeated "75% of resumes get auto-rejected by
the ATS before a human sees them" stat is **debunked**: it traces to a 2012 marketing claim
from a resume-services company (Preptel) that went out of business in 2013, with no study or
methodology ever behind it, and current 2025-26 research (interviews with recruiters at
Amazon/Google/Microsoft, a 2025 study of 25 recruiters across 10+ ATS platforms) finds the
opposite of the popular claim — most ATS platforms rank/sort applications rather than
auto-reject them, and 90%+ of applications do eventually get a human look.

The real, still-current, still-costing-people-jobs problem is different: ATS software
parses a resume into fields (name, dates, job titles, skills) so a person can search and sort
it later — and real, current formatting choices genuinely break that parsing. Tables and
multi-column layouts get read row-by-row and merge into unreadable "word salad." Headers,
footers and text boxes are frequently skipped entirely, sometimes dropping name and contact
info. Photos, icons, and skill-bar graphics are invisible to the parser outright. So a
"technically reviewed" application can still reach the recruiter as broken, incomplete data
— and recruiters spend on the order of 6-10 seconds on that first screen, nowhere near enough
time to notice information is actually missing and go looking for it.

The payoff: concrete, currently-recommended formatting fixes that measurably help a resume
parse correctly and actually reach a person intact — single column, standard section headers
(Experience/Education/Skills), the job posting's own keywords worked into the text, contact
info in the body (not a header/footer), and a plain .docx or a real text-layer PDF instead of
a designed template or an image-based export.

## Why this topic, why now
- **Locked topic, replacing the AI voice-cloning brief** — that topic was caught as a
  duplicate of already-shipped episode 38 ("Ten seconds of your voice is all AI needs to
  clone it now," `channel/episode-38-script.md`, merged, rendered, live) before any script
  was written. This is the corrected topic.
- **Genuinely universal, zero AI/technical literacy required**: anyone who has ever applied
  for a job understands "software reads your resume before a person does" instantly, with no
  setup.
- **Not yet covered**: checked against every existing episode script (1 through 52) and
  `studio/lib/articles.ts` — no prior episode covers resumes, job applications, or ATS.
- **A genuine myth-correction angle, not a repeat of the debunked stat**: this is the same
  discipline that caught episode 18's "ChatGPT agent mode" (a stale premise) and this
  session's own voice-cloning duplicate — verify before writing, and here specifically,
  verify the *popular* stat itself before using it, not just the topic's existence. Using
  the "75%" figure as fact would have been exactly the kind of fabricated-sounding stat this
  session already rejected twice on the previous (voice-cloning) topic.

## Verification (live web search, 30.9.2026)

**ATS adoption (real, sourced, current):**
- HR.com's 2025-26 survey: 78% of employers now use an ATS, up from 66% the year before.
- Fortune 500: 97.4% (487 of 500) use an ATS (Jobscan's 2026 Fortune 500 usage report).
- Resume Genius's 2026 Hiring Insights Report: 71% of organizations use ATS software (an
  independent, close-but-not-identical figure to HR.com's — both cited, not cherry-picked to
  the higher number).
- 93% of recruiters report using an ATS in 2026; 70% of in-house recruiters use theirs daily.

**The "75% auto-rejected" claim — checked and found unsupported:**
- Traces to a 2012 marketing claim by Preptel, a resume-services company that closed in
  2013 — no underlying study or methodology has ever been found.
- Current, contradicting research: a 2025 study of 25 US recruiters across 10+ ATS platforms
  found 92% do not configure auto-rejection rules based on resume content; recruiter Jan
  Tegze and researchers interviewing recruiters at Amazon, Google and Microsoft report that
  none of the major ATS platforms automatically reject or hide resumes from recruiters, and
  that 90-95%+ of applications are in fact reviewed by a human.
- **This script does not use the 75% figure or any auto-reject framing** — it states plainly
  that most resumes are reviewed, and the real problem is what a human recruiter is actually
  looking at once parsing has gone wrong.

**The real, current mechanism — resume parsing failures (sourced, current, 2026):**
- Tables/multi-column layouts: parsed row-by-row, merging content from separate columns into
  unreadable text ("word salad") — job titles, companies, and dates scrambled together
  (Jobscan, multiple independent 2026 sources).
- Headers/footers/text boxes: frequently skipped entirely by ATS parsers — a name, phone
  number or email placed in a styled header can vanish from the parsed record, leaving a
  nameless, contactless application on the recruiter's side.
- Images/graphics (photos, icons, skill-level bars): invisible to parsers outright; some
  parsers flag an image as an error requiring manual handling rather than reading around it.
- Recommended, currently-standard fix (Jobscan and multiple other 2026 ATS-formatting
  guides, cross-checked, not a single source): single-column reverse-chronological layout,
  standard section headings, a common font, contact details in the document body (not a
  header/footer), keywords drawn directly from the job posting's own language, saved as
  .docx or a true text-layer PDF (not a flattened image/export).

**Recruiter review time (real, sourced):**
- The Ladders' original eye-tracking study (2012): ~6 seconds average initial resume scan.
  Their 2018 follow-up: 7.4 seconds.
- Current 2025-26 surveys (Hiring Landscape, cited across multiple outlets): 42% of HR
  professionals spend under 10 seconds on the initial scan; 64.9% make their first keep-or-
  cut decision in under 15 seconds. Cited as a range (6-10 seconds), not a single invented
  precise number, since sources vary.

## Comprehension test — applied to the entire script (24.9.2026 standing rule)
- **Hook**: no jargon — "software," "resume," "a person" — a viewer who has never heard the
  term ATS understands the claim immediately.
- **Line 2**: names the term ("It's called an ATS") only after the plain-language concept has
  already landed in line 1 — same pattern as episode 49's "AI Overviews" reveal.
- **Line 3 (myth correction)**: "that number's fake" and "no real study behind it" — plain
  words, no research-methodology jargon.
- **Line 4 (mechanism)**: "tables," "columns," "scrambled" — concrete, visual, no parsing/
  technical-formatting jargon (no "parser," "field extraction," "OCR").
- **Line 5 (time constraint)**: "seven seconds," "nobody's stopping to notice" — plain.
- **Line 6 (fix)**: "one column," "plain headers," "the exact words from the job post," a
  ".docx or text PDF, never a picture of one" — every term explained by what it is, not
  assumed.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type: Direct Address** (declarative, second-person-adjacent, non-question — same shape
  as episode 2's all-time-high "What an AI agent actually is" and episode 46's "Your Copilot
  chats at work don't vanish...") — last used as a pure Direct Address episode 46, a
  7-episode gap; not a repeat of episode 52 (Shock/Surprise) or episode 51 (Contrarian Open)
  immediately prior.
- **The new 30.9.2026 "feel it in the gut" standing rule** (`CLAUDE.md`): the hook doesn't
  just state that ATS software exists — it opens on a specific, universally-recognized felt
  memory ("that job you never heard back from") before revealing the real mechanism behind
  it. Checked from an outsider's seat: nearly every viewer who has ever applied for a job has
  personally lived the exact moment the hook names.
- **Dry-sentence test**: read cold, creates real pull — ties a memory the viewer already has
  to a claim they didn't know ("software read it first, and it might not have worked").
- **Checkable-claim test**: "software read your resume first" is checkable and true for most
  employers (78%/97.4%/93% adoption figures above) — not a hypothetical "would you even
  know" framing.
- **Sendability test**: a specific, real person (anyone currently job hunting) would forward
  this — the hook line and the caption's complete fix are both standalone and actionable
  with zero extra clicks.
- **Comment-inviting element**: caption asks a direct, debatable, personally-answerable
  question (see caption file) — not just a follow CTA.
- **David's added standing bar for this episode — full-runtime tension, not just the hook**:
  the script does not relax into flat explanation once the hook lands. Line 3 (myth
  correction) keeps tension by overturning what the viewer thinks they already know; line 4
  escalates with a vivid, concrete image (your own name and job history turning into
  scrambled nonsense); line 5 adds real time pressure (seven seconds, no time to notice);
  line 6 is the payoff the whole build has been pointing toward, not a separate afterthought.
  Compared directly against episodes 1, 2, and 49 for pacing: all three keep the claim
  escalating line to line rather than settling into neutral explainer tone after the hook —
  this script is built the same way, each line raising the stake or specificity of the one
  before it, not restating the hook's claim in different words.

## Density check
6 distinct ideas across 6 non-CTA lines (slightly above this account's usual 4-5, justified
by the topic genuinely having a myth-correction beat the other reach-first episodes didn't
need): (1) the felt memory + real claim (software reads first), (2) the term + adoption
stat, (3) the popular stat is fake, (4) the real mechanism (parsing failure imagery),
(5) the time-constraint stat, (6) the concrete fix. Two CTA lines don't count as content.

## Simplicity/length check
Every line is plain consumer language, no unexplained jargon (checked line by line above).
Length target: 30-75s per the standing floor; 8 lines including 2 CTA lines, similar shape
and density to episodes 49/51/52 (all landed 40-55s at similar density) — final length
confirmed after voice generation and retiming.

## Where the comment-inviting element lives
Caption ends with a direct, debatable, personally-answerable question: "Have you ever sent
out a great resume and never heard anything back — not even a rejection? Comment PARSED if
you think it might have been the formatting, or GHOSTED if you think it was something else."
— plus a comment-to-DM funnel ("Comment FIX and I'll send you the exact formatting checklist")
for a lower-effort path to engage.

## Narration (final, 9 lines; lines 4 and 6 reworded during production — see Production notes)
1. "That job you never heard back from? Software read your resume first — and it might not have actually been able to read it."
2. "It's called an ATS — a program that scans applications ahead of any person. Most companies, about eight in ten, use one now." (reworded during production, see Production notes: "three out of four" tripped `build_voice.py`'s onset-burst check on "three" — same known failure mode as episode 38 — so this uses the same accurate 78% figure phrased without the word "three"; "nearly" was tried first and dropped too, for tripping the -LY ending rule)
3. "You've probably heard it auto-rejects most resumes. That number's fake — it traces back to a company that closed over a decade ago, with no real study behind it."
4. "The real problem: that program can't read tables, columns, or a fancy layout. Your name, your dates, your whole work history — can come out as scrambled nonsense on the other side." (reworded during production: "designed" and "turned" both recurred as genuinely swallowed/clipped words across multiple independent reroll seeds — a real, repeated defect, not seed noise — so reworded rather than kept fighting the model, same discipline as the "three" fix on line 2)
5. "And the person who opens it next spends about seven seconds deciding. Nobody's stopping to notice your information's actually gone missing."
6. "The fix: one column, plain section titles like Experience and Skills, the exact language from the job post — send it as a real dot-docx or a text PDF, not an image." (reworded: "saved" recurred as a swallowed word across independent takes of this line; "picture of one" also flagged once — restructured to drop both)
7. "Send this to anyone job hunting right now who has no idea their resume's invisible."
8. "The setup's in the link in bio."
9. "Follow for the setup that actually works."

Lines 8 and 9 use the exact locked canonical text (`audio/voice/profile/canonical-lines.json`)
so `build_voice.py` loads the pre-polished clip byte-for-byte instead of regenerating.

## Production notes
Filled in during production below — voice generation, any accent/swallowed-word fixes, gate
results, render/QA results, and the two personal viewings.

## Not yet done at time of writing
Script only as of this point — voice generation, render, gate, and publish happen next in
this same session, under real time pressure (David asleep, wants this live in ~5 hours).
Verified 30.9.2026 — re-check all figures above if this sits unproduced for more than a
few weeks.
