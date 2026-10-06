# Episode 59 — LinkedIn trains its AI on your profile, and the switch is on by default

Built 6.10.2026, topic and hook approved by David the same day. Final line points at
episode 60 (Meta AI chats and Instagram ads) and uses the revised flowing format (no
"Tomorrow:" label — see CLAUDE.md, 6.10.2026).

## Topic choice (from the data, not picked fresh)

- Best recent episodes by David's own Instagram grid (6.10.2026): Alexa 447, ChatGPT
  hidden profile 414, resume-screening software 385, mom-video scam 321. All four are
  "something is already happening to your data / to you". LinkedIn is the closest
  everyday product to the resume episode (385) and has a real, short fix, which is what
  produces saves (`content-memory.md`, confirmed 21.9.2026).
- Not a repeat of a recent angle: no earlier episode covers LinkedIn.
- Rejected after a live check: Gmail + Gemini (real, on by default in the US, but no single
  off switch, turning it off also removes inbox sorting, and four recent episodes were
  already Google); iPhone notification summaries (too close to episode 44).

## Product verified live (6.10.2026)

- LinkedIn's own help page: setting "Data for Generative AI Improvement"; data used includes
  profile information, posts/articles/comments/poll responses, resumes and job-related
  answers, group activity, feedback on AI features; excluded: private messages, login
  credentials, payment information, salary data; opting out applies "going forward" and
  "does not affect training that has already taken place".
- Default on: Malwarebytes and Windows Latest (September 2025) — on by default, regions
  widened from 3.11.2025 (EU/EEA/Switzerland/Canada/Hong Kong, UK reported).
- **UNCONFIRMED / said carefully, not smoothed over:** exactly which countries have it on
  by default (sources disagree on the UK; LinkedIn's help page treats EU/UK differently).
  The video never claims a country list; the guide tells the viewer to check their own
  toggle. David is in Belgium (EU) — the toggle still exists there per the sources.
- **Correction of something I said in chat earlier:** I wrote that it was on in the US
  "since 2024" from memory before checking. Later searches found 2024 reporting that LinkedIn
  made US data eligible by default (September 2024), but I did not rely on it for the video.
- Not tested on a live account — stated in the article's Limits and the YouTube text.

## Hook rules check

- Hook: "Your LinkedIn profile is already teaching an AI — and nobody asked you." (12 words)
- Type: Shock/Surprise (last used solo: episode 57; episode 58 was Direct Address, so not
  a back-to-back repeat).
- Understandable from second one: LinkedIn is named with "profile" next to it, "teaching an
  AI" is plain words; nothing is assumed.
- Feel-it-in-3-seconds: it is the viewer's own profile and the viewer's own job search.
- Sendability: one specific person — a friend who is job hunting — the bridge line says so.

## Spoken script (plain language, ~60s)

1. Your LinkedIn profile is already teaching an AI — and nobody asked you.
2. There's a setting on LinkedIn that lets it train its AI on your profile and your posts. It's switched on by default.
3. Your job titles, your skills, what you wrote about yourself, your comments — all of it can be used. Your login and your bank info stay out of it.
4. Turning it off takes under a minute. Open LinkedIn, tap your photo, then Settings, then Data privacy.
5. Tap the one that says Generative AI, and flip the switch off.
6. One honest catch. Turning it off only works from now on. What it already learned, it keeps.
7. Send this to a friend who's looking for a job.
8. The setup's in the link in bio. (locked)
9. Tomorrow, I'll show you what Instagram does with the questions you ask its AI. Follow, so you don't miss it.

`script_lint.py` clean (0 risky words) after rewording "payment info", "Improvement", "turn".
Lines 5's spoken label is shortened on purpose: the exact label "Data for Generative AI
Improvement" is on the site page; "Improvement" ends in a soft -ENT this voice swallows.

## Binding promise

Line 9 promises episode 60 tomorrow: Meta using conversations with Meta AI to choose ads
(since 16.12.2025, no opt-out, EU/UK/South Korea excluded). If 60 changes or does not go out
the next day, re-render line 9 before 59 goes out.

## Photos (Unsplash License, free, no attribution) — all faceless, so no face-detection step applies

- `ep59-scene-a-typing.jpg` — woman's hands on a laptop with a latte, wood desk (Vardan Papikyan, unsplash 1qn0GnP9kk8).
- `ep59-scene-b-darkroom.jpg` — hand on a laptop keyboard, desk lamp, dark room (Bryan Plata, oXEdiNVw7KI). Mostly dark: watch for the frozen-picture check.
- `ep59-scene-c-phonelaptop.jpg` — hands holding a phone above a laptop, moody (Michal Biernat, h0xEUQXzU38).
- `ep59-scene-d-laptopdesk.jpg` — home office, shelves, window light (Thanos Pal, NXjBX_DaZuo).
- Dropped: a white-desk shot whose laptop screen shows a real Mailchimp page (wrong brand on screen), and two Unsplash+ (paid) shots.
- Real LinkedIn icon: `ep59-linkedin-logo.svg`, Wikimedia Commons (LinkedIn_icon.svg), icon only, no caption underneath. Scene 2.
- The two closing scenes share one photo (b), as the rule requires; the photo was also used in scene 4, not adjacent.
- Open point for David: only four free photos fit, so the closing photo repeats scene 4's. A fifth photo is a swap, not a rebuild.

## Design

Accent amber `#F59E0B` (not within 7 days of any dated entry: 54 `#06B6D4`, 55 `#EA580C`, 56 `#2563EB`, 57 `#059669`, 58 `#0D9488`). Music mood `urgent` (58 was `confident`).
