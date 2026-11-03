#!/usr/bin/env python3
"""Measured voice and music-bed quality checks that voice_doctor / check_accent do not cover.

Born 21.10.2026 from episode 74: David heard (1) a hook line with a "really bad tone" that
every automatic check passed, and (2) a background bed he could not hear, because the pinned
track was a sub-bass drone that a phone speaker does not reproduce. Nothing here replaces his
ear; each number only catches a failure that has already reached him once.

  /opt/v311/bin/python audio/voice_quality.py <narration.wav> <cues.json> [--music music.wav] [--vol 0.14]
  /opt/v311/bin/python audio/voice_quality.py <narration.wav> <cues.json> --mix <reel.mp4>   (HyperFrames reels)

cues.json is the old list [{"n":1,"line":"...","start":s,"end":e}] or the HyperFrames build's
{"lines":[{"n":"01-new","text":"...","start":s,"end":e}],"D":..}; both are read.
--mix: HyperFrames reels are mixed by the build, so no separate bed file exists. The bed is then
ESTIMATED as (finished mix) minus (best-fit gain x narration) and checked at volume 1.0. It is an
estimate, and the printed line says so; pass --music/--vol instead when the real bed file is known.

Checks:
  pitch     per spoken line: pitch range (p10-p90, semitones) and where the line ends relative
            to its own median. A hook swinging over 10 semitones, or ending more than 3.5
            below its median, sounded wrong (episode 74 line 1: 12.1 st, ending -4.4).
            Reference lines David liked: range 4.9-8.4 st.
  tone      a steady narrow tone in the voice stem longer than 0.6 s (hum, whine, ring).
  music     (with --music) the bed's share of energy under 150 Hz (a phone speaker drops it)
            and the bed-minus-voice level in the 300-3500 Hz band after --vol. Episodes 72 and
            73 measured -16.5 and -12.0 dB at the default volume.

Exit 1 when a check fails, so it can be wired into a gate. Uses librosa (/opt/v311/bin python).
"""
import argparse, json, subprocess, sys
import numpy as np


def load(path, sr):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def band_rms_db(x, sr, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / sr)
    m = (f >= lo) & (f <= hi)
    Y = np.zeros_like(X)
    Y[m] = X[m]
    y = np.fft.irfft(Y, len(x))
    return 20 * np.log10(np.sqrt((y ** 2).mean()) + 1e-12)


def norm_cues(raw):
    lines = raw["lines"] if isinstance(raw, dict) else raw
    return [{"n": c.get("n", i + 1), "line": c.get("line", c.get("text", "")),
             "start": float(c["start"]), "end": float(c["end"])} for i, c in enumerate(lines)]


def estimate_bed(voice, mix, out="/tmp/vq-bed-estimate.wav"):
    """music bed ~= mix - g*voice, g = least-squares gain over the whole file."""
    import soundfile as sf
    xm = load(mix, 48000)
    xv = load(voice, 48000)
    n = min(len(xm), len(xv))
    xm, xv = xm[:n], xv[:n]
    g = float((xm * xv).sum() / ((xv * xv).sum() + 1e-12))
    sf.write(out, (xm - g * xv).astype(np.float32), 48000)
    print("bed ESTIMATE: mix minus %.2f x narration (written to %s)" % (g, out))
    return out


def pitch_report(wav, cues):
    import librosa
    bad = []
    print("pitch (semitones vs each line's own median):")
    for c in cues:
        a, b = c["start"], c["end"]
        y, sr = librosa.load(wav, sr=16000, offset=a, duration=b - a)
        f0, _, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr, frame_length=1024)
        ok = ~np.isnan(f0)
        if ok.sum() < 10:
            continue
        st = 12 * np.log2(f0 / np.nanmedian(f0))
        rng = np.nanpercentile(st[ok], 90) - np.nanpercentile(st[ok], 10)
        t = np.arange(len(f0)) * 512 / sr
        tail = (t >= (b - a) - 0.7) & ok
        end = float(np.nanmean(st[tail])) if tail.sum() > 2 else float("nan")
        flag = []
        if rng > 10:
            flag.append("range over 10 st")
        if end == end and end < -3.5:
            flag.append("ends %.1f below median" % end)
        print("  line %3s  range %4.1f st  end %+5.1f  %s  %s" % (c["n"], rng, end, ("<-- " + ", ".join(flag)) if flag else "", c["line"][:48]))
        if flag:
            bad.append(c["n"])
    return bad


def tone_report(wav):
    from numpy.lib.stride_tricks import sliding_window_view
    x = load(wav, 48000)
    N, hop = 8192, 2048
    win = np.hanning(N)
    L = np.array([20 * np.log10(np.abs(np.fft.rfft(x[i:i + N] * win)) + 1e-9) for i in range(0, len(x) - N, hop)])
    f = np.fft.rfftfreq(N, 1 / 48000)
    prom = np.zeros_like(L)
    for t in range(L.shape[0]):
        pad = np.pad(L[t], 40, mode="edge")
        prom[t] = L[t] - np.median(sliding_window_view(pad, 81), axis=1)
    hit = prom > 18
    need = int(0.6 * 48000 / hop) + 1
    found = []
    for b in range(40, len(f) - 1):
        h = hit[:, b] | hit[:, b - 1] | hit[:, b + 1]
        run = best = start = bs = 0
        for t, v in enumerate(h):
            if v:
                if run == 0:
                    start = t
                run += 1
                if run > best:
                    best, bs = run, start
            else:
                run = 0
        if best >= need and f[b] > 60:
            found.append((f[b], best * hop / 48000, bs * hop / 48000))
    print("tone: %s" % ("none steady over 0.6 s" if not found else "%d steady tonal bins" % len(found)))
    for fr, d, t0 in found[:6]:
        print("  ~%.0f Hz for %.1f s from %.1f s" % (fr, d, t0))
    return bool(found)


def music_report(voice, music, vol):
    xm = load(music, 16000)
    xv = load(voice, 16000)
    X = np.abs(np.fft.rfft(xm * np.hanning(len(xm)))) ** 2
    f = np.fft.rfftfreq(len(xm), 1 / 16000)
    low = X[f < 150].sum() / X.sum()
    diff = band_rms_db(xm, 16000, 300, 3500) + 20 * np.log10(vol) - band_rms_db(xv, 16000, 300, 3500)
    print("music: %.0f%% of the bed's energy is under 150 Hz; bed minus voice in 300-3500 Hz at volume %.2f = %.1f dB" % (low * 100, vol, diff))
    fail = False
    if low > 0.6:
        print("  <-- mostly sub-bass: a phone speaker will not play it")
        fail = True
    if diff < -18:
        print("  <-- too quiet to hear on a phone speaker")
        fail = True
    if diff > -6:
        print("  <-- loud enough to fight the voice")
        fail = True
    return fail


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("cues")
    ap.add_argument("--music")
    ap.add_argument("--vol", type=float, default=0.14)
    ap.add_argument("--mix", help="finished mp4/wav with voice + bed; bed is estimated, volume 1.0")
    a = ap.parse_args()
    cues = norm_cues(json.load(open(a.cues)))
    if a.mix:
        a.music, a.vol = estimate_bed(a.wav, a.mix), 1.0
    bad = pitch_report(a.wav, cues)
    tone = tone_report(a.wav)
    mus = music_report(a.wav, a.music, a.vol) if a.music else False
    if bad or tone or mus:
        print("\nFAILED — listen to the flagged part before shipping")
        sys.exit(1)
    print("\nvoice quality: clean")
