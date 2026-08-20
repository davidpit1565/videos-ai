#!/usr/bin/env python3
"""Check a finished reel against the things that have actually gone wrong.

Every check here exists because a real defect got past a human eye: a frozen
picture while the voice had stopped, a colour card that flashed too fast to read,
a first frame with no hook on it, audio mastered off-target for the platform.

  python3 export/qa.py export/reel-01-QA.mp4 --build video/reel-01-kar.html \
      --vo audio/voice/ep01-v2.wav

Exit status is 1 if anything is a blocker. Run it before the file is sent.
"""
import argparse, json, os, re, subprocess, sys, wave
import numpy as np

W, H, FPS = 160, 284, 30           # decode small: this is about change, not detail
STATIC_WARN, STATIC_FAIL = 2.0, 4.0
LEN_MIN, LEN_MAX = 30.0, 90.0      # measured band for this kind of content
LUFS_TARGET, LUFS_TOL = -14.0, 1.5


def ffprobe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                          "-of", "json", path], capture_output=True, text=True).stdout
    return json.loads(out)


def gray_frames(path):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path,
                        "-vf", f"fps={FPS},scale={W}:{H},format=gray",
                        "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True)
    a = np.frombuffer(p.stdout, dtype=np.uint8)
    n = len(a) // (W * H)
    return a[:n * W * H].reshape(n, H, W).astype(np.int16)


def loudness(path):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
                        "-filter_complex", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    tail = p.stderr[-1400:]
    g = re.search(r"I:\s*(-?[\d.]+)\s*LUFS", tail)
    pk = re.findall(r"Peak:\s*(-?[\d.]+)\s*dBFS", tail)
    lra = re.search(r"LRA:\s*(-?[\d.]+)\s*LU", tail)
    return (float(g.group(1)) if g else None,
            max((float(x) for x in pk), default=None),
            float(lra.group(1)) if lra else None)


