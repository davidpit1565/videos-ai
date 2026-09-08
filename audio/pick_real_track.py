#!/usr/bin/env python3
"""Cut a real, licensed music-library track to an episode's exact length —
same contract as build_music.py (a total duration in, a ready music.wav out),
so produce.sh can point at either one interchangeably.

Usage: python3 audio/pick_real_track.py <seconds> <out.wav> --mood <mood>

Moods map to files in audio/music-library/ (see MANIFEST.md for what each one
actually sounds like and its real source/license). A track shorter than the
requested length is looped (audio/music-library/trending-vibe--alexmorgan.mp3
is the one 22s case); a longer one is trimmed from its start. Either way the
same fade-in/fade-out as build_music.py's own output, so the two are
interchangeable in render.sh without retuning levels.
"""
import subprocess, sys, os

LIB = os.path.join(os.path.dirname(__file__), "music-library")

MOODS = {
    "neutral":     "confident-corporate-story--echoes-of-lumen.mp3",
    "corporate":   "confident-corporate-story--echoes-of-lumen.mp3",
    "urgent":      "tense-suspense-rising-dread--alexmorgan.mp3",
    "tense":       "suspense-tension-building--arpmedia.mp3",
    "triumphant":  "success--paulyudin.mp3",
    "bright":      "upbeat-and-inspiring--atlasaudio.mp3",
    "lofi":        "vibraphone--alexmorgan.mp3",
    "retro":       "nostalgic-memories-piano--alexmorgan.mp3",
    "drive":       "video-editing--alexmorgan.mp3",
    "punchy":      "trending-vibe--alexmorgan.mp3",
    # tense-suspense-rising-dread, not suspense-tension-building: the latter opens on a
    # ~5s near-silent fade-in (measured -25 to -52 dB) that a straight from-0 trim landed
    # right on top of episode 27's hook, the one moment a quiet music bed can't afford to
    # be inaudible. alexmorgan's track is present from t=0 (measured -4 to -12 dB
    # throughout, no dead zone) and its dynamic range (17.9 dB) is much closer to
    # episode 26's upbeat-and-inspiring--atlasaudio.mp3 (15.4 dB) — the track David
    # pointed to as "sounds perfect" — than arpmedia's 33.2 dB swings.
    "suspense":    "tense-suspense-rising-dread--alexmorgan.mp3",
}


def probe_duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def find_audible_start(path: str, src_dur: float, total: float, max_skip: float = 8.0) -> float:
    """Where to start the cut so it doesn't land on a quiet intro. A track like
    suspense-tension-building--arpmedia.mp3 opens on a several-second near-silent
    fade-in (measured -25 to -52 dB) — trimming from 0 put that dead zone right under
    episode 27's hook. Finds the first point ffmpeg's silencedetect calls "loud enough"
    (-24dB) and starts there instead, capped so a track that's genuinely a slow build
    throughout doesn't get skipped past its own intended intro, and so there's always
    enough source left to cover `total`."""
    cap = min(max_skip, max(0.0, src_dur - total))
    if cap <= 0:
        return 0.0
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-t", str(cap + 2), "-i", path,
         "-af", "silencedetect=noise=-24dB:d=0.3", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    for line in out.splitlines():
        if "silence_end" in line:
            # "silence_end: 4.83124 | silence_duration: ..." — the loud point right
            # after the intro's initial silence, if any is found this early.
            try:
                return min(cap, float(line.split("silence_end:")[1].split("|")[0].strip()))
            except (IndexError, ValueError):
                pass
    return 0.0


def main():
    total = float(sys.argv[1])
    out = sys.argv[2]
    mood = sys.argv[sys.argv.index("--mood") + 1] if "--mood" in sys.argv else "neutral"
    if mood not in MOODS:
        sys.exit(f"no real track mapped for mood '{mood}' — pick one of: {', '.join(sorted(MOODS))}")

    src = os.path.join(LIB, MOODS[mood])
    if not os.path.exists(src):
        sys.exit(f"missing track file: {src}")

    src_dur = probe_duration(src)
    fade_in, fade_out = 0.3, 2.0
    fade_out_start = max(0.0, total - fade_out)

    filt = f"afade=t=in:st=0:d={fade_in},afade=t=out:st={fade_out_start}:d={fade_out}"
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if src_dur < total:
        # loop the short clip enough times to cover the requested length
        cmd += ["-stream_loop", "-1", "-i", src, "-t", str(total)]
    else:
        start = find_audible_start(src, src_dur, total)
        cmd += (["-ss", str(start)] if start > 0 else []) + ["-i", src, "-t", str(total)]
    cmd += ["-ac", "1", "-ar", "48000", "-af", filt, out]
    subprocess.run(cmd, check=True)
    print(f"wrote {out}  {total:.1f}s  mood={mood}  source={MOODS[mood]}")


if __name__ == "__main__":
    main()
