# Music: what was not downloaded, and where to get more (16.10.2026)

Nothing was blocked: Pixabay showed no Cloudflare or captcha wall in the browser, so
all 54 tracks were downloaded automatically (see `audio/music-library/MANIFEST.md`).

**The new mp3 files (205 MB) are on this computer only, in `audio/music-library/`, and
are not committed to git** (over the 80 MB limit set for the task). Back them up
yourself if you want them off this machine. Without them, a fresh clone cannot render
the new moods: `pick_real_track.py` exits with "missing track file".

If you want more of any mood, search by hand (Pixabay Music, filter Duration 1-3 min,
no vocals) and save as `audio/music-library/<mood>--<title-slug>--<artist>.mp3`,
for example `lofi--chill-lofi--zephiramusic.mp3`. Then add a row to MANIFEST.md and the
file name to `NEW[...]` in `audio/pick_real_track.py`.

| Mood | Search |
|---|---|
| tense / urgent | https://pixabay.com/music/search/tense%20urgent%20thriller/ |
| punchy / trending | https://pixabay.com/music/search/punchy%20trending%20reels/ |
| curious / mystery | https://pixabay.com/music/search/curious%20mystery/ |
| lofi / chill | https://pixabay.com/music/search/lofi%20chill/ |
| confident / tech | https://pixabay.com/music/search/technology%20corporate/ |
| upbeat / bright | https://pixabay.com/music/search/upbeat%20bright/ |
| cinematic / dramatic | https://pixabay.com/music/search/cinematic%20dramatic/ |
| minimal / ambient | https://pixabay.com/music/search/minimal%20ambient/ |
| triumphant | https://pixabay.com/music/search/triumphant%20victory/ |
