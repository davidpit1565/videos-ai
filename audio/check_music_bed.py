#!/usr/bin/env python3
"""A real, systematic check that music actually sounds present — not just that a
music.wav file exists. Built after episode 27 shipped with a music bed that measured
fine on paper (present, correct level target) but had a ~5s near-silent dead zone
under the hook, and episode 29 drew the same complaint again from a different track
whose overall level was healthy but whose isolated bed still read as "no music" to
the ear it actually has to satisfy.

What this catches: a track that is technically present (nonzero samples, correct
integrated level after the final mix) but is too quiet on its own, or has a long
silent/near-silent stretch anywhere past the deliberate fade-in, to actually register
as music under narration. What this does NOT catch: whether the track's arrangement,
melody, or character sounds good — that is an ear call, not a measurement, and stays
David's to make every time (per CLAUDE.md: "voice decisions from measurement *and*
his ear — and when they disagree, his ear wins").

Usage: python3 audio/check_music_bed.py <music.wav> [--min-rms -24] [--max-silence 1.5]
Exits nonzero (and prints why) if the bed fails either bar.
"""
import argparse, subprocess, sys


def probe(path):
    out = subprocess.run(
        ["ffmpeg", "-i", path, "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    mean = maxv = None
    for line in out.splitlines():
        if "mean_volume:" in line:
            mean = float(line.split("mean_volume:")[1].split("dB")[0].strip())
        if "max_volume:" in line:
            maxv = float(line.split("max_volume:")[1].split("dB")[0].strip())
    return mean, maxv


def longest_silence(path, noise_db, after=2.0):
    out = subprocess.run(
        ["ffmpeg", "-i", path, "-af", f"silencedetect=noise={noise_db}dB:d=0.3", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    longest, start = 0.0, None
    for line in out.splitlines():
        if "silence_start:" in line:
            try: start = float(line.split("silence_start:")[1].strip())
            except ValueError: start = None
        elif "silence_duration:" in line and start is not None:
            try:
                dur = float(line.split("silence_duration:")[1].strip())
                if start >= after:
                    longest = max(longest, dur)
            except ValueError:
                pass
    return longest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--min-rms", type=float, default=-24.0,
                     help="the bed's own mean_volume must be at least this loud")
    ap.add_argument("--max-silence", type=float, default=1.5,
                     help="longest allowed near-silent stretch after the fade-in, in seconds")
    args = ap.parse_args()

    mean, maxv = probe(args.wav)
    if mean is None:
        sys.exit(f"could not measure {args.wav} — volumedetect produced no output")

    silence = longest_silence(args.wav, noise_db=args.min_rms - 6)

    print(f"{args.wav}  mean {mean:.1f} dB  peak {maxv:.1f} dB  longest quiet stretch {silence:.2f}s")

    fails = []
    if mean < args.min_rms:
        fails.append(f"mean level {mean:.1f} dB is below the {args.min_rms:.1f} dB floor — "
                      f"this bed will read as absent under narration")
    if silence > args.max_silence:
        fails.append(f"a {silence:.2f}s near-silent stretch (past the fade-in) exceeds the "
                      f"{args.max_silence:.1f}s cap — a real dead zone, same failure mode as episode 27")

    if fails:
        print("FAILED:")
        for f in fails:
            print(f"  - {f}")
        sys.exit(1)

    print("ok — music bed has a real, continuous presence")


if __name__ == "__main__":
    main()
