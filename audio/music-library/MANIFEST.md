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

## Third batch, 16.10.2026: 54 tracks added by Claude Code (channel/music-sourcing-prompt.md)

Unlike the first two batches these were NOT listened to by David first: Claude Code
downloaded them from Pixabay Music, ran ffprobe plus `audio/check_music_bed.py` on a
30 s cut of each, and dropped the thin ones. **Mood labels (the filename prefix) are a
first guess from the title and the search keyword, and "no vocals" is unverified by ear.**
Listen and re-tag or delete anything that lands wrong. Kept: 60-200 s, mean level above
-24 dB, no quiet stretch. `pick_real_track.py` now rotates: a mood never reuses a track
from the last 3 picks (history in git-ignored `last-used.json`).

Dropped (not in this library): `curious--mystery-quirky--leberch` (mean -24.2 dB),
`cinematic--dramatic-cinematic-documentary--musicdream` (-27.5 dB),
`cinematic--documentary--leberch` (-28.4 dB), `minimal--minimal-piano-2--atlasaudio`
(-29.8 dB), all under the -24 dB floor; `bright--upbeat--alex-morgan` (41 s) and
`bright--bright-music--jonasblakewood` (51 s), too short; `punchy--hype-drill-music--kontraa`
(235 s), `curious--investigation--leberch` (264 s), `lofi--chill-lamp-light--ornave`
(218 s), over 200 s.

**Commercial / famous songs are never baked into an mp4.** Only Pixabay-licensed music
lives here; a song people know gets added inside Instagram when posting.

