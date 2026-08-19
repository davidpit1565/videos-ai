#!/usr/bin/env python3
"""Generate the channel's background bed.

No sample library and no licensing headache — the track is synthesised, so every
video gets a bed that fits its exact length and nothing ever gets copyright-claimed.

  python3 build_music.py <seconds> <out.wav> [--bpm 82] [--key 55.0]
"""
import sys, wave
import numpy as np

SR = 44100

def env(n, a, d, s, r, sus=0.7):
    """ADSR over n samples, times in seconds."""
    a, d, r = int(a*SR), int(d*SR), int(r*SR)
    s = max(0, n - a - d - r)
    return np.concatenate([
        np.linspace(0, 1, a, endpoint=False) ** 1.6,
        np.linspace(1, sus, d, endpoint=False),
        np.full(s, sus),
        np.linspace(sus, 0, r) ** 1.4,
    ])[:n]

def saw(f, n, detune=0.0):
    t = np.arange(n) / SR
    ph = 2*np.pi*f*(1+detune)*t
    # band-limited-ish: sum of a few harmonics, softer than a raw saw
    return sum(np.sin(ph*h)/h for h in (1, 2, 3, 4, 5)) / 2.28

def sine(f, n):
    return np.sin(2*np.pi*f*np.arange(n)/SR)

def tri(f, n):
    x = (np.arange(n)*f/SR) % 1.0
    return 2*np.abs(2*x - 1) - 1

def lowpass(x, cutoff, q=0.9):
    """One-pole cascade — gentle, no ringing, good enough for a pad."""
    a = np.exp(-2*np.pi*cutoff/SR)
    y = x.copy()
    for _ in range(2):
        out = np.empty_like(y); acc = 0.0
        for i in range(len(y)):
            acc = (1-a)*y[i] + a*acc
            out[i] = acc
        y = out
    return y * (1/(1-a*q) if a < 1 else 1) * 0.35

def lowpass_fast(x, cutoff):
    """FFT-domain soft rolloff — same idea as above, orders of magnitude faster."""
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1/SR)
    X *= 1.0 / (1.0 + (f/cutoff)**2)
    return np.fft.irfft(X, n)

def reverb(x, decay=1.5, mix=0.32):
    n = int(decay*SR)
    rng = np.random.default_rng(7)
    ir = rng.normal(0, 1, n) * np.exp(-np.linspace(0, 6, n))
    ir[0] = 1.0
    wet = np.convolve(x, ir, mode="full")[:len(x)]
    wet /= (np.abs(wet).max() or 1)
    return (1-mix)*x + mix*wet*(np.abs(x).max() or 1)

# semitone offsets for each chord voicing, over the key root
PROG = [
    ("Am7",  [0, 3, 7, 10]),
    ("Fmaj7",[-4, 0, 5, 9]),
    ("Cmaj7",[3, 7, 12, 14]),
    ("G",    [-2, 2, 7, 11]),
]

def build(total, bpm=82, root=55.0):
    beat = 60.0/bpm
    bar  = beat*4
    n_total = int(total*SR)
    pad  = np.zeros(n_total)
    bass = np.zeros(n_total)
    arp  = np.zeros(n_total)
    perc = np.zeros(n_total)

    n_bars = int(np.ceil(total/bar))
    for b in range(n_bars):
        name, ivs = PROG[b % len(PROG)]
        start = int(b*bar*SR)
        n = min(int(bar*SR*1.15), n_total-start)          # let chords ring over the bar
        if n <= 0: break

        # pad — four detuned voices an octave up
        e = env(n, 0.55, 0.35, 0, bar*0.55, sus=0.62)
        for k, iv in enumerate(ivs):
            f = root*2*(2**(iv/12))
            v = (saw(f, n, detune=0.0035*(k-1.5)) + saw(f, n, detune=-0.0028*(k-1.5)))*0.5
            pad[start:start+n] += v*e*(0.30 - 0.03*k)

        # sub — root, one octave down
        nb = min(int(bar*SR), n_total-start)
        bass[start:start+nb] += sine(root*(2**(ivs[0]/12)), nb)*env(nb, 0.02, 0.25, 0, bar*0.5, sus=0.5)*0.5

        # arpeggio — eighth notes, two octaves up, quiet
        for i in range(8):
            s2 = start + int(i*beat/2*SR)
            n2 = min(int(beat*0.75*SR), n_total-s2)
            if n2 <= 0: break
            f = root*4*(2**(ivs[[0,2,1,3,2,0,3,1][i]]/12))
            arp[s2:s2+n2] += tri(f, n2)*env(n2, 0.005, 0.10, 0, 0.28, sus=0.18)*0.16

        # pulse — soft kick on 1 and 3, breath of noise on the offbeats
        rng = np.random.default_rng(b)
        for i in (0, 2):
            s3 = start + int(i*beat*SR); n3 = min(int(0.16*SR), n_total-s3)
            if n3 <= 0: break
            f = np.linspace(95, 46, n3)
            perc[s3:s3+n3] += np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-np.linspace(0, 9, n3))*0.36
        for i in (1, 3):
            s3 = start + int(i*beat*SR); n3 = min(int(0.05*SR), n_total-s3)
            if n3 <= 0: break
            perc[s3:s3+n3] += rng.normal(0, 1, n3)*np.exp(-np.linspace(0, 12, n3))*0.05

    pad = lowpass_fast(pad, 2400)
    arp = lowpass_fast(arp, 7000)
    bass = lowpass_fast(bass, 160)
    mix = reverb(pad*0.80 + arp*1.9, decay=1.6, mix=0.30) + bass*0.62 + perc*0.5
    # gentle high shelf so it has air rather than sitting under a blanket
    mix = mix + lowpass_fast(mix, 220)*(-0.35) + (mix - lowpass_fast(mix, 4500))*0.55

    # slow swell so it never sits still, plus top and tail
    t = np.arange(n_total)/SR
    mix *= 0.86 + 0.14*np.sin(2*np.pi*t/19.0)
    fade = int(2.2*SR)
    mix[:fade]  *= np.linspace(0, 1, fade)**1.5
    mix[-fade:] *= np.linspace(1, 0, fade)**1.5

    mix /= (np.abs(mix).max() or 1)
    return (mix*0.82)

if __name__ == "__main__":
    total = float(sys.argv[1]); out = sys.argv[2]
    bpm  = float(sys.argv[sys.argv.index("--bpm")+1]) if "--bpm" in sys.argv else 82.0
    root = float(sys.argv[sys.argv.index("--key")+1]) if "--key" in sys.argv else 55.0
    a = build(total, bpm, root)
    with wave.open(out, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((a*32767).astype(np.int16).tobytes())
    print("wrote %s  %.1fs  %d bpm" % (out, len(a)/SR, bpm))
