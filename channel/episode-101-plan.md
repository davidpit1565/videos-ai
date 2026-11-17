# Episode 102 plan: free GitHub alternatives to paid apps (Q1, reference DfSvS-CTqDA)

Publish mode: ASK DAVID (TRIAL or REGULAR; default REGULAR if he does not say).
Status: PLAN ONLY. Nothing built, voiced, published or merged. Written 16.11.2026.
Funnel stage: TOP. Format: numbered series candidate, "Free twins #1".

## 0. What we copy and what we do not (answer to David's "copy whole slides / the text")
- We copy the STRUCTURE and the beat order: paid logos first, they break, free ones appear, one card per item (paid pill, repo name, stars, licence), a progress counter, a saveable list at the end.
- We do NOT copy the creator's script lines, his card artwork, his hazard tape, his exact layout or his colours. Reason: copyright and Instagram's re-posting / originality rules (an "unoriginal" reel gets limited reach), and his reel shares the light-and-orange "AI look" Roni told us to leave.
- The FACTS are public and we may state them, but only the ones we verified ourselves (section 2). Several of his facts are wrong today or need a caveat.

## 1. The reference, as seen (15.11.2026 download, re-read 16.11.2026 from scratchpad `refs10/DfSvS-CTqDA/`)
@auraguy.ai, 3.11.2026, 68 s, 1,414 likes, 609 comments, views not exposed. Frames re-read 16.11 (contact sheets of the real video). Caption = the spoken list:
1. Open Generative AI (Anil-matcha/Open-Generative-AI, shown 32.2K, MIT) for Higgsfield
2. VoiceStudio (debpalash/VoiceStudio, 99.9K, AGPL-3.0) for ElevenLabs
3. OpenSEO (every-app/open-seo, screenshot) for SEMrush
4. AppFlowy (AppFlowy-IO/AppFlowy, 78.1K, AGPL-3.0) for Notion
5. OpenWhispr (OpenWhispr/openwhispr, 10.6K, MIT) for Wispr Flow
6. OpenProject (opf/openproject, 17K, GPL-3.0) for Asana
7. Cal.diy (calcom/cal.diy) for Calendly
8. Chatwoot (chatwoot/chatwoot, 38.8K, "MIT CORE") for Intercom
9. Cap (CapSoftware/Cap) for Loom
CTA: comment "REPO" for a DM (we cannot DM at scale; ours is the link in bio).

## 2. Verification, 16.11.2026
HOW (honest about the method): `gh api repos/...` was refused by this session's GitHub scope (403) and api.github.com was blocked through the proxy, so stars, licence and creation date were read from the GitHub repo pages through Exa's page fetch on 16.11.2026. Exa may serve a recent snapshot, not this minute: RE-READ every star count on the GitHub page itself on build day, and round down on screen ("35K+"). Last push date was NOT obtained for any repo (not in the fetched data): unconfirmed. Prices read from the official pricing pages on 16.11.2026 (same fetch method).

| # | Repo (stars, licence, created) | What it really is | Paid tool, cheapest paid plan (official page, 16.11.2026) | Verdict |
|---|---|---|---|---|
| 1 | Anil-matcha/Open-Generative-AI: 34,952, MIT, 2023 | A front end for image/video models "powered by MuAPI" (a paid API); README sells "uncensored", "no content filters", "Spicy" | Higgsfield: price page did not load (higgsfield.ai/pricing): UNCONFIRMED | DROP (needs a paid API to generate anything, so not "free"; "uncensored/spicy" branding is a brand-safety risk; name resembles Higgsfield) |
| 2 | debpalash/VoiceStudio: 111,689, AGPL-3.0, created 9.4.2026 | Local voice cloning, voice design, dubbing, dictation, text to speech; also sells "VoiceStudio Pro" and "Cloud" | ElevenLabs Starter $6/mo (Creator $22, first month $11), elevenlabs.io/pricing | FEATURE WITH CAVEAT: 111K stars in 7 months is unusual (check star history before building); runs on your own computer (needs a decent one); voice cloning: say "your own voice" only |
| 3 | every-app/open-seo: 27,822, MIT, created 27.2.2026 | SEO tool; you bring a paid DataForSEO key and pay per use, or $10/mo hosted | Semrush: prices page loaded without the dollar figures: UNCONFIRMED | DROP for this reel (not free; young; niche audience) |
| 4 | AppFlowy-IO/AppFlowy: 78,984, AGPL-3.0, 2021 | Notes, docs, wikis, tasks with AI; desktop and phone apps; calls itself "the open source Notion alternative" | Notion Plus $10 per member/mo, notion.com/pricing (Notion also has a free plan) | SAFE TO FEATURE (say "alternative", not "replaces everything") |
| 5 | OpenWhispr/openwhispr: 11,623, MIT, 2025 | Press a key, talk, text appears; local models or your own cloud key | Wispr Flow: page lists Free $0 and paid per-user plans; the calculator says "Flow Pro monthly cost: $12" (wisprflow.ai/pricing). Wispr Flow itself has a FREE plan | FEATURE WITH CAVEAT: Wispr Flow is free for basic use, so "free alternative" only beats its paid Pro; say "Pro costs $12 a month" |
| 6 | opf/openproject: 17,407, GPL-3.0, 2012 | Mature project management; describes itself as a JIRA alternative; self-host or their cloud | Asana Starter $10.99/user/mo billed yearly, asana.com/pricing | FEATURE WITH CAVEAT (it is a Jira-style tool, heavier than Asana; self-hosting is technical). Not in our set |
| 7 | calcom/cal.diy: 50,053, MIT, 2021 (calcom/cal.com now opens cal.diy) | Community edition of Cal.com; README: "strictly recommended for personal, non-production use", self-hosting "requires advanced knowledge" | Calendly Standard $10/seat/mo billed yearly, calendly.com/pricing (Calendly also has a free plan) | FEATURE WITH CAVEAT: say "for personal use, you host it yourself"; the reel's "replaces Calendly" is too strong |
| 8 | chatwoot/chatwoot: 39,919, licence "Other" (MIT core plus a separate enterprise folder), 2019 | Mature shared inbox for chat, email, WhatsApp; "open-source alternative to Intercom, Zendesk" | Intercom Essential $29/seat/mo monthly, $19 billed yearly, plus $0.99 per AI answer, intercom.com/pricing | SAFE TO FEATURE (say "free to host yourself"; their cloud is paid) |
| 9 | CapSoftware/Cap: 25,103, licence "Other" (check the LICENSE file before naming one), 2023 | Screen recorder with share links; "the open source alternative to Loom"; self-host or their paid cloud | Loom Business $18 per user/mo, loom.com/pricing (billing period not shown in the fetch; Loom has a free plan with 25 videos, 5-minute limit) | SAFE TO FEATURE (licence shown as "open source", not "MIT") |

