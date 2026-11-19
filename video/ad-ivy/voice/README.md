# Super Ivy ad narration (Kokoro af_heart), 19.11.2026

Voice: Kokoro-82M, preset voice af_heart (spare: af_sarah, tested, not used). Licence: Kokoro-82M is Apache 2.0; the origin of the voice-pack training data is unverified. Confirm before a paid ad. No real person cloned, no reference clip.
Script: channel/ad-ivy-plan.md section D with line 1 = "Re-explaining yourself to ChatGPT. Again." (lines-ivy.txt).
Files: narration-ivy.wav (48 kHz mono 16-bit), ../cues-ivy.json, words-ivy.json (Whisper small.en), takes/ (every speed 1.05/1.10/1.15 per line), gen_ivy.py, eval_ivy.py, stitch_ivy.py.
Picks: speed 1.15 for lines 1 and 7, 1.05 for lines 2, 5 and 8, 1.10 for the rest. Edge silence trimmed, inner pauses capped, each line gained to about -19.4 dB RMS, 0.09 s between lines.
No music file yet: voice_quality's music check was not run. Audio was measured, not heard.
Known: line 8 ends weakly ("up", last 90 ms about 26 dB under the line); line 5's "too" is read by Whisper as "2" and in the stitched file "and" as "in" (the raw take reads "and"); the hook has a Kokoro sentence break after "ChatGPT" (Whisper gap about 0.4 s, mostly a soft tail).
