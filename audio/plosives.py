"""Word-initial stops, measured. Every check in this repo so far read word *endings*
— so T, D, K at the start of a word have never been measured at all, which is where
he keeps hearing the accent.

What separates English /t k p/ from Flemish and from Indian English is not the burst,
it is the silence after it. English aspirates: burst, then 40-80ms of breath, then the
vowel. Flemish and Indian English do not: the vowel starts almost on the burst. That
delay is Voice Onset Time and it is directly measurable.

  vot      burst -> first periodic frame, in ms (voiceless t/k/p)
  prevoice periodic frames *before* the burst, in ms (voiced d/g/b). English word-initial
           /d/ has almost none; Dutch has a lot, and it reads as a foreign D.
  asp      aspiration energy 2-8kHz between burst and vowel, relative to the vowel
  centroid spectral centre of the burst itself. A retroflex stop sits lower than an
           alveolar one, which is the other half of what "sounds Indian" means.
"""
import sys, json, argparse, numpy as np, wave

SR = 16000
HOP = 0.0025          # 2.5ms — VOT differences of interest are 20-40ms
WIN = 0.010

def load(p):
    import librosa
    y, _ = librosa.load(p, sr=SR, mono=True)
    return y / (np.abs(y).max() + 1e-9)

def frames(y, hop=HOP, win=WIN):
    h, w = int(hop * SR), int(win * SR)
    n = max(0, 1 + (len(y) - w) // h)
    return np.lib.stride_tricks.as_strided(
        y, (n, w), (y.strides[0] * h, y.strides[0])).copy(), h, w

def band_rms(F, lo, hi):
    S = np.abs(np.fft.rfft(F * np.hanning(F.shape[1]), axis=1))
    f = np.fft.rfftfreq(F.shape[1], 1 / SR)
    m = (f >= lo) & (f < hi)
    return 20 * np.log10(np.sqrt((S[:, m] ** 2).mean(1)) + 1e-9)

def periodic(y, hop=HOP, win=0.030):
    """Normalised autocorrelation peak in the 70-350Hz lag range. The window has to be
    long enough to hold the longest lag: a 10ms window cannot resolve a 100Hz male F0,
    and an earlier version of this returned zero for every frame because of it."""
    F, h, w = frames(y, hop, win)
    out = np.zeros(len(F))
    lo, hi = int(SR / 350), min(int(SR / 70), w - 1)
    for i, f in enumerate(F):
        f = f - f.mean()
        e = (f ** 2).sum()
        if e < 1e-8 or hi <= lo:
            continue
        a = np.correlate(f, f, "full")[len(f) - 1:]
        out[i] = a[lo:hi].max() / (e + 1e-12)
    return out

def centroid(y0):
    S = np.abs(np.fft.rfft(y0 * np.hanning(len(y0))))
    f = np.fft.rfftfreq(len(y0), 1 / SR)
    return float((f * S).sum() / (S.sum() + 1e-9))

VOICELESS = {"t": "t", "k": "k", "p": "p", "c": "k", "q": "k"}
VOICED = {"d": "d", "g": "g", "b": "b"}

def initial_stop(raw):
    """The letter is not the sound. "chat" is not a /k/, "the" is not a /t/, "phone"
    is not a /p/, and "GPT" is three letter-names. Getting this wrong is how a first
    pass measured 117 words and reported nothing."""
    if len(raw) > 1 and raw.upper() == raw and raw.isalpha():
        return None                                   # GPT, AI — spelled out
    c = raw[0]
    nxt = raw[1] if len(raw) > 1 else ""
    if nxt == "h" and c in "tcpsg":                   # the, chat, phone, ship, ghost
        return None
    if c == "c" and nxt in "eiy":                     # ceiling
        return None
    if c == "g" and nxt in "ei":                      # gentle
        return None
    if c in "kpg" and nxt == "n":                     # knee, pneumatic, gnaw
        return None
    if c == "t" and nxt == "s":
        return None
    return VOICELESS.get(c) or VOICED.get(c)

def measure(y, at, dur, ph=None):
    """one word. returns dict or None if the burst cannot be located."""
    a = max(0, int((at - 0.100) * SR))
    b = min(len(y), int((at + min(dur, 0.28)) * SR))
    seg = y[a:b]
    if len(seg) < int(0.08 * SR):
        return None
    F, h, w = frames(seg)
    if len(F) < 12:
        return None
    # 1kHz up, deliberately: a 500Hz-up band still carries the first formant, so the
    # vowel onset itself trips the "energy rose" test and the burst is placed there.
    # That is what produced /t/ readings of 0ms with a 630Hz burst centre — not an
    # unaspirated stop, a misdetection.
    hi = band_rms(F, 1000, 8000)
    per = periodic(seg)
    lowe = band_rms(F, 80, 1000)
    hie = band_rms(F, 2000, 8000)
    # A vowel puts most of its energy below 1kHz; aspiration is the opposite. This
    # ratio separates the two at 2.5ms resolution, which autocorrelation cannot do
    # at a male F0.
    ratio = lowe - hie

    # What defines a stop is the silence, not the noise: the vocal tract is sealed,
    # energy collapses, then it is released. So anchor on the closure and take the
    # burst as the release out of it. Looking for "the loudest rise" instead found
    # vowel onsets and neighbouring syllables, and measured his Flemish /k/ at 143ms
    # — impossible for an unaspirated stop, which is how that version was caught.
    lim = min(len(hi) - 6, int(0.200 / HOP))
    if lim < 6:
        return None
    ci = int(np.argmin(hi[:lim]))
    rest = hi[ci:lim + 4]
    up = np.where(rest > hi[ci] + 6.0)[0]
    if not len(up):
        return None
    bi = ci + int(up[0])
    if bi >= len(hi) - 4:
        return None

    # Voicing onset: two consecutive periodic frames after the burst. Aspiration is
    # aperiodic by definition, so periodicity alone marks where the vowel starts. An
    # earlier version also required the low band to exceed the loudest pre-burst frame,
    # which in connected speech is the previous word's vowel — it never fired.
    # the threshold is taken from this word: halfway between the closure and the
    # word's own vowel, so it does not depend on level or on the speaker
    clo = float(np.median(ratio[max(0, ci - 2):bi])) if bi > ci else float(ratio[ci])
    vow_ref = float(np.percentile(ratio[bi:], 85))
    if vow_ref - clo < 4:
        return None
    thr = clo + 0.5 * (vow_ref - clo)
    vi = None
    for i in range(bi, len(ratio) - 1):
        if ratio[i] > thr and ratio[i + 1] > thr:
            vi = i
            break
    if vi is None:
        return None

    # prevoicing: periodic frames immediately before the burst (during the closure)
    pv = 0
    for i in range(bi - 1, 0, -1):
        if i < len(per) and per[i] > 0.45:
            pv += 1
        else:
            break

    asp = float(band_rms(F[bi:vi] if vi > bi else F[bi:bi + 1], 2000, 8000).mean())
    vow = float(band_rms(F[vi:min(len(F), vi + 12)], 2000, 8000).mean())
    c0 = a + bi * h
    cen = centroid(y[c0:c0 + int(0.020 * SR)])
    # Where a release sits in frequency is set by where the tract was sealed: lips
    # low and diffuse, alveolar ridge high, velum in between. A "burst" outside its
    # own phoneme's range is not a quiet consonant, it is the wrong event, and must
    # be dropped rather than reported as an accent.
    OK = {"p": (250, 2600), "t": (1800, 8000), "k": (900, 4200)}
    lo_hi = OK.get(ph)
    if lo_hi and not (lo_hi[0] <= cen <= lo_hi[1]):
        return None
    return dict(vot=(vi - bi) * HOP * 1000,
                prevoice=pv * HOP * 1000,
                asp=round(asp - vow, 1),
                centroid=round(cen, 0))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--words", required=True, help="deep json with word timestamps")
    ap.add_argument("--label", default="")
    ap.add_argument("--json", default="")
    ap.add_argument("--vot-floor", type=float, default=40.0,
                    help="ms. English word-initial /t k p/ below this reads unaspirated")
    a = ap.parse_args()

    y = load(a.wav)
    words = json.load(open(a.words))["words"]
    rows = []
    for w in words:
        raw = w["word"].strip().strip(".,!?—-").lower()
        if not raw:
            continue
        ph = initial_stop(raw)
        if not ph:
            continue
        m = measure(y, float(w["at"]), float(w["dur"]), ph)
        if m:
            m.update(word=w["word"], ph=ph, at=round(float(w["at"]), 2),
                     voiced=raw[0] in VOICED)
            rows.append(m)

    name = a.label or a.wav.split("/")[-1]
    print(f"{name}  {len(rows)} word-initial stops measured")
    vl = [r for r in rows if not r["voiced"]]
    vd = [r for r in rows if r["voiced"]]
    if vl:
        v = np.array([r["vot"] for r in vl])
        print(f"  voiceless t/k/p  n={len(vl)}  VOT median {np.median(v):.0f}ms  "
              f"range {v.min():.0f}-{v.max():.0f}ms")
        for ph in "tkp":
            s = [r["vot"] for r in vl if r["ph"] == ph]
            if s:
                print(f"    /{ph}/  n={len(s):2d}  median {np.median(s):3.0f}ms")
    if vd:
        p = np.array([r["prevoice"] for r in vd])
        print(f"  voiced d/g/b     n={len(vd)}  prevoicing median {np.median(p):.0f}ms")

    bad = sorted([r for r in vl if r["vot"] < a.vot_floor], key=lambda r: r["vot"])
    if bad:
        print(f"  under the {a.vot_floor:.0f}ms floor — these are the ones that read "
              f"unaspirated:")
        for r in bad:
            print(f"    {r['at']:6.2f}s  /{r['ph']}/  {r['vot']:3.0f}ms  "
                  f"asp {r['asp']:+5.1f}dB  burst {r['centroid']:.0f}Hz  {r['word']}")
    else:
        print(f"  every voiceless stop clears the {a.vot_floor:.0f}ms floor")
    if a.json:
        json.dump(rows, open(a.json, "w"), indent=1)

if __name__ == "__main__":
    main()
