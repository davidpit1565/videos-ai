# Voice and sound: how to get a human, energetic, motivating voice (research, 1.11.2026)

Status: research only. Nothing here was heard or run. No TTS model was started, no audio generated, no Firecrawl used.
Searches were done with Exa (web search/fetch). I read search highlights, not whole pages, except where noted.
Labels: FACT = stated by a source I name. HYPOTHESIS = my inference, must be tested with David's ear plus `audio/voice_quality.py`. UNKNOWN = I could not confirm.
Source quality: vendor pages and SEO blogs are marked (vendor) or (blog). Treat prices as of the dates in the sources and re-check before paying.

Repo context read: `CLAUDE.md` (voice section, voice_quality rule), `audio/voice/profile/profile.json`, `audio/build_voice.py` (flags and ffmpeg chain), `audio/voice_quality.py` (header), `scratchpad/v6/voice-targets.md`, `audio/music-library/MANIFEST.md`.

---

## 0. The core finding (read this first)

1. FACT (blog, localaimaster, 27.9.2026, summarising the model source code): Chatterbox conditions its token prompt on the first 6 s of the reference and its decoder on the first 10 s; the speaker embedding uses the whole clip. XTTS-v2 uses first 12 s for prosody, F5-TTS clips to about 12 s, IndexTTS-2 to 15 s. Everything after that is wasted for delivery.
2. FACT (profile.json in the repo): our current reference is a calm recording, and David's ear picked it. FACT (voice-targets.md, measured): a clone follows the source's melody; his own recording is median 120 Hz, 6-10 st range, ends about 0.
3. HYPOTHESIS (strong, consistent with 1 and 2 and with the Chatterbox README line "the model follows the melody of his recording more closely" in profile.json): the ceiling on energy is the first 6-10 s of the reference clip, not the settings. Settings and post-processing can move the numbers a little. A reference recorded in the target delivery moves the ceiling.
4. So the highest-value, lowest-cost action is one 10-minute recording session of David himself, doing the reference-reel style (high onset, falling endings, short lines, 0.25 s pauses). That session gives (a) a new energetic reference clip for Chatterbox, (b) real lines usable directly for hooks, (c) a test of whether his own voice at "TikTok energy" already beats every clone. Section 7 is the protocol.

Evidence on what "energetic" should mean, so we do not overshoot (FACT, Rodero 2022, Frontiers in Communication, 120 participants): medium pitch variation was rated most effective and attractive; many variations gave the most positive emotion; too many variations can sound exaggerated or unnatural. Earlier work cited there (Rosenberg and Hirschberg 2009, Niebuhr and Silber-Varod 2021): higher and varied pitch relates to perceived charisma. Implication (HYPOTHESIS): aim at the upper edge of the 10 st gate with a clear shape, do not chase the reference reel's 13-16 st (which was inflated by creak anyway, per voice-targets.md).

---

## 1. Ranked recommendation (effort / benefit)

