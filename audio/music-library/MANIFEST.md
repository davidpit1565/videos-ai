# Real music library — real musicians, not synthesized

Every track here is a real recording, downloaded by David from Pixabay Music
(pixabay.com/music/) after listening to it himself. This exists because
`audio/build_music.py`'s synthesized beds all started sounding too similar —
"real songs in the background, real melodies, not something AI" was the
explicit ask (6.9.2026).

**License, confirmed from pixabay.com/service/license-summary/**: free to use,
no attribution required, usable in monetized/commercial content. The only
restriction: don't resell the raw audio file itself as a standalone product.
Safe for a monetized Instagram account.

Pick a track with `audio/pick_real_track.py <duration> <mood> <out.wav>` —
it trims (or loops, for the one short clip) to the exact episode length with
a fade-out, the same contract `build_music.py` already has.

| File | Source (artist, Pixabay) | Duration | Suggested mood |
|---|---|---|---|
| `trending-vibe--alexmorgan.mp3` | alex-morgan | 22.5s | short punchy loop — needs looping for anything over ~20s |
| `tense-suspense-rising-dread--alexmorgan.mp3` | alex-morgan | 69.1s | urgent / tense |
| `confident-corporate-story--echoes-of-lumen.mp3` | echoes_of_lumen | 174.2s | neutral / confident / corporate |
| `success--paulyudin.mp3` | PaulYudin | 167.5s | triumphant / success |
| `vibraphone--alexmorgan.mp3` | alex-morgan | 181.3s | calm / lofi / warm |
| `nostalgic-memories-piano--alexmorgan.mp3` | alex-morgan | 168.0s | reflective / nostalgic / piano |
| `video-editing--alexmorgan.mp3` | alex-morgan | 157.8s | neutral / tech / everyday |
| `suspense-tension-building--arpmedia.mp3` | ARPMedia | 89.7s | tense / building |
| `upbeat-and-inspiring--atlasaudio.mp3` | AtlasAudio | 195.5s | bright / triumphant |
| `upbeat-energetic--maksymmalko.mp3` | MaksymMalko | 170.3s | bright / upbeat / energetic |
| `energetic--atlasaudio-2.mp3` | AtlasAudio | 93.2s | bright / energetic |
| `scary-horror--arpmedia.mp3` | ARPMedia | 104.1s | horror / scary (new mood, 16.9.2026) |
| `upbeat-energetic--lnplusmusic.mp3` | lNPLUSMUSIC | 138.9s | bright / upbeat / energetic |
| `energetic--ikoliksaj.mp3` | ikoliks_aj | 106.1s | bright / energetic |
| `upbeat-energetic--ikoliksaj-2.mp3` | ikoliks_aj | 99.0s | bright / upbeat / energetic |

These mood labels are a first-pass guess from the track titles and a quick
listen — re-tag any of them if they land differently once actually cut under
a real narration.

**Second batch added 16.9.2026 (David, listened and picked each one himself):**
gives "bright" its first real second/third/fourth option — `pick_real_track.py`
now picks randomly among a mood's candidates instead of always returning the
same file. Also adds a genuinely new mood, `scary`/`horror`, that didn't exist
before. Four duplicate uploads from the same session (re-downloads of tracks
already in this library — `success--paulyudin.mp3`,
`suspense-tension-building--arpmedia.mp3`,
`confident-corporate-story--echoes-of-lumen.mp3`,
`upbeat-and-inspiring--atlasaudio.mp3`, confirmed byte-identical by duration
and file size) were caught and skipped, not re-added.

Still only one option each for `neutral`/`corporate`/`confident`,
`urgent`/`tense`/`suspense`, `triumphant`, `lofi`, `retro`, and `drive` — pull
more real tracks for those the same way, one at a time, listened to and
picked by David first.
