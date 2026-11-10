# Music research, episode 92 (10.11.2026)

Episode: faceless English Reel, ~28-33 s, real dark-mode ChatGPT screen recording, no voice, music only. Beats: prompt, ChatGPT picks 47, "we won't be able to talk for 47 days", ChatGPT begs "Wait... can I have a second chance?", user says yes, ChatGPT picks 100, punchline "HAHAHAHA You gave me a second chance and I STILL chose 100". Tone: funny with a tender/sad twist, light, playful, typing sped up.

Status labels: SOURCED = a URL is given and was read in this session. HYPOTHESIS = untraceable or my inference. MEASURED = my own ffmpeg/numpy numbers on the library files. NOT HEARD = I have no ears; David's ear decides.

## 1. Evidence (research)

| # | Claim | Status | Source |
|---|---|---|---|
| 1 | Meta's ads guidance names audio (music, voiceover, sound effects) a key engagement driver on Reels and says to use the first few seconds to hook viewers. | SOURCED (secondhand summary of Meta guidance; the primary Meta page was not located) | https://www.flowjam.com/blog/ai-instagram-reels-ads , https://houseofmarketers.com/meta-shares-reels-tips-for-marketers-2026/ |
| 2 | "More than 75% of Reels views are sound on", attributed to Meta for Developers. | UNCONFIRMED: only secondhand; I could not open Meta's own page. Do not cite as fact. | https://www.flowjam.com/blog/ai-instagram-reels-ads |
| 3 | Emplifi analysis (March 2026, 10,110 brand Reels): speech in the first 3 s kept ~25% more viewers to 10 s than music-only openings. Third-party, brand accounts, correlation. Relevance here: ep92 has no voice, so the music-only opening carries the whole first 3 s; this is a reason the picture (the typed prompt) must do the hooking and the music must not be a passive pad. | SOURCED (third party) | https://www.pulse.bot/digital-marketing/news/human-speech-and-presence-help-drive-reels-engagement-26291baf-0b96-441f-aefa-8af987fa02e8 |
| 4 | Comedy sound design: a short silence/gap before a sound cue builds anticipation; a clean stop after it lets the reaction land; the beat is often the silence right after the last word, then the effect. | SOURCED (vendor/tutorial blogs, practical advice, not research) | https://sonilo.com/blog/guides/funny-sound-effects-for-videos , https://sfxengine.com/blog/sound-effects-timing-in-comedy-videos , https://www.finchley.co.uk/finchley-learning/comedy-video-editing-made-simple-a-fun-filled-videography-tutorial |
| 5 | Sound effects work only where they clarify a turn the picture already set up; do not put one on every line; test each cue with and without. | SOURCED (same editing guides) | https://sonilo.com/blog/guides/funny-sound-effects-for-videos |
| 6 | The "sad violin / strings over a ridiculous text" device is the best-known comedic-sad music trope in text-message content (the Jax and Lindsey Stirling video, Nov 2021, 2.4 M views). I found no source for a specific "sad piano" meme sound. | SOURCED for the violin trope only | https://www.boredpanda.com/woman-reading-cheating-ex-text-sad-violin-lindsey-stirling-jax/?media_id=51 , https://www.good.is/she-added-sad-violin-music-to-her-cheating-ex-s-apology-and-the-result-is-a-masterpiece-ex1/ |
| 7 | A ChatGPT-conversation video maker offers optional typing sounds and expects music to be added in the posting app. Shows typing ticks are a normal convention in this format, nothing about effect on reach. | SOURCED (tool page, weak) | https://www.trymypost.com/ai/chatgpt/video |
| 8 | Pixabay licence: free use, modification allowed, no attribution required; you may not sell or distribute the content on a standalone basis; branded/trademarked content cannot be used commercially for goods and services. Content ID not mentioned on the summary page; the full Content License is the binding text. Fetched live 10.11.2026. | SOURCED | https://pixabay.com/service/license-summary/ |
| 9 | Genre, tempo range and instruments of tracks under viral AI-chat reels specifically, drop timing, "silence vs music" effect on retention. | NOT FOUND. No traceable data. Everything on tempo and energy curve below is HYPOTHESIS. | none |

The three searches (Instagram audio guidance, ChatGPT chat reels, comedic silence) found no per-genre or per-tempo data for this format. The brief below is my judgement from the comedy-timing guides (4, 5), the violin trope (6), and our own `channel/music-notes.md` (character beats generic; bed must read on a phone speaker).

## 2. Brief (HYPOTHESIS, judgement not measurement)