| Rank | Action | Effort | Expected benefit | Risk |
|---|---|---|---|---|
| 1 | Record a NEW energetic reference (12-15 s, starts on speech) in the 10-minute session; A/B against the current reference on 3 lines | 10 min David + 30 min pipeline, one-time | HIGH (raises the ceiling; HYPOTHESIS, test) | His ear picked the calm one before (19.8.2026): the new one must win by ear AND by `voice_quality.py` start/end/range numbers; keep old reference |
| 2 | Hybrid: David records the hook lines (first 2-3 lines) live per episode, clone does the body | 3-5 min per episode | HIGH on the part viewers judge first (hook) | Mixed voices can sound uneven; match room tone and loudness; labeling still needed if any line is synthetic |
| 3 | Take selection by contour (6-8 seeds per line, score start/end/range) + per-line exaggeration 0.78-0.85 hooks / 0.64-0.70 instruction lines | already in voice-targets.md section "How to reach them" | MEDIUM | Swallowed words at high exaggeration (accent check is the guard) |
| 4 | Light post chain: end-of-line decrescendo, presence EQ, optional +1.5 st lift, duck music | 1-2 h to script once | LOW-MEDIUM (shape of level, not melody) | Over-processing sounds artificial; each step needs his ear |
| 5 | Text levers: short lines, commas for beats, "!" on hook beats, stressed word first, no ALL CAPS | free | LOW-MEDIUM | See section 3.3 for caps warning |
| 6 | Switch/add a model (Pocket TTS, Chatterbox Nano/Turbo, hosted) | high, uncertain | LOW for this problem (all clone the reference's delivery) | Loses levers (Turbo ignores exaggeration and cfg), licence, CPU speed |
| 7 | Voice conversion (Chatterbox VC, Seed-VC, RVC) from David's performance | high on CPU | LOW (direct recording of David already gives his voice) | GPU needed, GPL, archived repo |

Why not hosted first: FACT (ElevenLabs help, toolcolumn Oct 2026): cloning needs Starter ($6/month nominal; promo "$1 first month until Nov 8" on its own page, vendor). That fixes CPU limits but does not obviously fix the calm-reference problem (UNKNOWN: I found no source comparing hosted clones' expressiveness from a calm reference). It adds recurring cost and a credit meter (about 1 credit per character, 30k credits = about 30 min on Starter). Test only if section 7 fails.

---

## 2. Recording David's real voice (option 1)

### 2.1 Why phone, and the setup that sources agree on
FACT (several sources, consistent): room matters more than microphone. Sources: Distance Recordings 2026, Addaly (not dated), Mr. Vocal 2026, Shure guide, AudioEdit 2026, St Andrews blog 2023.
- Closet full of hanging clothes (or duvet over head and phone) is the standard cheap booth. Reverb cannot be fixed afterwards (Addaly). Bathroom and kitchen are the worst (Shure).
- Distance: 15-20 cm (6-8 in) from mouth to the phone's bottom microphone; slightly off-axis 15-30 degrees so plosives miss the capsule (Mr. Vocal, Addaly). A sock or fabric over the phone or a tissue between mouth and phone reduces plosives (Mr. Vocal claims about 6 dB, blog).
- Level: peaks around -12 to -6 dBFS, never clipping (Addaly, Distance Recordings). A quiet file can be raised, a clipped one cannot be repaired.
- Do not hold the phone; stand or tripod; towel under it if on a table. Airplane mode (Addaly, Distance Recordings). Use a voice-recorder app saved as WAV or high-bitrate, not the audio track of a video (Addaly).
- Leave 2 s of silence before and after each take (AudioEdit): needed for noise profile and clean cuts.
- If you stumble: pause 2 s, re-read the whole line from the start (AudioEdit): makes editing trivial.
UNKNOWN: which phone David has and where its mics are (iPhone: bottom edge near charging port per Mr. Vocal; Android varies). First step of the protocol asks him to check.

### 2.2 Energy delivery tips with some support
- FACT (blog, voice-director sources): "TikTok energy" in voice-over briefs means roughly 160-180 words per minute (about 2.7-3 words/s), hook in the first line, contractions, little announcer polish (realvotalent, 30.5.2026). Our v5 clone is at 3.75 words/s and the reference at 3.4, David's own at 3.2 (voice-targets.md): speed is not the gap.
- FACT (blog): "the camera subtracts": raise energy about 20 percent over normal conversation; smile while speaking; record the hook on its own in several versions (danilbogdan, realvotalent, suchavoice). The "jumping jacks" and "8/10 energy from word one" claims (pavone) are anecdote with an unverifiable view-count example; use the idea (start at energy, no warm-up), not the numbers.
- FACT (blog, suchavoice): energy is not speed; rushing blurs words. Pauses carry weight. Matches the reference's 0.25-0.38 s pauses.
- HYPOTHESIS: he may find the reference style (high onset, staircase down) easiest if he does NOT read but says each line to a person, from memory, after reading it once. Protocol uses "say it to a friend" cue and lets him choose which of 3 reads feels natural.

### 2.3 Use directly or clone from it
- Direct use: `audio/voice/profile/canonical-lines.json` maps exact line text to a pre-polished clip and `build_voice.py` loads it byte for byte (CLAUDE.md). So recorded lines already have a place in the pipeline. They still must pass `voice_doctor.py` and `voice_quality.py`.
- Clone from it: cut 12-15 s that starts on a word, ends on a finished sentence plus about 1 s quiet. Recipe from localaimaster (blog): `ffmpeg -i raw.wav -ss <start> -t 13 -ac 1 -ar 24000 -c:a pcm_s16le ref.wav`, then `loudnorm=I=-18:TP=-2:LRA=11`. Our existing construction (profile.json) deliberately put the best 10 s window first, because Chatterbox reads the opening seconds. Do the same: the opening 10 s must be the most energetic, cleanest speech.
- FACT (HF discussion on chatterbox-turbo, user report): Turbo mispronounced words when the reference was several minutes long; under 1 min was better (anecdote).
- UNKNOWN: whether lowering cfg_weight below 0.3 helps with an energetic reference. README says lower cfg_weight (about 0.3) with exaggeration 0.7+ for expressive speech; we are already at 0.30.

---

## 3. Improving Chatterbox output (option 2)

### 3.1 Settings (FACT, official README / model card)
- Defaults exaggeration 0.5, cfg_weight 0.5. Fast reference speaker: cfg about 0.3 improves pacing. Expressive/dramatic: cfg about 0.3 and exaggeration 0.7 or higher. Higher exaggeration speeds speech up; lower cfg slows it back down.
- If reference language and tag differ, set cfg 0 to stop accent bleed (not our case for English; relevant for Flemish, see CLAUDE.md "Flemish needs its own reference").
- FACT (HN user report, anecdote): the model guesses emotion from text and often gets it wrong; sometimes inserts noises at the start/end of short clips; mishandles numbers over two digits ("3:00 AM") and ALL CAPS words (may spell, yell or garble).
- Repo state: exaggeration 0.50, cfg 0.30, temperature 0.75 in profile.json; v4 episodes use about 0.78 (CLAUDE.md).

### 3.2 Which model variant (FACT)
- Original Chatterbox 500M (English): exaggeration and cfg levers. This is what the repo uses (it has `--exaggeration`, `--cfg`).
- Turbo 350M: paralinguistic tags `[laugh] [chuckle] [cough] [sigh] [gasp] [groan] [sniff] [shush] [clear throat]` (HF discussion, Resemble staff, 5.1.2026; user says "hit or miss"). Talemate docs: exaggeration, CFG/pace and min-p do NOT affect Turbo. So switching to Turbo removes the two levers we use for energy.
- Nano 110M: Resemble claims 3x realtime on 8 CPU cores. FACT (socialvik blog, 16.10.2026, own test): on a 6-core laptop Nano needed 1.93 s of compute per second of audio (slower than real time), Turbo 5.39 s per second. Rhapsode docs (Apple M5 Pro): Nano CPU 0.9-2.3x realtime, Turbo CPU about 0.8x (busy machine). chatterbox.cpp (GGML, Q4): Turbo on a Ryzen 9 9950X CPU about 1.2x realtime (vendor/repo benchmark).
- UNKNOWN: original-500M CPU speed in our container (not measured here, no models were run). The repo already generates on CPU, so it works; Turbo/Nano would not obviously be faster to switch to.
- FACT: every output carries the Resemble PerTh watermark; no setting to disable (socialvik). Relevant to the legal section.

### 3.3 Text tricks (mostly anecdotal, from GitHub issues; test, do not assume)
- FACT (cornball-ai port issue #5, quoting upstream behaviour): commas insert pauses; upstream rewrites `...`, `;`, `:` into commas; sentence-final `. ? !` shape phrasing; extra spaces do not work (3+ spaces break).
- FACT (resemble-ai issue #210): `[PAUSE]` style tokens are read aloud in the original model; a user reports hard returns (newlines) create longer pauses between sentences (anecdote). Repo already splits per line and sets gaps, which is the safer lever.
- FACT (cornball-ai port issues #2 and R docs): internal ALL CAPS caused silence or "first word only" in one port, later attributed to a port bug, and the port now leaves caps as emphasis. So caps behaviour is inconsistent across implementations. HYPOTHESIS: avoid ALL CAPS on the Python original; use word order and punctuation for stress. The repo's own `script_lint.py` is the arbiter.
- Original model has paralinguistic-like tokens in vocab per the cornball issue (`[UM]`, `[giggle]`, `[inhale]`, etc.), UNKNOWN whether they work in the version we run. A breath before a hook line is a cheap thing to test on one line.
- Chunk size matters: Talemate notes smaller chunks lose inflection context. Our per-line synthesis already trades this off.

### 3.4 Post-processing (our chain already exists; additions are HYPOTHESIS)
Existing chain in `build_voice.py` (read): highpass 75, EQ -1.5 dB at 240 Hz, +1.5 dB at 4.2 kHz, +2 dB at 7.2 kHz, deesser, acompressor ratio 2.2, loudnorm about -17.
Sourced general guidance for phone-speaker speech: high-pass 80-100 Hz; gentle compression; a small lift 2-5 kHz for presence, "a little"; light noise reduction only (jeffapierson reels audio guide, blog; deckready, vendor blog suggests 3:1 compression for talk reels). Do not add stronger compression: voice-targets.md notes our per-line level swing is already comparable to the reference.
Additions worth testing, each on 2 lines with his ear:
1. End-of-line decrescendo, -4 to -6 dB over the last 0.4 s (matches measured reference fade of 8-14 dB inside a line).
2. Whole-voice lift of +1.5 st with `rubberband=pitch=1.09:formant=preserved` (from voice-targets.md; beyond +2 st sounds processed).
3. Breath sounds: HYPOTHESIS only. A real inhale (from the 10-minute recording, 0.15-0.25 s) placed 0.05 s before the hook may add "human". No source measured this; test and keep only if his ear approves.
4. Do not "fix" with time-stretch: `retime.py` already moves the picture to the voice.

### 3.5 Measurable gates already in repo
`voice_quality.py`: range over 10 st fails; end below -3.5 st fails; tone and music-bed checks. voice-targets.md notes the gate was set from lines he liked (4.9-8.4 st) and the ep 74 hook that failed (12.1 st, end -4.4). Keep the gate, add a start-offset metric (see section 9).

---

## 4. Alternatives, cost, licence, cloning, CPU fit (option 3)

All licence/price data below is from sources named; re-verify before relying. "Fits CPU container" is judged from source numbers, not measured by me.

| Model / service | Cost and licence | Clones a voice? | English quality (source) | CPU-only container? |
|---|---|---|---|---|
| Chatterbox 500M (current) | free, MIT code and weights (Awesome TTS; socialvik) | yes, about 5-10 s | Resemble's own blind test: 63-65% preferred Chatterbox over ElevenLabs (vendor study, Turbo version in one report) | works in repo (slow); no number measured here |
| Chatterbox Nano 110M / Turbo 350M | MIT; Turbo/Nano ignore exaggeration/cfg (Talemate); tags supported | yes | not independently compared | Nano 1.8-1.9x slower than real time on a 6-core laptop (socialvik 16.10.2026); Turbo 5.4x slower |
| Kyutai Pocket TTS 100M | MIT; model card prohibits cloning without explicit consent (HF card); trained on public English data | yes, about 5 s, captures emotion, accent, cadence and mic/room (Kyutai report) | Kyutai's table: WER 1.84, audio-quality ELO 2016 vs Chatterbox Turbo 2055, speaker similarity ELO 1898 vs 2012 (vendor evaluation, Librispeech, cleaned input) | YES: faster than real time on CPU, about 2.8x on 1 thread; smaller 18.2M/6.9M variants 9.9-12.6x (Kyutai blog 20.10.2026). English plus 5 languages (not Dutch/Flemish) |
| Kokoro-82M | Apache 2.0 | NO (54 preset voices) | strong narration for its size (blogs) | YES, 15x realtime on Apple M4 (michaelservices); a preset voice, not David |
| F5-TTS | code MIT, weights CC-BY-NC-4.0 (non-commercial) | yes | high, but 0.09x realtime on Apple M4 (michaelservices) | NO |
| XTTS-v2 | CPML non-commercial; Coqui shut down Jan 2024 (blogs) | yes | good | NO (CPU well below real time) |
| Orpheus 3B | Apache 2.0 | yes, with emotion tags | expressive (blog) | NO (needs about 8-12 GB) |
| Fish Speech / S2 Pro open weights | non-commercial weights | yes | strong | NO |
| ElevenLabs | Free 10k credits, no commercial use, no cloning; Starter $6: instant cloning and commercial licence, 30k credits; Creator $22 (elevenlabs.io pricing, toolcolumn 23.10.2026). Voice Changer (speech to speech) 1,000 credits/min | yes (Starter+); needs consent | top-tier; no head-to-head with our clone | n/a (hosted) |
| Cartesia | Free 20k credits (about 27 min); Pro $5: commercial licence and instant cloning from about 10 s (recatools 14.10.2026, directory blog) | yes (Pro) | vendor claims | n/a |
| Fish Audio | Free personal only; Plus $15: commercial (recatools 1.10.2026) | yes, about 10 s | emotion tags | n/a |
| Hume Octave | free 10k characters, commercial restrictions on free (costbench) | yes (paid) | UNKNOWN | n/a |
| Seed-VC (voice conversion) | GPL-3.0, repo archived 21.11.2025 (xportstudio, github) | zero-shot, 1-30 s reference | recommended GPU | NO |
| RVC | MIT; needs about 10 min of clean audio to train (xportstudio) | trained model | strong in the wild | GPU recommended |
| Chatterbox VC | part of Chatterbox, preserves source prosody and timing (LAION repo) | uses target 6-10 s | n/a | LAION repo: CPU about 20x slower than GPU |

Takeaways:
1. FACT: the licence trap is real. F5, XTTS, Fish, Higgs, Spark have non-commercial weights; Chatterbox, Pocket TTS, Kokoro, Orpheus are permissive. The channel and the services business are commercial, so non-commercial weights are out.
2. FACT: Kokoro and Piper do not clone (micdrop.dev, localaimaster). Useful only if David accepted a non-David narrator, which contradicts CLAUDE.md (voice is his clone).
3. Pocket TTS is the only permissive cloner that is comfortably real-time on CPU. It is a candidate for fast iteration and for A/B on the new reference (HYPOTHESIS: same source-follows-melody behaviour). Its speaker similarity was lower in Kyutai's own table. Do not replace Chatterbox without David's ear.
4. Voice conversion adds nothing over recording David directly, except cleaning up a noisy phone take into the clone timbre (not needed if the closet protocol is followed).
5. Hosted services: use only as an A/B experiment with a paid month (about $5-6). Cloning on any of them requires consent and verification (ElevenLabs: voice verification for professional clones; prohibits cloning without consent).

### 4.1 Ethics and law for cloning his own voice
- Consent: his own voice, his own consent. FACT: Pocket TTS and ElevenLabs prohibit cloning others without consent; for David himself there is no consent problem. Rule for the business: never clone a client's voice without written consent (`CLAUDE.md` never-fabricate spirit; not a legal opinion).
- Platform label, FACT (secondary sources quoting Meta's Help Center; I did not open the Meta page itself): Instagram requires the "Add AI label" for "realistic-sounding audio" made with AI, and gives "a reel narrated with a realistic AI-generated voiceover" as an example (sirency 1.10.2026, fastclips 4.10.2026, kompozy 22.5.2026). The line is realism, not ownership: "a cloned version of your voice reading a script" falls inside (sirency). Instagram also detects C2PA/IPTC signals automatically and may label anyway (speaksay, gradually). RECOMMENDATION: toggle the label on every reel that has any synthetic voice, and check whether this is already done. UNKNOWN: whether the label affects reach for voice-only AI (the documented reach limit is for AI-generated-person profiles, fastclips).
- EU AI Act, FACT (European Commission FAQ, 24.7.2026): Article 50 applies from 2 August 2026; providers must mark synthetic audio machine-readably (the Chatterbox PerTh watermark is a provider-side mark; whether it satisfies "interoperable" is UNKNOWN); deployers must disclose deepfakes (audio that resembles an existing person and would falsely appear authentic) clearly at first exposure; a personal non-professional exemption exists (ANCOM summary) and does not fit a business channel. UNKNOWN: whether David's own cloned voice narrating a tips reel counts as a "deepfake" under Art. 3(60). Lowest-risk practice: label + one caption line ("voice: AI version of mine"). Not legal advice; if the services business sells voice-clone work to clients, ask a lawyer.
- Mixed episodes (real hook + synthetic body): the platform label applies if any realistic audio is synthetic.

---

## 5. Sound design kit (option 4)

Caveat: the brief says the reference style uses typing ticks, whooshes, pops, stamp/buzz. I did not analyse the reference reel's audio; that list is taken from the brief. Repo fact: `video/style-samples-31-10/round5/mix.py` already synthesises pop, click, error buzzer, success chime and whoosh and mixes them with narration and music (README, 1.11.2026), not yet in `produce.sh` gates.

### 5.1 Which effects matter (HYPOTHESIS, from the brief plus editing practice)
| Effect | Job | When | Notes |
|---|---|---|---|
| Whoosh | motion between scenes | on zoom-through/cut | start the whoosh 40-80 ms before the visual change so the peak lands on it; short (0.25-0.5 s) |
| Pop | element/headline appears | on the first frame of text reveal | very short (0.04-0.06 s) |
| Typing tick | typed text on screen | one tick per 1-2 characters, jittered | irregular spacing; Motion rule "no stepped rhythm" (CLAUDE.md) applies to audio too |
| Click/tap | UI action in a screen recording | at the real tap | match the real frame |
| Stamp / thud | the key claim lands | at most once or twice per reel | low-mid thud, not sub-bass (phone speakers drop sub-bass, see music) |
| Buzz / error | "this fails" beat | on the contradiction reveal | short, dry |
| Ding / success | "it works" beat | at the fix | short, bright |
| Riser | build before hook payoff | 0.5-1 s | optional, use sparingly |
StoryCut's list of most-used SFX (blog) matches: whoosh on cuts, pop on captions, ding on tips, bass boom on the main claim, record scratch for jokes. Idea from that page worth keeping: pick two or three signature sounds and reuse them so videos sound like you (HYPOTHESIS: identity benefit, not measured).

### 5.2 Licence-free sources (verify the licence page on download)
- FACT: Freesound CC0 sounds are free for commercial use, no attribution (storycut curated 213 CC0 sounds; lotsofsounds CC0 soundboard; both blogs/sites). Individual Freesound files can be CC-BY (attribution needed): only take files marked CC0.
- FACT: SFXMint pack (14 sounds, CC0, whoosh, pop 0.06 s, typing, riser, impact, ding) and Wyzowl SFX Kit (320 sounds, CC0, 48 kHz 24-bit WAV, each with a sync point and a loudness value; whoosh about -24 to -20.5 LUFS, pop about -25 LUFS, keyboard keys -27 to -30 LUFS). Wyzowl says it was made with Claude; its licence page is on its own site. I did not open the licence text.
- FACT: Mixkit says all sounds are free under the Mixkit License (terms not read by me; UNKNOWN restrictions).
- FACT: the repo's music already comes from Pixabay with a confirmed licence (MANIFEST.md). Pixabay also hosts SFX; same licence summary (confirmed in the manifest for music; assume same, verify).
- Caveat FACT (storycut): CC0 sounds can be re-used inside someone else's registered track, producing a false Content ID claim; keep the Freesound link per file in a manifest.
- Record each SFX's source URL and licence in a manifest next to the files (same discipline as `audio/music-library/MANIFEST.md`).
- Sounds that are recordings of trademarked sounds (iPhone camera click, app notifications) are excluded by StoryCut; consistent with the repo's logo rule: use only real, licensed material.

### 5.3 Levels relative to the voice
Sources disagree because they measure differently. Use the repo's measured gate as the authority.
- Vendor blog (deckready): voice -12 to -8 dBFS, BGM -24 to -18, SFX -16 to -10; BGM 12-14 dB under voice; hook SFX at the start.
- Mix-engineering blog (mediastrategylab): music about 6 LU under dialogue while speaking, 3 LU in gaps; ducking attack 80-150 ms, release 300-500 ms.
- Reels guide (jeffapierson): duck music 12-20 dB while speaking; test on a phone speaker at low volume.
- Repo gate (CLAUDE.md, voice_quality.py): bed about -6 to -18 dB under the voice in the 300-3500 Hz band; measured by `--music`.
RECOMMENDED RULES (HYPOTHESIS, to be tuned by ear):
1. SFX peaks 4-8 dB under the voice peak, whoosh and pop quieter than stamp.
2. Never place an SFX on a stressed word of the voice; put it in the pause (0.25 s gaps already planned).
3. High-pass every SFX at 150 Hz; nothing below 150 Hz except at most one low thud (a phone speaker drops it).
4. Typing ticks lowest (-20 dB under voice or more) and jittered.
5. Total target -14 LUFS, true peak -1 dBTP (see section 6). The first 5 s short-term loudness should not be 4-6 LU under the average (mediastrategylab claim, blog).

---

## 6. Music (option 5)

### 6.1 How loud and what genre
- FACT (several blogs, consistent): loudness target for Reels/TikTok/Shorts about -14 LUFS integrated, true peak -1 dBTP. jeffapierson notes none of the platforms publishes an official Reels target in its help centre: it is a working target. Repo already masters to -14 LUFS / -1 dBTP (CLAUDE.md).
- FACT: phone speakers produce almost nothing below about 500 Hz (loopin blog; consistent with ep 74 sub-bass drone failure in CLAUDE.md). Choose beds with energy in 500 Hz - 5 kHz (the repo gate measures 300-3500 Hz).
- Genres: the library already has bright, confident, punchy, upbeat-energetic, triumphant, tense, lofi, minimal, cinematic (counted from filenames, 71 files). For "motivating" the fitting moods are punchy / upbeat-energetic / confident / triumphant (HYPOTHESIS, no source measured motivation per genre). Beds with a clear beat help cuts land on beats (blossom blog). Avoid vocals in the bed (masks speech); instrumental only.
- Per repo rule: real library only, `pick_real_track.py`, verify with `check_music_bed.py`.

### 6.2 Trending audio: what is actually known (2026)
- FACT (ishort.pro, 1,211 reels from users of a transcription tool, Jul-Sep 2026, vendor sample, not random): original audio median 198k views (n=885) vs licensed music 289k (n=148), but music reels were shorter; at matched lengths under 30 s original 365k (n=136) vs music 352k (n=63); against each creator's own median both scored 1.0x. Conclusion in the source: audio type alone did not predict a hit.
- FACT (same source quoting Social Media Today): Mosseri's ranking videos (Sept 2026) listed originality, recency, small-creator "breaking content" and larger models; audio was not on the list.
- FACT (postplanify, 25.4.2026, blog): from 1.3.2026 the Trending Audio tab is open to all public accounts. Business accounts still get a restricted, commercially cleared library; chart songs are mostly missing (planoly, blossai, versely). The Instagram help page says its licensed music library is for personal non-commercial use (versely quoting it, not read by me). UNKNOWN: whether @actually_works.ai is a creator or business account; it changes which trending sounds can legally be used. Our Pixabay beds avoid the question.
- CONTRADICTORY claims: chartlex (vendor) says audio is "a ranking input" citing an Instagram prediction of "go to the audio page"; versely echoes this. Both are vendor posts; I did not find Instagram's own page here. Treat as HYPOTHESIS: a trending sound gives a second door (audio page), not a proven ranking bonus.
- Spoken words are indexed by in-app search (blossai claim, vendor): voice is an asset, which is a reason to keep a clean, clear voice that the platform can transcribe. HYPOTHESIS.
- Practical conclusion: for a voice-led channel the sound of the voice is the lever; trending audio is optional and legally restricted. Test it as a deliberate experiment (`channel/experiments.md`), not as a default: one episode with a licensed-safe trending original sound at very low volume under the voice, same hook type and topic class as a control.

---

## 7. A concrete 10-minute recording protocol for David (one page)

Goal: get a clean, energetic reference clip, hook lines, and a breath/ambience sample. Use one phone, one room, one session. You do not need to be perfect: say the line to a friend.

Before (2 minutes)
1. Pick the closet with clothes (or sit on the bed with a duvet over your head and the phone). Not bathroom/kitchen/empty room.
2. Phone: airplane mode on. Open the built-in Voice Memos (iPhone) or Recorder (Android), set quality to lossless or highest (WAV or M4A high). Do not film video.
3. Put the phone on a stack of books or a tripod, bottom edge (microphone) pointing at you, 15-20 cm (a fist plus a thumb) from your mouth, tilted so it is slightly beside your mouth (about 30 degrees), not straight in your face. A sock over the phone is optional.
4. Test 10 seconds: say line 1 loudly as if to a friend. Play it back: peaks should land about -12 to -6 dB (if the app shows a meter: yellow, never red). If red, move 5 cm back.
5. Smile first. Stand, do not sit slumped (standing opens the voice). Water nearby.

Recording rules (apply to every take)
- 2 seconds of silence at the start and end, no talking, no touching the phone.
- Same distance every take.
- Mistake: stay quiet 2 seconds, then say the whole line again from its start. Keep going, do not stop the recording.
- Say it, do not read it: glance at the line, look away, say it from memory.
- Energy: about 20 percent more than normal chat. First word starts high, last words fall and get softer. Pause 0.25-0.4 s after the punch lines.

Script format (put it on your screen in this form)
- One line per row. Mark with CAPS the 1-2 words that get the push, a slash `/` where the pause goes, an arrow down at the end where the voice falls:
  `CHATGPT is a yes-man. / (down)`
  `It LITERALLY agrees with you on everything. / (down)`
- Use the real v6 script lines (the same ten as voice-targets.md) so the files can go straight into the pipeline.

The 10 minutes
- Minutes 0-2: setup and test (above).
- Minutes 2-4, Block A "reference": read the v6 lines 1-4 in one continuous take (no stop), at the target energy. Do this 3 times. This continuous 12-15 s of fast, high-onset speech is the future clone reference. The first 10 s of the best take matters most.
- Minutes 4-7, Block B "hooks": record each of lines 1, 2, 6, 10 three times, one after the other, each a different energy: (1) normal, (2) 20 percent more, (3) 40 percent more. You pick later by ear.
- Minutes 7-9, Block C "rest of the lines": lines 3, 4, 5, 7, 8, 9 two takes each. Commas in line 7 are the list beats, take a 0.3 s pause at each.
- Minute 9-10, Block D "room": 15 seconds of silence (room tone), then one breath in and out at normal volume, then one "hm" and one short laugh if natural (optional). These are for noise matching and optional breath sounds.

After (David or Claude, 20 minutes, not part of the 10)
1. Export WAV, do not edit on the phone. Trim each take (keep 0.3 s before the first word), name `d-<line>-<energy>-<take>.wav`.
2. Run `audio/voice_doctor.py` and `audio/voice_quality.py` on the best take of each line. Compare with the table in section 9.
3. Cut the reference: best Block A take, 12-15 s, starts on a word, ends on a finished sentence plus about 1 s quiet; resample 24 kHz mono; loudnorm -18 LUFS.
4. A/B (his ear): 3 lines generated from old reference vs new reference, with the same seed, exaggeration 0.78, cfg 0.30. He picks blind.
5. Register any recorded line he approves in `audio/voice/profile/canonical-lines.json` the same way as the locked closing line.

Consistency for future sessions: same closet, same phone position (mark the spot with tape), same time of day, same app and settings. A 2-minute top-up of the hook lines per episode is enough after the first session.

---

## 8. Experiments to run (cheap, in order)
1. New energetic reference vs old, blind A/B by David, 3 lines (section 7). Pass: he picks the new one and the numbers in section 9 improve.
2. Hybrid: recorded hook + clone body on one episode; check for a level/timbre jump at the join.
3. Pocket TTS with the same new reference on the same 3 lines (CPU, fast): only to see if it follows the reference's energy better than Chatterbox. Keep Chatterbox if his ear says so.
4. Decrescendo and +1.5 st lift on two lines (HYPOTHESIS, ear).
5. One reel with a trending-safe sound as a deliberate test (`channel/experiments.md`), later.

---

## 9. Measurable pass criteria for "sounds motivated"

Source for the numbers: `voice-targets.md` (measured, pyin, 16 kHz) and `voice_quality.py` gates, tightened from the reference reel and his own approved lines. These are targets, not a validated model of motivation (UNKNOWN: no study maps these numbers to "motivating"). The ear check always overrules.

Per line (spoken text, same cues as `voice_quality.py`):
1. Pitch range p10-p90: hook lines (1, 2, 6) 8-10 st; other lines 6-9 st. Hard fail above 10 st (existing gate), warn below 6.
2. Start offset: first stressed word median is +2.5 to +5 st above the line median (new metric to add).
3. End offset (last 0.7 s vs line median): -2.5 to -4.5 st on statements; at or above -3.5 on hooks if possible, never below -4.5 (existing gate floor -3.5 for pass).
4. Level fade inside a line: last word is 6-10 dB under the line's loudest word.
5. Median pitch: 140-148 Hz (+1.5 to +2 st) if the +1.5 st lift is used; otherwise David's natural median with the 120 Hz baseline and no claim about it.
6. Speech rate 3.3-4.2 words/s, not faster than the reference's 4.2 (`voice-targets.md`).
7. Pauses: 0.25 s default, 0.36 s after punch lines, 0.25-0.3 s at list commas (line 7), measured on the cues file.
8. No steady tone (existing `voice_quality.py` tone check) and no swallowed endings (`script_lint`, `check_accent.py`).

Whole episode:
9. Integrated loudness -14 LUFS (about 1 LU), true peak at or below -1 dBTP; first 5 s short-term loudness within 3 LU of the programme average (the mediastrategylab tip, blog).
10. Music bed -6 to -18 dB under the voice in 300-3500 Hz (existing gate); less than 85 percent of the bed energy under 150 Hz.
11. SFX: peaks 4-8 dB under the voice peak; none on a stressed word.
12. Phone-speaker test: play at low volume on a phone; every word of the hook understandable on first listen (Pierson).
13. Human gate (not measurable): David listens once and says the take is "more excited" without "off moments"; for each flagged line a re-roll or a recorded line replaces it. Say plainly in the handoff: measured, not heard.

---

## 10. UNKNOWN / not done
- Original Chatterbox CPU speed in our container: not measured (no model was run).
- Whether a new reference raises exaggeration headroom: untested HYPOTHESIS.
- Which Instagram account type is used; the Meta help page was not opened directly (secondary sources only).
- Whether his cloned voice counts as a deepfake under the AI Act: open legal question.
- Licence text of Mixkit and Wyzowl SFX Kit not read in full.
- Nothing in the voice-sound space here was checked against the actual reference reel's audio for SFX use; the SFX list comes from the brief.

## Sources (URL list)
- Chatterbox README/tips: github.com/resemble-ai/chatterbox ; huggingface.co/ResembleAI/chatterbox ; chatterbox-turbo tags: huggingface.co/ResembleAI/chatterbox-turbo/discussions/21 ; Nano: huggingface.co/ResembleAI/chatterbox-nano
- Reference length and engines: localaimaster.com/blog/voice-clone-sounds-robotic (27.9.2026)
- Talemate Chatterbox/Turbo parameters: vegu-ai.github.io/talemate/user-guide/agents/voice/chatterbox/
- CPU timing: socialvik.com/blog/chatterbox-tts-cpu-commercial-use (16.10.2026) ; rhapsode.dev/docs/engines/chatterbox ; github.com/gianni-cor/chatterbox.cpp ; michaelservices.net/notes/the-local-tts-license-trap (25.8.2026)
- Text tricks: github.com/resemble-ai/chatterbox/issues/210 ; github.com/cornball-ai/chatterbox/issues/2 and /5 ; news.ycombinator.com/item?id=45767776
- Licences: tts.mahimai.ca/open-source-and-open-weight-models/ ; micdrop.dev/blog/open-source-voice-cloning (28.10.2026) ; d-central.tech/local-voice-ai-models/
- Pocket TTS: kyutai.org/pocket-tts-technical-report/ ; kyutai.org/blog/2026-10-20-pocket-tts-small/ ; huggingface.co/kyutai/pocket-tts
- Voice conversion: github.com/plachtaa/seed-vc ; xportstudio.com/blog/seed-vc-vs-rvc (26.10.2026) ; github.com/LAION-AI/chatterbox-voice-conversion
- Hosted pricing: elevenlabs.io/pricing ; elevenlabs.io/docs/overview/administration/billing ; toolcolumn.com/learn/elevenlabs-free-vs-paid-plans (23.10.2026) ; recatools.com/ai-directory/cartesia/ and /fish-audio/ ; costbench.com/compare/cartesia-vs-hume-ai/
- Recording: mrvocal.com/posts/record-high-quality-voiceover-phone ; addaly.com/learn/motion-and-audio/sound-is-half-the-picture ; distancerecordings.com (24.2.2026) ; shure.com/en-us/insights/home-recording-guide-for-beginners ; audioedit.io/blog/recording-voice-overs-at-home ; digitalcommunications.wp.st-andrews.ac.uk (2023)
- Delivery: frontiersin.org/journals/communication/articles/10.3389/fcomm.2022.869084/full ; realvotalent.com (30.5.2026) ; suchavoice.com (7.2026) ; danilbogdan.com/learn/voice-pace-energy ; pavone.ai (anecdote)
- Loudness and levels: jeffapierson.com/journal_tools/training/11-reels/05-audio-for-reels.html ; mediastrategylab.com/tools/lufs-loudness-reference ; deckready.club/en/blog/instagram-reels-audio-en ; cutscore.io ; onloopin.com
- SFX: storycut.com/sound-effects ; lotsofsounds.com/soundboard/video ; sfxmint.com/sets/video-editing ; wyzowl.com/sfx-kit/ ; mixkit.co/free-sound-effects/click/
- Trending audio: ishort.pro/original-audio-vs-trending-sounds-instagram.html ; postplanify.com/blog/trending-audio-on-instagram ; planoly.com ; blossai.com ; versely.studio ; chartlex.com (vendor)
- Legal: digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act ; ancom.ro/en/ai-en/transparency-obligations-article-50/ ; sirency.com/blog/instagram-ai-label-rules ; fastclips.app/learn/instagram-ai-labels ; kompozy.io/how-to/disclose-ai-content-on-instagram
