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
    ap.add_argument("--vo", help="the narration wav")
    ap.add_argument("--music", help="the music bed, so the mix can be decomposed")
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
    # A card is a flat bright fill. Measured: the brass cards sit at mean luma 202-204
    # with spatial std 20-27, the ember one at 144/16, and ordinary frames at 22-33 with
    # std 32-57. Brightness alone missed the ember card, so both conditions are used.
    flat = f.reshape(len(f), -1).std(axis=1)
    card = (mean > 110) & (flat < 30)
    cards = [(s, e) for s, e in runs_of(card) if e - s > 0.10]
    # Whether a card plays over speech is decided by the cue times, not by energy: the
    # narration carries his own breaths in the gaps, and an energy test calls a breath
    # speech, which flagged every card in the reel as overrunning.
    lines = []
    if a.build:
        lines = [(float(c[0]), float(c[1])) for c in json.loads(
            re.search(r"var CUES=(\[.*?\]);", open(a.build, encoding="utf-8").read(),
                      re.S).group(1))]
    for s, e in cards:
        note = f"card {s:.2f}-{e:.2f}s ({(e-s)*fps:.0f} frames)"
        if e - s < 0.45:
            bad.append(note + " — too fast to read, reads as a glitch")
        clash = [(x, y) for x, y in lines if y > s + 0.03 and x < e - 0.03]
        if clash:
            bad.append(note + f" — plays over the line at {clash[0][0]:.2f}s")
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

    # Music under voice. Comparing the gaps to the speech is misleading when the bed is
    # ducked — the gaps are louder than the bed under the voice, so that comparison once
    # told me the bed was above the voice when it was 11 dB below it. With both stems in
    # hand the honest method is a least-squares fit of mix = a*voice + b*music per window,
    # which gives the ducking depth and the real separation.
    if a.vo and a.music and os.path.exists(a.vo) and os.path.exists(a.music) and au:
        mono = {}
        for tag, path in (("mix", a.mp4), ("vo", a.vo), ("mus", a.music)):
            dst = f"/tmp/qa-{tag}.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1",
                            "-ar", "24000", dst], check=True)
            with wave.open(dst) as w:
                mono[tag] = (np.frombuffer(w.readframes(w.getnframes()),
                                           dtype=np.int16).astype(np.float32) / 32768)
        sr2, win = 24000, int(0.25 * 24000)
        n = min(len(mono["mix"]), len(mono["vo"]), len(mono["mus"])) // win
        gains, vlev, mlev, speaking = [], [], [], []
        for i in range(n):
            sl = slice(i * win, (i + 1) * win)
            V, M, X = mono["vo"][sl], mono["mus"][sl], mono["mix"][sl]
            A = np.vstack([V, M]).T
            try:
                c, *_ = np.linalg.lstsq(A, X, rcond=None)
            except np.linalg.LinAlgError:
                continue
            vr = float(np.sqrt((V ** 2).mean()))
            gains.append((i * 0.25, float(c[0]), float(c[1]), vr))
        if gains:
            vr = np.array([g[3] for g in gains])
            talk = vr > np.percentile(vr, 60)
            mus_talk = np.median([g[2] for g, t in zip(gains, talk) if t])
            mus_gap = np.median([g[2] for g, t in zip(gains, talk) if not t])
            duck = 20 * np.log10(max(mus_gap, 1e-6) / max(mus_talk, 1e-6))
            # level of each part inside the mix while he is speaking
            v_in = 20 * np.log10(max(np.median([g[1] for g, t in zip(gains, talk) if t]), 1e-9)
                                 * max(float(np.sqrt((mono["vo"] ** 2).mean())), 1e-9))
            m_in = 20 * np.log10(max(mus_talk, 1e-9)
                                 * max(float(np.sqrt((mono["mus"] ** 2).mean())), 1e-9))
            sep = v_in - m_in
            print(f"  bed: ducking {duck:.1f} dB, and {sep:.1f} dB under the voice "
                  f"while he speaks")
            if sep < 14:
                bad.append(f"bed only {sep:.1f} dB under the voice — 18-20 is the target")
            elif sep > 26:
                warn.append(f"bed {sep:.1f} dB under the voice — inaudible, why have it")
            else:
                clean.append(f"bed {sep:.1f} dB under the voice, {duck:.1f} dB of ducking")

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
