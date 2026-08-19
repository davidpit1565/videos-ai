# Getting this into GitHub

The GitHub app connected to this session can read and push to repositories, but it
**can't create one** — that permission isn't granted (`403: Resource not accessible by
integration`). So the repo has to be created by you. It's about 30 seconds.

## Option A — you create it, I push (recommended)

1. Go to **github.com/new**
2. Repository name: **`ai-videos`**
3. Visibility: **Private**
4. **Do not** tick "Add a README", "Add .gitignore" or "Choose a license" — the repo already
   has all three locally and an initialised remote will cause a conflict on first push.
5. Click **Create repository**, then tell me it's done.

I'll push both commits to `claude/universal-ai-engine-tutorial-tow3v7` and open a draft PR.

## Option B — push it yourself right now

Everything is already committed locally on branch
`claude/universal-ai-engine-tutorial-tow3v7`. After creating the empty repo:

```bash
git remote add origin https://github.com/davidpit1565/ai-videos.git
git push -u origin claude/universal-ai-engine-tutorial-tow3v7
```

## Option C — the bundle (works even if this container is gone)

`ai-videos.bundle` is the entire repository — both commits, full history — in one file.
Nothing is lost if this session ends before the repo exists.

```bash
git clone ai-videos.bundle ai-videos
cd ai-videos
git remote set-url origin https://github.com/davidpit1565/ai-videos.git
git push -u origin claude/universal-ai-engine-tutorial-tow3v7
```

## What's not in the repo

`.gitignore` excludes the rendered long-form MP4 and its narration WAV — together they're
several hundred MB, which is exactly the kind of thing that makes a git repo unusable.
Rebuild either one on demand:

```bash
python3 audio/build_vo.py video/tutorial.html audio/tutorial-narration.wav 1.30
./export/render.sh video/tutorial.html 1920 1080 1066 audio/tutorial-narration.wav \
  export/tutorial-1920x1080.mp4
```

The Reel's MP4 (4.5 MB) **is** committed — it's small enough to be worth keeping as the
reference render.

## Rebuilding on your own machine

The render pipeline needs four things, none of them exotic:

| Tool | Why | Install |
|---|---|---|
| Node + `playwright-core` | records the page headlessly | `npm i playwright-core` |
| Chromium | the renderer | comes with Playwright |
| `ffmpeg` | trims the pre-roll, encodes H.264, muxes audio | `brew install ffmpeg` / `apt install ffmpeg` |
| `piper-tts` + a voice | the narration | `pip install piper-tts` then `python3 -m piper.download_voices en_US-lessac-medium` |

The voice used for these renders is **`en_US-lessac-medium`**. Swap it in `audio/build_vo.py`
for a different one — or drop in your own recorded VO as a WAV and skip Piper entirely; the
render script doesn't care where the audio came from.