def runs_of(mask, fps=FPS):
    out, start = [], None
    for i, v in enumerate(mask):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((start / fps, i / fps))
            start = None
    if start is not None:
        out.append((start / fps, len(mask) / fps))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("--build", help="the HTML the render came from")
    ap.add_argument("--vo", help="the narration wav, for card-in-silence checks")
    ap.add_argument("--static-fail", type=float, default=STATIC_FAIL)
    a = ap.parse_args()

    bad, warn, clean = [], [], []

    info = ffprobe(a.mp4)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    au = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"]["duration"])
    fps = eval(v["r_frame_rate"])
    print(f"{os.path.basename(a.mp4)}  {v['width']}x{v['height']}  {fps:g}fps  {dur:.2f}s  "
          f"{int(info['format']['size'])/1e6:.1f}MB")

    if (v["width"], v["height"]) != (1080, 1920):
        bad.append(f"frame is {v['width']}x{v['height']}, not 1080x1920")
    else:
        clean.append("1080x1920")
    if v.get("pix_fmt") != "yuv420p":
        bad.append(f"pixel format {v.get('pix_fmt')} — social needs yuv420p")
    else:
        clean.append("yuv420p")
    if abs(fps - 30) > 0.01:
        warn.append(f"{fps:g} fps")
    else:
        clean.append("30fps")
    if au:
        if int(au["sample_rate"]) != 48000 or int(au["channels"]) != 2:
            bad.append(f"audio {au['sample_rate']}Hz {au['channels']}ch — want 48000/2")
        else:
            clean.append("48kHz stereo")
    else:
        bad.append("no audio stream")
    if not (LEN_MIN <= dur <= LEN_MAX):
        warn.append(f"{dur:.1f}s is outside the 30-90s band")
    else:
        clean.append(f"length {dur:.1f}s inside 30-90s")

    if a.build:
        src = open(a.build, encoding="utf-8").read()
        m = re.search(r"var DUR=([0-9.]+)", src)
        if m and abs(float(m.group(1)) - dur) > 0.05:
            bad.append(f"render is {dur:.2f}s, the build declares {m.group(1)}s")
        else:
            clean.append("length matches the build")

    f = gray_frames(a.mp4)
    diff = np.abs(np.diff(f.astype(np.int16), axis=0)).mean(axis=(1, 2))
    mean = f.mean(axis=(1, 2))

    still = np.concatenate([[False], diff < 0.35])
    for s, e in runs_of(still):
        if e - s >= a.static_fail:
            bad.append(f"picture frozen {e-s:.2f}s at {s:.2f}-{e:.2f}s")
        elif e - s >= STATIC_WARN:
            warn.append(f"picture nearly still {e-s:.2f}s at {s:.2f}-{e:.2f}s")
    if not any("frozen" in x for x in bad):
        clean.append(f"no frozen run over {a.static_fail:g}s")

    dark = mean < 8
    for s, e in runs_of(dark):
        bad.append(f"black frames {s:.2f}-{e:.2f}s")
    if mean[0] < 12:
        bad.append(f"first frame is blank (mean luma {mean[0]:.1f})")
    else:
        clean.append(f"first frame carries picture (luma {mean[0]:.1f})")
    if mean[-1] < 12:
        warn.append(f"last frame is blank (mean luma {mean[-1]:.1f})")

    # the full-frame colour cards: a bright frame filling the screen
    card = mean > mean.mean() + 3.2 * mean.std()
    cards = [(s, e) for s, e in runs_of(card) if e - s > 0.10]
    vo = None
    if a.vo and os.path.exists(a.vo):
        with wave.open(a.vo) as w:
            sr = w.getframerate()
            y = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        fr = int(0.02 * sr)
        env = 20 * np.log10(np.maximum(np.array(
            [np.sqrt((y[i*fr:(i+1)*fr]**2).mean()) for i in range(len(y)//fr)]), 1e-9))
        thr = np.percentile(env, 10) + 0.35 * (np.median(np.sort(env)[-int(len(env)*0.4):])
                                               - np.percentile(env, 10))
        vo = (env, thr)
    for s, e in cards:
        note = f"card {s:.2f}-{e:.2f}s ({(e-s)*fps:.0f} frames)"
        if e - s < 0.45:
            bad.append(note + " — too fast to read, reads as a glitch")
        if vo is not None:
            seg = vo[0][int(s/0.02):int(e/0.02)]
            if len(seg) and seg.max() > vo[1]:
                bad.append(note + " — plays over speech")
    if cards:
        clean.append(f"{len(cards)} colour cards, "
                     f"{min(e-s for s, e in cards):.2f}-{max(e-s for s, e in cards):.2f}s each")
        spacing = [round(cards[i+1][0] - cards[i][0], 1) for i in range(len(cards)-1)]
        print(f"  card spacing: {spacing}")

    changes = np.where(diff > diff.mean() + 0.8 * diff.std())[0] / fps
    if len(changes) > 2:
        gaps = np.diff(changes)
        print(f"  visual change: median {np.median(gaps):.2f}s, longest {gaps.max():.2f}s")
        clean.append(f"visual change every {np.median(gaps):.2f}s median")

    if au:
        I, peak, lra = loudness(a.mp4)
        print(f"  loudness: {I} LUFS integrated, peak {peak} dBFS, LRA {lra} LU")
        if I is None:
            warn.append("could not read loudness")
        elif abs(I - LUFS_TARGET) > LUFS_TOL:
            bad.append(f"{I} LUFS — target {LUFS_TARGET} +/-{LUFS_TOL}")
        else:
            clean.append(f"{I} LUFS")
        if peak is not None and peak > -0.5:
            bad.append(f"true peak {peak} dBFS — needs headroom under -1")
        elif peak is not None:
            clean.append(f"peak {peak} dBFS")

    # music under voice: the level in the gaps between lines is the bed alone, and the
    # level during a line is voice over bed. Research puts the bed 18-20 dB down.
    if a.build and au:
        cues = json.loads(re.search(r"var CUES=(\[.*?\]);",
                                    open(a.build, encoding="utf-8").read(), re.S).group(1))
        mono = "/tmp/qa-mix.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.mp4, "-ac", "1",
                        "-ar", "24000", mono], check=True)
        with wave.open(mono) as w:
            sr2 = w.getframerate()
            m = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        def rms(t0, t1):
            seg = m[int(t0 * sr2):int(t1 * sr2)]
            return 20 * np.log10(max(float(np.sqrt((seg ** 2).mean())), 1e-9)) if len(seg) else None
        sp = [rms(float(c[0]) + 0.1, float(c[1]) - 0.1) for c in cues]
        gp = [rms(float(x[1]) + 0.12, float(y[0]) - 0.12)
              for x, y in zip(cues, cues[1:]) if float(y[0]) - float(x[1]) > 0.35]
        sp = [x for x in sp if x is not None]
        gp = [x for x in gp if x is not None]
        if sp and gp:
            sep = float(np.median(sp) - np.median(gp))
            print(f"  bed: speech {np.median(sp):.1f} dBFS, gaps {np.median(gp):.1f} dBFS "
                  f"-> {sep:.1f} dB apart")
            if sep < 12:
                bad.append(f"music only {sep:.1f} dB under the voice — 18-20 is the target")
            elif sep < 16:
                warn.append(f"music {sep:.1f} dB under the voice — 18-20 is the target")
            else:
                clean.append(f"music {sep:.1f} dB under the voice")

    seam = np.abs(f[0].astype(int) - f[-1].astype(int)).mean()
    print(f"  loop seam: first vs last frame differ by {seam:.1f}/255")

    print()
    for x in bad:
        print(f"  [BLOCKER] {x}")
    for x in warn:
        print(f"  [warn]    {x}")
    for x in clean:
        print(f"  ok        {x}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
