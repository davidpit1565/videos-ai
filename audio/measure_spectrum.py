import sys, numpy as np, librosa, warnings
warnings.filterwarnings("ignore")

def stats(path):
    y, sr = librosa.load(path, sr=22050, mono=True)
    y = y / (np.abs(y).max() + 1e-9)
    # voiced frames only, so silence doesn't drag the spectrum down
    f0, vflag, _ = librosa.pyin(y, fmin=60, fmax=350, sr=sr, frame_length=1024)
    v = f0[~np.isnan(f0)]
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=256))
    frames_voiced = np.repeat(vflag, 1)[: S.shape[1]]
    Sv = S[:, frames_voiced[: S.shape[1]]] if frames_voiced.sum() > 5 else S
    freqs = librosa.fft_frequencies(sr=sr, n_fft=1024)
    def band(lo, hi):
        m = (freqs >= lo) & (freqs < hi)
        return 20 * np.log10(Sv[m].mean() + 1e-9)
    body = band(200, 600)
    cent = float((freqs[:, None] * Sv).sum() / (Sv.sum() + 1e-9))
    return {
        "dur": len(y) / sr,
        "f0_med": float(np.median(v)) if len(v) else float("nan"),
        "f0_iqr": float(np.percentile(v, 75) - np.percentile(v, 25)) if len(v) else float("nan"),
        "voiced%": float(100 * np.mean(vflag)),
        "centroid": cent,
        "presence": band(1500, 3500) - body,
        "clarity": band(3500, 7000) - body,
        "sband": band(6000, 9000) - body,
        "tilt": band(3000, 8000) - band(200, 1000),
    }

print(f"{'file':34}{'dur':>6}{'F0med':>7}{'F0iqr':>7}{'voiced%':>8}{'centroid':>9}{'pres':>7}{'clar':>7}{'S':>7}{'tilt':>7}")
for p in sys.argv[1:]:
    try:
        s = stats(p)
    except Exception as e:
        print(p, "ERR", e); continue
    n = p.split("/")[-1][:33]
    print(f"{n:34}{s['dur']:6.1f}{s['f0_med']:7.1f}{s['f0_iqr']:7.1f}{s['voiced%']:8.1f}"
          f"{s['centroid']:9.0f}{s['presence']:7.1f}{s['clarity']:7.1f}{s['sband']:7.1f}{s['tilt']:7.1f}")
