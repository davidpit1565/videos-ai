# Music notes: how we choose, what we know, what we test (started 3.11.2026)

David (3.11.2026): "I do not know how to choose music, I am bad at it, I do not know how the hook in music works. Try to understand over time, from our own choices, and we improve each time." This file is that memory. Status of every line: FACT (in our files), HYPOTHESIS, UNKNOWN.

## What we know (FACT, from this repo)
- Source: only the real licensed library, `audio/music-library/` (about 70 Pixabay tracks, free, no attribution, David listened to them). `audio/pick_real_track.py <seconds> <out.wav> --mood <mood>` trims to the exact episode length with fades. Never `audio/build_music.py` for what ships.
- The music mood tags in MANIFEST.md are first-pass guesses from titles.
- The "tense"/"urgent" mood maps to a bass-drone track: 85% of its energy is under 150 Hz, present in the file but inaudible on a phone speaker (episode 74). Check the bed with `audio/voice_quality.py ... --music <wav> --vol <v>` (bed about 6 to 18 dB under the voice in 300-3500 Hz) and `audio/check_music_bed.py`.
- Past picks: ep 74 `confident--innovation--atlasaudio.mp3` at volume 0.22 (David chose it after the drone failed); ep 75 `bright--feel-good-music--paulyudin.mp3` at 0.11; ep 66 bed "A" chosen by David; ep 82 three beds A/B/C, David chose A.
- Episode 83 first cut: bed C `confident--technology-corporate--themountain.mp3` chosen by numbers (bed -8.0 dB under the voice in 300-3500 Hz, 21% under 150 Hz). Roni's verdict (3.11.2026): "very generic, change that". One listener, one opinion; but it matches the tag: corporate + technology.

## How a music hook might work (HYPOTHESIS, not measured by us)
1. The bed sets the feeling of the line: warning/suspense for a privacy warning, light and quick for a tip. A mismatch (a cheerful corporate bed under a scary line) reads as generic.
2. A bed with a recognisable character in its first seconds (a rhythm, an instrument) may help the first 3 s; a pad that could be under any video does not.
3. The bed must not fight the voice: keep it simple in the voice band.
None of this has data on reach for our channel. We have 80 episodes' views but music was never varied on purpose, so views cannot tell us.

## Selection routine (use it, then log it)
1. Write the feeling of the episode in 3 words (e.g. quiet, warning, personal).
2. List 5-8 candidates by mood tag; drop corporate/inspiring/technology/upbeat-generic tags unless the line really is that.
3. Cut each to the exact length under the real narration; measure (voice_quality --music, check_music_bed): audible on a phone, not a bass drone.
4. Send David 3 finalists (same picture and voice, only the bed differs). His ear decides; if he does not know, ask one outside listener (Roni) "which is less generic".
5. Log below.

## Log (add one row per episode)
| Ep | Track | Mood tag | Bed vs voice (300-3500 Hz) | Verdict (who) | Notes |
|---|---|---|---|---|---|
| 83 v1 | confident--technology-corporate--themountain | confident / corporate | -8.0 dB | "very generic" (Roni, 3.11) | replaced |
| 83 v2 | minimal--minimal-ambient-background--audiodollar (D) | minimal | -7.4 dB, 5% under 150 Hz | pending (David's ear) | picked by measurement; alternatives E curious--inquisitive-curiosity--musictown (-8.2 dB), F lofi--lofi-night-haze--ornave (-7.3 dB) |
| 84 A | curious--mystery--soundpromusic | curious | -7.6 dB, 64% under 150 Hz (FAIL: sub-bass) | not heard | rejected by numbers |
| 84 B | curious--curious-circuits--sonican | curious | -8.5 dB, 48% under 150 Hz | not heard | over the 40% bar |
| 84 C | punchy--fresh-urban-stomp--osynthw | punchy | -7.3 dB, 81% under 150 Hz (FAIL) | not heard | rejected |
| 84 D | vibraphone--alexmorgan | calm/warm | -7.3 dB, 50% under 150 Hz | not heard | over the bar |
| 84 E | minimal--minimal-piano--leberch | minimal | -7.8 dB, 54% under 150 Hz | not heard | too quiet (bed mean -20 dB) |
| 84 F | punchy--punchy-brass-groovy-pop-track--moonpub | punchy / playful | -7.8 dB, 44% under 150 Hz | not heard | runner-up, playful brass groove |
| 84 G | curious--mysterious-fog-curious-discovery--alex-morgan | curious | -9.2 dB, 77% under 150 Hz (FAIL) | not heard | rejected |
| 84 H (chosen) | curious--inquisitive-orchestra--musictown | curious | -7.8 dB at vol 0.37 (ducked -16.2 dB), 35% under 150 Hz | pending (David's ear) | picked by measurement only: only candidate under the 40% bar; feeling "quiet, slightly sneaky, light playful edge" |

## Ideas to test (deliberate experiments, log in experiments.md)
- Same style of episode with a character bed vs a neutral bed, compare average watch time (needs several episodes, not one).
- Ask David for 5 tracks he likes on first listen from the library and see what they share (tag, tempo, instruments).