- Feeling in 3 words: playful, tender, deadpan.
- Tempo: 95-120 BPM, steady and not driving. Fast typing needs a bed that does not compete with the ticks; a 132+ BPM bed would feel like a hype reel and flatten the sad twist. Library BPM below are crude onset-autocorrelation estimates (half/double ambiguity), treat +/- a factor of 2 as possible.
- Instruments: mallets (vibraphone, marimba, glockenspiel), pizzicato strings, soft piano, light plucks, a little muted bass. Avoid: corporate synth pads, stock "inspiring" builds, sub-bass drones, trap hats, big drums.
- Energy curve across ~30 s:
  - 0-3 s: already present at full character (no slow fade-in; the music-only opening has no voice to carry it). Light, bouncy, quiet-ish.
  - 3-14 s (prompt, 47, "47 days"): keep steady and sparse; this is where the typing ticks sit.
  - ~14-19 s (the begging line, "Wait... can I have a second chance?"): soften. Drop the rhythm layer or duck the bed 6-8 dB so a single tender melodic note or strings swell is exposed. This is the sad twist.
  - Yes / ChatGPT picks 100 (~19-24 s): bed returns to the opening groove, slightly brighter, as the setup for the reveal.
  - Punchline ("HAHAHAHA ... I STILL chose 100"): a deliberate cut of the bed to near silence for ~0.3-0.5 s right before the line appears (comedy-timing, claim 4), then the groove comes back with a small sting; hold the last 2 s as a clean loop-friendly tail or an abrupt stop on the 💀. Fade-out only if the reel does not loop.
- Sting / sfx placement (cues only; exact times come from the build's timeline, I do not have ep92's final timings):
  - Begging reply: one soft cue only, as the bubble appears. `video/ep90/sfx/ding.ogg` (0.53 s) is the best fit, a gentle confirmation tone that reads as "tender"; alternative `pop_b.ogg` (0.24 s, a soft plop). No impact or whoosh here.
  - "yes" from the user: `select.ogg` (0.21 s) or `click_a.ogg` (0.10 s).
  - Punchline: gap of silence, then `impactsoft.ogg` (0.57 s) on the 💀 beat; use `impactpunch.ogg` only if the bed is cut and the hit has to stand alone. Do not use `riser.ogg` (2.46 s): it telegraphs the joke; the comedy guides say the gap is the build-up.
  - Typing: `tick.ogg` (0.077 s) or `click_b.ogg` (0.009 s) per keystroke burst, not per character (sped-up typing); keep them 12-15 dB under the bed. `pop_a.ogg` (0.10 s) for each incoming message bubble.
  - Skip `riser`, `subhit`, `whoosh_*` for this episode; they belong to the torn-paper style, not a chat screen. HYPOTHESIS.

## 3. Library scan (audio/music-library, 69 mp3)

Method: ffprobe duration, a numpy onset-autocorrelation BPM estimate (crude), share of spectral energy under 150 Hz and in 300-3500 Hz over the first 30 s, and RMS of the first 3 s vs the 30 s mean. Nothing was listened to. `audio/check_music_bed.py` was not run per track; these are rougher screens. The existing library moods are first-guess tags from titles.

Raw numbers for the candidates examined (dur from MANIFEST):

| Track | Dur | BPM est. | <150 Hz | 300-3500 Hz | first 3 s vs 30 s |
|---|---|---|---|---|---|
| vibraphone--alexmorgan | 181 s | ~131 (or ~66) | 50% | 23% | -13.8 / -12.3 dB |
| nostalgic-memories-piano--alexmorgan | 168 s | ~131 (or ~66) | 14% | 60% | -16.9 / -14.6 dB |
| bright--feel-good-music--paulyudin | 95 s | ~101 | 12% | 84% | -20.9 / -17.8 dB |
| curious--inquisitive-curiosity--musictown | 184 s | ~109 | 13% | 84% | -15.5 / -15.0 dB |
| punchy--punchy-brass-groovy-pop-track--moonpub | 105 s | ~132 | 45% | 31% | -14.8 / -14.3 dB |
| lofi--lofi-night-haze--ornave | 124 s | ~82 | 39% | 37% | -18.6 / -18.1 dB |
| curious--curious-circuits--sonican (current) | 98 s | ~120 | 51% | 29% | -12.3 / -10.2 dB |
| trending-vibe--alexmorgan | 23 s | ~131 | 61% | 24% | -15.9 / -12.5 dB |
| bright--upbeat--subclair | 116 s | ~120 | 64% | 21% | -17.5 / -14.6 dB |
| bright--feel-good-beat--tunetank | 163 s | ~132 | 55% | 39% | -21.3 / -15.2 dB |
| minimal--minimal-piano--leberch | 84 s | ~147 | 51% | 24% | -19.9 / -20.1 dB (too quiet, as already logged for ep84) |
| lofi chill (zephira x2, velario x2, atlas) | 119-161 s | 70-178 | 58-80% | 10-23% | bass-heavy, soft intros; reject |

Note: the whole-spectrum percentages are share of energy, music is naturally bass-heavy, so a 50% under-150 Hz figure is normal for beat tracks; the earlier bar of 40% (ep84) is stricter than is needed when the music is the ONLY audio (there is no voice band to protect), but the phone-speaker point still holds: the tune must carry in 300-3500 Hz.

### Shortlist: 5 best for the brief (NOT HEARD, ranked)

