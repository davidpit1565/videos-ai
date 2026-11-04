# ChatGPT age reel, v6 (organic motion), 4.11.2026
33.21 s, 1080x1920, -14 LUFS, peak -1.2, freezedetect 0, safecheck 0 issues (measured by me and the build agent).
Motion: noise-driven drift, voice-reactive pulses, wobbly cursor and strokes, varied entrances. Median frame-difference 2.76 (v5 4.20, ep 82 1.32).
NOT done: music is synthesized (not the licensed library), voice_quality.py and check.sh not run, audio measured not heard, "teen" vs "team" needs David's ear. Quiet stretches at 9.5-10.5 s and 26.5 s. Confetti touches the last headline. Not in the studio yet.

## Update 4.11.2026: music replaced (David: the bed must come from our library, not be generated)
Bed is now `curious--inquisitive-curiosity--musictown.mp3` from `audio/music-library/` (cut by `audio/pick_real_track.py`), mixed with the real ducking. Bed minus voice in 300-3500 Hz: -7.9 dB, 10% of energy under 150 Hz (measured with voice_quality.py on the ducked bed). Alternatives built and measured: curious-circuits--sonican (-12.2 dB, 46% under 150 Hz), feel-good-beat--tunetank (-11.0 dB, 46% under 150 Hz). Chosen by measurement (least bass, so it carries on a phone), NOT by ear.

## Update 4.11.2026 (later): bed chosen by David
David heard the options in the Artifact player and picked the second: `cinematic--dramatic--themountain` (dramatic, documentary feel). The earlier lofi and musictown beds were rejected as "generic" and "childish". Measured: bed minus voice in 300-3500 Hz -11.5 dB, 48% of energy under 150 Hz (a little bass-heavy for a phone; the voice band is still inside the -6 to -18 dB window). `chatgpt-age-v6.mp4` in this folder now has this bed.
