# Ivy ad: female voice tests (measured, not heard), 19.11.2026

Lines: L1 "You talk. Ivy drafts the email. Done." / L2 "ChatGPT knows your whole life. Your next AI shouldn't start from zero." All wavs 48 kHz mono, one TTS at a time under flock /tmp/tts.lock. No real person cloned or imitated, no David reference clip used.
Numbers: `measure.py` (same pyin method as audio/voice_quality.py: F0 median, p10-p90 range in semitones, end offset of last 0.7 s vs line median) plus Whisper small.en text. Output in `measured.txt`.

## What the repo/container has
- audio/voice/profile/: David's clone only (reference.wav, canon-*.wav locked lines). No female or stock reference clip anywhere in the repo.
- Two-voice episodes (audio/voice/ep72..79): second voice came from the "voice box" app (Kokoro under the name "AI - AW"), only WAV outputs are stored, no engine or voice pack in the repo.
- Chatterbox 0.1.7 in /opt/v311 (MIT) has a built-in default voice (conds.pt in the HF cache). Measured F0 median 135 Hz (L1) and 155 Hz (L2): male/androgynous range, range 11.8 st on L1, and it misread "drafts" ("draft") and "ChatGPT" ("TAT GPT"). NOT viable as a woman.
- Kokoro-82M (installed: pip kokoro 0.9.4, misaki, spaCy model; weights from Hugging Face hexgrad/Kokoro-82M). Preset voices, no cloning. Licence: Apache 2.0 for code and weights. UNCLEAR: the model card describes the training data as permissive/public-domain and synthetic; I did not verify the voice packs' provenance, so for a PAID ad get the licence line confirmed (low risk, not zero).
- Piper, XTTS, F5: not installed. XTTS-v2 (CPML) and F5 weights (CC-BY-NC) are non-commercial: out for ads. Piper (MIT code, per-voice licences vary) not tested.

## Measured results
| File | dur L1/L2 | F0 median | range L1/L2 | end L1/L2 | Whisper |
|---|---|---|---|---|---|
| kokoro af_heart (speed 1.0) | 3.02 / 5.03 s | 210 / 197 Hz | 8.7 / 7.6 st | -1.7 / +0.4 | exact |
| kokoro af_sarah (1.05) | 3.12 / 5.35 | 187 / 188 | 9.5 / 8.9 | -1.5 / +0.7 | exact ("YouTalk" run-together on L1) |
| kokoro af_bella (1.05) | 3.23 / 5.20 | 206 / 195 | 5.2 / 5.8 | -1.1 / +0.7 | exact |
| kokoro af_nicole (1.05) | 4.03 / 7.20 | 156 / 152 | 5.0 / 12.0 | -0.5 / +0.1 | exact, but slow and low |
| chatterbox default (exag 0.75, cfg 0.3) | 2.32 / 3.48 | 135 / 155 | 11.8 / 8.4 | -1.5 / +0.1 | two misreads |

## Ranking (energy and naturalness by numbers only; David must hear it)
1. af_heart: highest pitch, widest healthy range (7.6-8.7 st), fastest rate, exact text. Best energy candidate.
2. af_sarah: similar range, slightly lower pitch, one run-together word.
3. af_bella: clean but flat (5-6 st) = calmer.
4. af_nicole: F0 about 155 Hz (low), L2 range over 10 st and very slow.
5. chatterbox default: not female by pitch.
Ends are all within -1.7 to +0.7 st (no trailing off by this metric). Kokoro has no exaggeration control: more energy only via speed (1.1-1.15) or splitting into short sentences; not tested. Tone "assured": untested by ear.