1. `vibraphone--alexmorgan.mp3` (181 s, Pixabay alex-morgan). Mallet/vibraphone is the closest library match to "playful with a tender edge" (instrument fits the brief; calm/warm tag in MANIFEST). Used before: only as ep84 candidate D, never shipped. Caveat: 50% of energy under 150 Hz, and if the BPM is really ~131 it is brisker than the brief; check by ear. Cut from the start.
2. `bright--feel-good-music--paulyudin.mp3` (95 s). Modern-classical, light, 84% of energy in 300-3500 Hz so it carries on a phone, ~100 BPM, soft intro (-21 dB first 3 s, so start the cut a few seconds in). Fits the tender side, may be too gentle for the funny side. Already used on ep75 at vol 0.11. Flag: "feel-good" tag leans generic; judge by ear.
3. `curious--inquisitive-curiosity--musictown.mp3` (184 s). Sneaky/playful, ~109 BPM, 84% mid-band, 13% bass: the most phone-audible and least bass-reliant of the library. Weakness: already used on nextreel-git and as the family of ep88's bed (the tag "inquisitive" suggests "something is about to be revealed", which suits a joke setup but repeats the channel's sound). Use as safe fallback.
4. `nostalgic-memories-piano--alexmorgan.mp3` (168 s). Real piano, 60% mid-band, 14% bass; carries the tender beat best. Likely too sentimental as a bed for the whole reel, so use it only as a "sad twist" layer or if the final build splits the music (playful bed, then piano on the begging line). Risk: the title says "nostalgic memories", the tone may fight the joke.
5. `punchy--punchy-brass-groovy-pop-track--moonpub.mp3` (105 s). Playful brass groove, ~132 BPM; it was the ep84 runner-up for "playful". Funnier than tender; 45% under 150 Hz. Brass groove can read as a cartoon, which helps the punchline, but it ignores the sad twist. Option if David wants it comedic first.

Generic/corporate flags: avoid `confident--*` (all corporate/technology titles; the 3.11 "very generic" verdict was on `confident--technology-corporate--themountain`), `triumphant--*`, `bright--upbeat-music--nastelbom`, `bright--feel-good-beat--tunetank` (82/55% bass, thin tune), `upbeat-energetic--*`, `upbeat-and-inspiring--atlasaudio`. `lofi--*` beds measured bass-dominated and soft (58-80% under 150 Hz) and are indistinct under a phone speaker. `bright--feel-good-music--paulyudin` and `inquisitive-curiosity` are borderline-generic by title only; unverified by ear.

### The track used in ep92-final1

`curious--curious-circuits--sonican.mp3` (98.1 s; Pixabay title "Quirky Curious Circuits, Playful Electronic Music"; source URL in MANIFEST). Measured: ~120 BPM estimate, 51% of energy under 150 Hz, only 29% in 300-3500 Hz, first 3 s -12.3 dB (present from t=0, good), louder than most of the library. Fit verdict:
- Plus: it has character (quirky electronic), plays from the first second, tempo in range, was chosen for "playful, slightly odd".
- Minus: it is all-electronic and "curious/investigative" in colour, so there is nothing tender in it; under this brief the sad twist (the begging line) will not change the music's mood. It also has half its energy in the bass, which a phone speaker drops, so on a phone it may thin down to a tick and hiss. And on ep84 the same track was already marked "over the 40% bar" at -8.5 dB.
- Verdict: acceptable as a placeholder for the funny half, not a good fit for the "funny with a tender twist". HYPOTHESIS: a vibraphone/piano-led bed (shortlist 1, 2) plus a duck at the begging line would read warmer. Needs David's ear; I did not hear either.

## 4. Gap analysis and outside source

The library has no soft piano-plus-pizzicato "comedic-sad" track and no glockenspiel/marimba bed. Nearest free source: Pixabay Music (https://pixabay.com/music/), licence as in row 8 above (free, no attribution, no standalone resale, checked live 10.11.2026). Search terms to try, not downloaded and not listened to: "quirky pizzicato", "playful marimba", "comedic sad piano", "funny sneaky". The Pixabay licence summary does not mention Content ID; the full terms page was not read, and Instagram's own sound library (Meta Sound Collection, https://support.agorapulse.com/en/articles/16020547-how-to-add-audio-to-instagram-reels) is an alternative to adding a track inside the app, which CLAUDE.md already allows for famous songs. Anything newly downloaded still needs David to listen and a MANIFEST.md row.

## 5. Next steps for whoever builds ep92

1. Cut two or three of shortlist 1-3 to the exact reel length (the picker is random per run; use `FORCE_TRACK=<file>`), mix with the sfx cues in section 2, and run `audio/check_music_bed.py` plus a spectrum check.
2. Make the bed duck 6-8 dB at the begging line and cut to near silence for 0.3-0.5 s before the punchline.
3. Send David the options on one playable page (CLAUDE.md rule). His ear decides; log the pick in `channel/music-notes.md`.