Corrections to the reference: its star counts are already outdated (VoiceStudio 99.9K then, 111.7K now; Open Generative AI 32.2K then, 35.0K now); Chatwoot is not plain MIT; Cal.diy itself warns against business use; Open Generative AI is not free to use; most paid tools on the list have a free plan.

## 3. Duplicate check (16.11.2026)
grep of `channel/topics-covered.txt` and `channel/content-memory.md` for github, open source, repo, free alternative, notion, loom, calendly, elevenlabs, wispr, replace: only hit is episode 16 "Someone open-sourced our own video pipeline" (one tool, a different angle) and a production note about episode 26. No listicle of free alternatives has been published. NOT a duplicate. It is also a new format (not the chat-test class David is bored of).

## 4. Topic verdict (first, per the topic rule)
Why a stranger cares today: money they pay every month for apps they know by name (Loom, Notion, Calendly, ElevenLabs), felt in 3 s; named brands are checkable; a list is saveable and sendable. Weak side: it is not an AI story at its core (only VoiceStudio, OpenWhispr and AppFlowy's AI make it one), the audience that can self-host is narrow, and none of the three canon winners is a listicle, so this is an EXPERIMENT of a new format, not an extension of a proven one. Better than the queue? It is the only queued idea with an outside proof (1,414 likes, 609 comments on a faceless reel) and a saveable payoff; I rank it above Q2/Q3 for reach, below a proven chat test for expected views.

## 5. The video, most viral form for us
Faceless, Miki style (recipe `video/ep89c/`), Roni's "not AI-looking" rule: real logos, real screenshots of each repo's own README/app images, paper/receipt texture. Present tense, plain English, no code, no "self-host", no "repo" on screen except the word GitHub and its real logo.

### Item set (6, ordered by rising surprise, best teased early and paid off last)
1. Loom -> Cap (screen recordings)
2. Notion -> AppFlowy (notes and docs)
3. Calendly -> Cal.diy (booking page; on-screen small line "personal use")
4. Intercom -> Chatwoot (customer messages in one inbox)
5. Wispr Flow -> OpenWhispr (talk, it types)
6. ElevenLabs -> VoiceStudio (clone your own voice, on your own computer) = the payoff, teased from beat 2 as a greyed sixth slot "the big one".

### The visual mechanic (our own, not his grid)
A long paper RECEIPT titled "Your apps, every month" with six real logos and real "from" prices (Loom $18, Notion $10, Calendly $10, Intercom $19, Wispr Flow $12, ElevenLabs $6 = TOTAL $75 a month). Each beat stamps one line "FREE" and the total runs DOWN ($75 -> $57 -> $47 -> $37 -> $18 -> $6 -> $0): the running total is the counter and the reason to stay. Note on screen in small print: "cheapest paid plan, per person, Nov 2026". Prices mix monthly and yearly billing (Intercom $19 and Calendly $10 are yearly rates): the receipt says "from".

### Hook (about 6 words, statement, surprise first, names the products)
- Option A (recommended): "Loom, Notion, Calendly. Free twins exist." spoken as one flowing line with commas; frame 0 = the receipt with three big real logos, "$75 a month" and a "FREE TWINS" stamp (3 text items in all).
- Option B: "You pay $75 a month. Stop." (stronger stake, but names no product in the words: fails the first-second subject rule unless the logos carry it).
- Test both with a blind reader on frame 0 before building ("what is this about? would you stop?").

### Beat list (target 32-36 s) with what is new per beat
| t | Spoken (draft, present tense) | Picture | What is new |
|---|---|---|---|
| 0-2.2 | "Loom, Notion, Calendly. Free twins exist." | Receipt, 3 big logos, $75/month | The stake: money + named apps |
| 2.2-4.5 | "Six apps. Seventy-five dollars a month. Watch it hit zero." | Receipt unrolls to 6 lines; slot 6 greyed "the big one" | The promise (zero) and the teased sixth |
| 4.5-8 | "Loom records your screen. Cap does it free." | Loom line stamped FREE, Cap logo + real Cap app screenshot, total 57 | First proof, real screenshot |
| 8-11.5 | "Notion? AppFlowy. Notes, docs, even AI." | AppFlowy screenshot slides in, total 47 | AI enters |
| 11.5-15 | "Calendly? Cal dot diy, for your own bookings." | Booking page screenshot, small "personal use", total 37 | A caveat stated, keeps trust |
| 15-19 | "Intercom charges per answer. Chatwoot puts every message in one inbox." | Chatwoot inbox screenshot, total 18 | Reversal: per-answer fees |
| 19-23 | "Wispr Flow? OpenWhispr. You talk, it types." | Waveform -> text appearing, total 6 | Felt demo |
| 23-28 | "And the big one: ElevenLabs. VoiceStudio clones your voice on your own computer." | Slot 6 lights, VoiceStudio screenshot, total $0, receipt tears | The payoff saved for last |
| 28-31 | "Save the list. Send it to whoever pays for Loom." | Saveable card (below) | Save + named send |
| 31-33.5 | "The setup's in the link in bio." | Card stays | CTA (locked clip) |
| 33.5-35.5 | "Want the next one? Follow, and you'll see it." | Card + follow | Plain follow, no promised episode |

Build-up check: the open question ($75 -> $0, and what "the big one" is) closes visibly each beat; every beat adds a new app + a new kind of fact; a fresh reason to stay at ~8 s (AI appears) and at ~2/3 (per-answer fees, then the big one); no beat only describes the picture; the reveal is withheld from 2.2 s to 23 s. A blind reader must still mark the first beat where they would scroll.

### Saveable card (screenshot-able, inside the safe box x 108-972, y 269-1248)
"6 free twins" list: Loom -> Cap; Notion -> AppFlowy; Calendly -> Cal.diy; Intercom -> Chatwoot; Wispr Flow -> OpenWhispr; ElevenLabs -> VoiceStudio. Each row: both real logos, star count read on build day ("25K stars"), "free, open source". Footer: "Prices: cheapest paid plan, Nov 2026."

- Named person to send it to: "whoever pays for Loom" (the boss / the friend with a small business).
- Reason to watch twice: the total drops fast; the sixth slot is visible greyed from 2.2 s; the card is pausable.

### Real assets to source (official pages only, never redrawn)
Paid logos: Loom (Atlassian brand / loom.com press), Notion (notion.com brand page), Calendly (calendly.com brand), Intercom (intercom.com press), Wispr Flow (wisprflow.ai), ElevenLabs (elevenlabs.io brand). Free logos and app screenshots: each repo's own README images / official site (cap.so, appflowy.com, cal.diy, chatwoot.com, openwhispr.com, voicestudio.sh) and the GitHub mark from github.com/logos. Screenshots must be the product's own published images or our own capture of the real page, labelled as such.

### What we cannot test and how the video must word it
We have NOT installed or run any of the six. So: say "free alternative" / "free twin", never "works just as well" or "replaces"; never "save thousands"; the $75 is the sum of public cheapest plans, labelled "from"; say "free to host yourself" where the free path is self-hosting (Cap, Cal.diy, Chatwoot, AppFlowy self-host); voice cloning only of "your own voice". The caption and the `/e/102` setup page must list each repo link, licence, star count with the date read, and the honest caveats (Cal.diy personal use; Wispr Flow and Loom have free plans; VoiceStudio needs a strong computer). The setup path (explain-steps, English only) can only be "download from the official page" steps for apps with installers (Cap, AppFlowy, OpenWhispr, VoiceStudio); for Chatwoot and Cal.diy say plainly that hosting needs a server.

### Predicted views (judgement label, not a measurement)
HOOK 72, VIRALITY 70, OVERALL 70, PREDICTED VIEWS about 500 (range 250-1,200). Reasoning: strong money stake and saveable list, outside proof of engagement, but new format for us, not a chat-AI test like the canon three, and much of its value is for people who can install apps. Our median is about 240, top about 1,560.

### Open items before building
1. David: Publish mode, hook A vs B, and whether Cal.diy (personal-use warning) stays or OpenProject replaces it.
2. Re-read all stars and the Loom/Wispr billing period on the live pages on build day; check VoiceStudio's star history; read Cap's and Chatwoot's LICENSE files.
3. Blind-reader test on frame 0 and on the beat list.
