"""Did that consonant arrive as a burst or as frication?

Written because th_check could not answer it. That tool anchors on "the 20ms before the word
is quiet", which is true at the start of an utterance and false after the voiced /n/ of "in".
Tested against a set where the answer was known — Chatterbox's own voice, whose phonetics are
not in doubt, saying the same sentence with different words in the slot — it called a certain
/th/ "unmeasured" every time, and before that it called "Two" and "Tea" fricatives. Two
retractions from one blind spot.

This anchors on the vowel, which is present in every case:

  1. the loudest low-band frame in the window is the vowel
  2. voicing onset is the last frame before it still sitting 10dB below it
  3. the high band in the 80ms before that onset is compared to the high band *of the same
     word's vowel* — a ratio inside one word, so nothing depends on what came before it

`peak` is that ratio at its maximum. A stop releases one sharp burst far above the vowel;
frication is gentler noise closer to it.

SCOPE: one contrast — /th/ against /t/ before a vowel. Not a general fricative detector.

Calibrated on the known set, three seeds per word, same frame ("It finds the risk in _
seconds"):

    three   +5.4  +9.9 +11.5       /th/            in scope
    two    +18.2 +20.8 +29.4       /t/ + vowel     in scope
    tea    +19.2 +21.9 +27.4       /t/ + vowel     in scope

    tree    +4.1  +6.2             /tr/            groups with /th/
    free    +0.8  +3.9  +5.5       /f/             falls below the band
    sea     +7.0 +16.6             /s/             spans both sides

In scope the separation is clean and wide: frication tops out at 11.5, bursts start at 18.2,
and BAND sits inside the first with the threshold in the empty middle.

The last three rows are why the scope is stated rather than assumed. A first version of this
file claimed a clean split on a partial view of the set; when the rest finished generating,
`free` and `sea` broke it, and the rule test named them. They are kept as evidence of the
limits, and they are physical rather than surprising: /f/ is a weak labiodental with little
3-8kHz energy, and /s/ is a strong sibilant that can exceed its own vowel as far as a stop
burst does. Point this at a sibilant and it will call it a burst.

Note what `tree` did. It grouped with `three`, and Whisper transcribed it as "3". So the
distinction the ear is actually reacting to is not /th/ against /t/ — it is frication against
a hard burst before a vowel, which is what "a misplaced T" sounds like.

Sixteen rows. Enough to separate two groups that do not overlap in scope, not enough to trust
a reading that lands in the gap between them — so BAND is narrower than the gap on purpose.
"""
import numpy as np

SR, HOP, WIN = 16000, 0.0025, 0.010
# inside the frication group, clear of both edges of the gap
BAND = (4.0, 13.0)
# the words this is calibrated for; anything else needs its own ground-truth rows first
IN_SCOPE = ("three",)


def _frames(y):
    h, w = int(HOP * SR), int(WIN * SR)
    n = max(0, 1 + (len(y) - w) // h)
    return np.lib.stride_tricks.as_strided(
        y, (n, w), (y.strides[0] * h, y.strides[0])).copy()


def _band(F, lo, hi):
    S = np.abs(np.fft.rfft(F * np.hanning(F.shape[1]), axis=1))
    f = np.fft.rfftfreq(F.shape[1], 1 / SR)
    m = (f >= lo) & (f < hi)
    return 20 * np.log10(np.sqrt((S[:, m] ** 2).mean(1)) + 1e-9)


def load(p):
    import librosa
    y, _ = librosa.load(p, sr=SR, mono=True)
    return y / (np.abs(y).max() + 1e-9)


def measure(y, at, dur):
    """peak: high band before voicing, relative to the word's own vowel, in dB."""
    a = max(0, int((at - 0.08) * SR))
    b = min(len(y), int((at + min(dur, 0.30)) * SR))
    F = _frames(y[a:b])
    if len(F) < 20:
        return None
    lo, hi = _band(F, 80, 900), _band(F, 3000, 8000)

    vpk = int(np.argmax(lo))
    if vpk < 4:
        return None
    vi = vpk
    while vi > 1 and lo[vi - 1] > lo[vpk] - 10:
        vi -= 1
    hv = float(hi[vpk:min(len(hi), vpk + 12)].mean())

    pre = hi[max(0, vi - int(0.08 / HOP)):vi]
    if len(pre) < 3:
        return None
    return dict(peak=round(float(pre.max() - hv), 1),
                rise=round(float(np.max(np.diff(pre))), 1) if len(pre) > 2 else 99.0)


def verdict(r):
    """in-band, or the side it fell out on — never a bare boolean, because which side it
    missed by is what says whether to reroll or to stop trying."""
    if r is None:
        return "unmeasurable"
    if r["peak"] > BAND[1]:
        return "burst"
    if r["peak"] < BAND[0]:
        return "absent"
    return "frication"


def find(words, target):
    """the target word's timing, matched loosely — the transcriber writes "three" as "3"
    and "tree" as "3" too, so a caller that needs certainty must know it by position"""
    t = target.lower()
    alias = {"three": ("three", "3"), "four": ("four", "4"), "five": ("five", "5")}
    ok = alias.get(t, (t,))
    for w in words:
        if "".join(c for c in w["word"].lower() if c.isalnum()) in ok:
            return w
    return None
