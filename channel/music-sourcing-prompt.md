# Prompt for Claude Code in the terminal — widen the music library (16.10.2026)

Paste everything under the line into Claude Code, run from the `videos-ai` repo on David's own computer
(his IP and browser are far less likely to hit Pixabay's bot check than the cloud session did).

---

Read CLAUDE.md first (the music rules, "Building and rendering"). Then do this end to end without asking me
to confirm each step. Answer me in Hebrew; code and file names in English.

**Problem.** Every episode ends up on the same 2-3 tracks out of `audio/music-library/` (mostly
`trending-vibe--alexmorgan.mp3`). I want a much wider library and automatic rotation.

**Task 1 — get more tracks (target: 30+ new, 5+ per mood).**
1. Source: Pixabay Music (https://pixabay.com/music/), the Pixabay Content License: free for commercial use,
   no attribution. Use the browser tooling available to you (Playwright / browser-use) like a normal user:
   search, preview, download the MP3. If Pixabay shows a Cloudflare / "Just a moment" / captcha wall, do NOT try
   to bypass it. Stop on that source, tell me exactly which searches to do by hand, and continue with Task 3.
2. Moods to fill (search 3-4 keyword variants each, pick tracks 60-150 s long, clean start, no vocals, no
   abrupt ending): `tense/urgent` (we have only 1), `punchy/trending`, `curious/mystery`, `lofi/chill`,
   `confident/tech`, `upbeat/bright`, `cinematic/dramatic`, `minimal/ambient`, `triumphant`.
3. Avoid: tracks with vocals, tracks that need a fade-in longer than 2 s to be listenable, anything
   with a sound-alike of a famous song, anything sampled from a commercial song.
4. Save each file as `audio/music-library/<mood>--<title-slug>--<artist>.mp3`.
5. For every file: `ffprobe` the duration, run `python3 audio/check_music_bed.py` on a 30 s cut
   (mean dB, peak dB, longest quiet stretch) and drop any track that reads thin or has a long quiet stretch —
   CLAUDE.md documents that exact failure on episode 29.

**Task 2 — wire them in.**
1. Add every kept track to `audio/music-library/MANIFEST.md` (file, artist, duration, mood, source URL,
   license = Pixabay Content License, date). Mood labels are a first guess — say so in the file.
2. Add them to `MOODS` in `audio/pick_real_track.py` (new moods allowed; keep every existing key working).
3. Rotation: make `pick_real_track.py` remember what it used. Write `audio/music-library/last-used.json`
   (last 5 picks, git-ignored), and when a mood has more than one candidate never choose a track used in the
   last 3 episodes. Falls back to any candidate if all were used. A test: call it 10 times for `punchy`
   and print the distribution.
4. Run `python3 audio/pick_real_track.py 30 /tmp/t.wav --mood <m>` for EVERY mood and report that each
   works and what file it picked.

**Task 3 — a shortlist if sourcing was blocked.** Write `channel/music-todo.md`: the exact Pixabay search
URLs per mood for me to download by hand, and the file naming I expect.

**Hard rules.**
- No commercial songs (no "Me and the Devil", no ripped YouTube audio). Songs people know are added inside
  Instagram when posting, never baked into the mp4. Write one line about this in MANIFEST.md.
- Nothing from `audio/music-library/` that I haven't got a license line for.
- Do not touch voice, templates or any episode files.
- Work on a new branch from `origin/main`, open a PR, run what checks exist, merge it (CLAUDE.md: studio only
  reflects `main`). The tracks are small enough to commit; if the total is over 80 MB, commit only the
  MANIFEST/py changes and tell me where the files live.

**Report back (Hebrew, short):** how many tracks per mood, what you dropped and why, the 10-run rotation
distribution, anything blocked.