| File | Artist (Pixabay) | Duration | Mood (first guess) | Source URL | License | Date |
|---|---|---|---|---|---|---|
| `tense--airium-tense--leberch.mp3` | leberch | 122.0s | tense | https://pixabay.com/music/suspense-airium-tense-610770/ | Pixabay Content License | 16.10.2026 |
| `tense--tense-suspense--leberch.mp3` | leberch | 142.0s | tense | https://pixabay.com/music/suspense-tense-suspense-375422/ | Pixabay Content License | 16.10.2026 |
| `tense--suspense-tense-background-music--sigmamusicart.mp3` | SigmaMusicArt | 85.2s | tense | https://pixabay.com/music/crime-scene-suspense-tense-background-music-381891/ | Pixabay Content License | 16.10.2026 |
| `tense--palladium-thriller--leberch.mp3` | leberch | 116.0s | tense | https://pixabay.com/music/suspense-palladium-thriller-610771/ | Pixabay Content License | 16.10.2026 |
| `tense--thriller-tension--leberch.mp3` | leberch | 144.1s | tense | https://pixabay.com/music/ambient-thriller-tension-262903/ | Pixabay Content License | 16.10.2026 |
| `tense--suspense-tension-background-music--peacockmusic.mp3` | PeacockMusic | 180.9s | tense | https://pixabay.com/music/suspense-suspense-tension-background-music-485734/ | Pixabay Content License | 16.10.2026 |
| `tense--chase-percussive--echobrainz.mp3` | Echobrainz | 68.0s | tense | https://pixabay.com/music/chase-scene-chase-percussive-616744/ | Pixabay Content License | 16.10.2026 |
| `punchy--punchy--themountain.mp3` | The_Mountain | 138.0s | punchy | https://pixabay.com/music/corporate-punchy-151190/ | Pixabay Content License | 16.10.2026 |
| `punchy--fresh-urban-stomp--osynthw.mp3` | Osynthw | 65.2s | punchy | https://pixabay.com/music/upbeat-fresh-urban-stomp-345079/ | Pixabay Content License | 16.10.2026 |
| `punchy--punchy-brass-groovy-pop-track--moonpub.mp3` | Moonpub | 104.8s | punchy | https://pixabay.com/music/funk-punchy-brass-groovy-pop-track-478669/ | Pixabay Content License | 16.10.2026 |
| `punchy--trending-instagram-reels-music--bombinsound.mp3` | BombinSound | 94.0s | punchy | https://pixabay.com/music/future-bass-trending-instagram-reels-music-499599/ | Pixabay Content License | 16.10.2026 |
| `punchy--trending-instagram-reels-music--delosound.mp3` | DELOSound | 169.5s | punchy | https://pixabay.com/music/electronic-trending-instagram-reels-music-456261/ | Pixabay Content License | 16.10.2026 |
| `punchy--hip-hop-beat--themountain.mp3` | The_Mountain | 69.4s | punchy | https://pixabay.com/music/beats-hip-hop-hip-hop-beat-576571/ | Pixabay Content License | 16.10.2026 |
| `curious--mysterious-fog-curious-discovery--alex-morgan.mp3` | alex-morgan | 89.6s | curious | https://pixabay.com/music/electronic-mysterious-fog-curious-discovery-575877/ | Pixabay Content License | 16.10.2026 |
| `curious--curious-circuits--sonican.mp3` | Sonican | 98.1s | curious | https://pixabay.com/music/eccentric-quirky-curious-circuits-playful-electronic-music-411246/ | Pixabay Content License | 16.10.2026 |
| `curious--inquisitive-curiosity--musictown.mp3` | Musictown | 183.6s | curious | https://pixabay.com/music/suspense-inquisitive-curiosity-no-clock-tick-115377/ | Pixabay Content License | 16.10.2026 |
| `curious--mystery--soundpromusic.mp3` | SoundProMusic | 75.7s | curious | https://pixabay.com/music/mystery-mystery-473323/ | Pixabay Content License | 16.10.2026 |
| `curious--inquisitive-orchestra--musictown.mp3` | Musictown | 177.3s | curious | https://pixabay.com/music/main-title-inquisitive-orchestra-22215/ | Pixabay Content License | 16.10.2026 |
| `lofi--chill-lofi--zephiramusic.mp3` | ZephiraMusic | 137.4s | lofi | https://pixabay.com/music/lofi-chill-lofi-585360/ | Pixabay Content License | 16.10.2026 |
| `lofi--lofi-chill--zephiramusic.mp3` | ZephiraMusic | 148.8s | lofi | https://pixabay.com/music/lofi-lofi-chill-612445/ | Pixabay Content License | 16.10.2026 |
| `lofi--chill-lofi--velariomusic.mp3` | VelarioMusic | 160.6s | lofi | https://pixabay.com/music/beats-chill-lofi-616929/ | Pixabay Content License | 16.10.2026 |
| `lofi--lofi-night-haze--ornave.mp3` | Ornave | 124.1s | lofi | https://pixabay.com/music/lofi-lofi-night-haze-553402/ | Pixabay Content License | 16.10.2026 |
| `lofi--study-music--velariomusic.mp3` | VelarioMusic | 147.5s | lofi | https://pixabay.com/music/lofi-study-music-612039/ | Pixabay Content License | 16.10.2026 |
| `lofi--chill-beats--atlasaudio.mp3` | AtlasAudio | 119.3s | lofi | https://pixabay.com/music/lofi-chill-beats-606221/ | Pixabay Content License | 16.10.2026 |
| `confident--technology-corporate--themountain.mp3` | The_Mountain | 137.0s | confident | https://pixabay.com/music/corporate-technology-corporate-186320/ | Pixabay Content License | 16.10.2026 |
| `confident--technology-music--nastelbom.mp3` | NastelBom | 130.1s | confident | https://pixabay.com/music/corporate-technology-technology-music-602443/ | Pixabay Content License | 16.10.2026 |
| `confident--tech-innovation--themountain.mp3` | The_Mountain | 153.3s | confident | https://pixabay.com/music/corporate-tech-innovation-149935/ | Pixabay Content License | 16.10.2026 |
| `confident--tech--atlasaudio.mp3` | AtlasAudio | 115.2s | confident | https://pixabay.com/music/corporate-tech-613339/ | Pixabay Content License | 16.10.2026 |
| `confident--innovation--atlasaudio.mp3` | AtlasAudio | 152.0s | confident | https://pixabay.com/music/corporate-innovation-522427/ | Pixabay Content License | 16.10.2026 |
| `confident--abstract-technology--verclubmusic.mp3` | Verclub_Music | 164.6s | confident | https://pixabay.com/music/abstract-abstract-technology-608980/ | Pixabay Content License | 16.10.2026 |
| `confident--tech-corporate--themountain.mp3` | The_Mountain | 187.9s | confident | https://pixabay.com/music/corporate-tech-corporate-593075/ | Pixabay Content License | 16.10.2026 |
| `bright--upbeat-music--nastelbom.mp3` | NastelBom | 116.2s | bright | https://pixabay.com/music/upbeat-upbeat-upbeat-music-617071/ | Pixabay Content License | 16.10.2026 |
| `bright--upbeat--subclair.mp3` | Sub_Clair | 116.1s | bright | https://pixabay.com/music/upbeat-upbeat-607558/ | Pixabay Content License | 16.10.2026 |
| `bright--feel-good-music--paulyudin.mp3` | PaulYudin | 95.0s | bright | https://pixabay.com/music/modern-classical-feel-good-feel-good-music-573999/ | Pixabay Content License | 16.10.2026 |
| `bright--feel-good-music--starostin.mp3` | STAROSTIN | 170.0s | bright | https://pixabay.com/music/instrumental-feel-good-feel-good-music-590411/ | Pixabay Content License | 16.10.2026 |
| `bright--feel-good-beat--tunetank.mp3` | Tunetank | 163.3s | bright | https://pixabay.com/music/beats-feel-good-beat-350017/ | Pixabay Content License | 16.10.2026 |
| `cinematic--cinematic-dramatic--atlasaudio.mp3` | AtlasAudio | 162.0s | cinematic | https://pixabay.com/music/orchestral-cinematic-dramatic-606225/ | Pixabay Content License | 16.10.2026 |
| `cinematic--dramatic--themountain.mp3` | The_Mountain | 126.7s | cinematic | https://pixabay.com/music/orchestral-dramatic-610133/ | Pixabay Content License | 16.10.2026 |
| `cinematic--dramatic--prettyjohn1.mp3` | prettyjohn1 | 67.3s | cinematic | https://pixabay.com/music/epic-classical-dramatic-491632/ | Pixabay Content License | 16.10.2026 |
| `cinematic--epic-trailer--nastelbom.mp3` | NastelBom | 60.0s | cinematic | https://pixabay.com/music/main-title-epic-trailer-617062/ | Pixabay Content License | 16.10.2026 |
| `cinematic--epic-trailer-2--nastelbom.mp3` | NastelBom | 85.9s | cinematic | https://pixabay.com/music/orchestral-epic-trailer-602514/ | Pixabay Content License | 16.10.2026 |
| `minimal--ambient--nastelbom.mp3` | NastelBom | 151.3s | minimal | https://pixabay.com/music/ambient-ambient-495893/ | Pixabay Content License | 16.10.2026 |
| `minimal--minimal-piano--leberch.mp3` | leberch | 84.0s | minimal | https://pixabay.com/music/modern-classical-minimal-piano-590996/ | Pixabay Content License | 16.10.2026 |
| `minimal--minimal-ambient-background--audiodollar.mp3` | AudioDollar | 157.4s | minimal | https://pixabay.com/music/ambient-minimal-minimal-ambient-background-554921/ | Pixabay Content License | 16.10.2026 |
| `minimal--minimal-minimalist--solarflex.mp3` | SolarFLEX | 77.7s | minimal | https://pixabay.com/music/ambient-minimal-minimalist-569519/ | Pixabay Content License | 16.10.2026 |
| `minimal--ambient-soft--avelinemusic.mp3` | AvelineMusic | 133.7s | minimal | https://pixabay.com/music/ambient-ambient-soft-615314/ | Pixabay Content License | 16.10.2026 |
| `minimal--instrumental-minimal--themountain.mp3` | The_Mountain | 132.0s | minimal | https://pixabay.com/music/corporate-instrumental-minimal-522469/ | Pixabay Content License | 16.10.2026 |
| `triumphant--triumphant--kulakovka.mp3` | Kulakovka | 115.7s | triumphant | https://pixabay.com/music/main-title-triumphant-276654/ | Pixabay Content License | 16.10.2026 |
| `triumphant--triumph-triumphant-fanfare--mfcc.mp3` | MFCC | 73.4s | triumphant | https://pixabay.com/music/main-title-triumph-triumphant-fanfare-music-321091/ | Pixabay Content License | 16.10.2026 |
| `triumphant--victory-news-orchestral-anthem--sonican.mp3` | Sonican | 100.7s | triumphant | https://pixabay.com/music/main-title-victory-news-triumphant-orchestral-anthem-394549/ | Pixabay Content License | 16.10.2026 |
| `triumphant--success-music--paulyudin.mp3` | PaulYudin | 93.2s | triumphant | https://pixabay.com/music/corporate-success-success-music-518730/ | Pixabay Content License | 16.10.2026 |
| `triumphant--success--themountain.mp3` | The_Mountain | 104.3s | triumphant | https://pixabay.com/music/corporate-success-513166/ | Pixabay Content License | 16.10.2026 |
| `triumphant--great-achievement--themountain.mp3` | The_Mountain | 156.0s | triumphant | https://pixabay.com/music/main-title-great-achievement-155587/ | Pixabay Content License | 16.10.2026 |
| `triumphant--motivational-uplifting-success--denis-pavlov-music.mp3` | Denis-Pavlov-Music | 169.4s | triumphant | https://pixabay.com/music/corporate-motivational-inspiring-uplifting-success-achievement-empowering-617086/ | Pixabay Content License | 16.10.2026 |
