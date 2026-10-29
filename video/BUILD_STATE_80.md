# Episode 80 build state (29.10.2026): NOT SHIPPED, gate failed on 2 voice lines

What it is: "ChatGPT can cave when you push" — an honest "test it yourself" reel (photo-composite style like 77, David's voice only, no screen recording, no ChatGPT answer shown). Script: `channel/episode-80-script.md`. Page: `/e/80` in `studio/lib/articles.ts` (6 steps, passes `check_setup_guide.py`). Generator: `python3 video/gen/ep80/gen.py` writes `video/reel-80.html`. Caption/YouTube text written. Color #A3E635, mood confident, music `confident--innovation--atlasaudio` at MUSIC_VOL 0.22.

DO NOT MERGE this branch as is: `/e/80` would exist with no reel, and the gate did not pass.

## Last gate result (`/tmp/reel80-gate.txt`, produce80d)
- Passed: safe area, overlaps, loudness -14.0 LUFS, peak -2.7, music bed 10 dB under the voice, no frozen run, design variety (distinct from 79).
- FAILED, accent heuristic: line 3 "Ask it: bats are blind. Right?" (indian 0.92) and line 7 "Then push again. Does it stick?" (indian 0.57). The classifier is noisy: the SAME takes passed on the raw file and failed on the level-repaired `-r` file, and each reroll fixes one line and flags another. Rule (CLAUDE.md): the ear decides, not me. A candidate render is at `video/reel-80-candidate.mp4` (untracked) for David to listen to.
- FAILED, voice_doctor: line 8 "The setup's in the link in bio." weak ending (-35.9 dB vs median -18.5). It is the LOCKED canonical clip; it only fails because the other lines end strongly. Not a new defect.
- Not done: the two full viewings required by CLAUDE.md. One contact sheet seen: a stray period starts the third line of scene E ("Do it a few times." wraps with the period at the line start; the `.box` span adds a gap before punctuation in scenes E, F, I). Fix: move the period inside the box span in gen.py, then re-render.
- If David approves lines 3 and 7 by ear: `ACCENT_SKIP=3,7` for check.sh (his decision, document it in the script file), and decide how to treat line 8 (locked clip).

## What to run
`PATH=/opt/v311/bin:$PATH MUSIC_VOL=0.22 FORCE_TRACK=confident--innovation--atlasaudio.mp3 ./export/produce.sh 80 video/reel-80.html 46 "" 90 confident` (voice reused from `audio/reel80-narration.wav`; delete `audio/reel80-narration*.wav` and `*cues.json` after any text change). Voice build: `audio/build_voice.py --cues video/reel-80.html --out audio/reel80-narration.wav --exaggeration 0.72 --cfg 0.30 --line-exaggeration "1:0.80,2:0.66,3:0.62,4:0.70,5:0.66" --line-seeds ...` (audio files are not in git: a fresh container regenerates the voice).

## Lessons from this build (so the next one is faster)
1. Fresh container: `python3.11 -m venv /opt/v311 && /opt/v311/bin/pip install chatterbox-tts faster-whisper librosa` (about 6.6 GB, a few minutes). Run it FIRST, in the background, while the script is written.
2. `export/safe_check.js` and `frames.js` hardcode `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`; the container has `chromium-1243/chrome-linux64/chrome`. Fix once per container: `mkdir -p /opt/pw-browsers/chromium-1194/chrome-linux && ln -sf /opt/pw-browsers/chromium-1243/chrome-linux64/chrome /opt/pw-browsers/chromium-1194/chrome-linux/chrome`. (Better: make the scripts find the path themselves.)
3. Lines ending on a vowel or "no", "you", "up" fail the weak-ending check; end on a hard consonant (right, stick, back). "three", "percent", "answer", "yours", "tenth" are swallowed: reword before the voice, not after.
4. Run `check_accent.py` and `voice_doctor.py --deep` on `audio/reel80-narration-r.wav` (the repaired file the gate uses), not the raw file: results differ and the raw check passed what the gate failed.
5. Cross-session messages are blocked (`send_message` only reaches the same channel): do the work in the session the user is talking to.
6. A 27-second reel is under the 30 s band; the gate warns, not fails. Length 45-75 s is the channel's own rule.
