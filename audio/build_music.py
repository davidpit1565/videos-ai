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

def pluck(f, n, damping=0.5, decay=0.996, brightness=0.6, seed=0):
    """Karplus-Strong plucked string — a period-length noise/tone burst run through a
    feedback delay line one cycle long, each pass averaged with the sample one cycle
    behind it. That averaging is what a real plucked string does physically (high
    harmonics die fastest); it's the actual mechanism, not a sample of one. `damping`
    near 1 keeps more of the delayed signal (a longer, warmer ring — guitar);
    nearer 0.5 blends in more of the fresh burst (a shorter, brighter strike — piano).
    `decay` is separate: overall energy lost per cycle, independent of tone."""
    period = max(2, int(round(SR / f)))
    rng = np.random.default_rng(seed)
    buf = rng.uniform(-1, 1, period)*brightness + sine(f, period)*(1 - brightness)
    out = np.empty(n)
    for i in range(n):
        j = i % period
        val = buf[j]
        out[i] = val
        nxt = buf[(j + 1) % period]
        buf[j] = (damping*val + (1 - damping)*nxt) * decay
    return out

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

# semitone offsets for each chord voicing, over the key root. Different progressions
# read as genuinely different tracks, not just the same one sped up or slowed down —
# tempo alone was the mistake: every episode sounded identical because only bpm moved.
# Each mood is a chord progression plus a style: which of the four voices play, what
# shape they take. Chord progression alone stopped being enough once "completely
# different, not just a mood swing" was the ask — two tracks that both run
# pad+arp+kick only ever read as the same track retuned. STYLE changes which voices
# exist and how, so a genuinely different one has to sound built differently, not
# just moved to a different key.
DEFAULT_STYLE = dict(arp=True, perc="kick", wave="saw", swell=19.0, decay=1.6, mix=0.30, chord_hold=1.0,
                pluck_damping=0.5, pluck_decay=0.996, pluck_brightness=0.6)

MOODS = {
    # the default — even, unresolved, works for most explainer content
    "neutral": dict(prog=[("Am7", [0, 3, 7, 10]), ("Fmaj7", [-4, 0, 5, 9]),
                ("Cmaj7", [3, 7, 12, 14]), ("G", [-2, 2, 7, 11])]),
    # minor, restless, never lands on the root — for exposes and warnings
    "urgent":  dict(prog=[("Am", [0, 3, 7, 12]), ("E7", [-1, 4, 7, 10]),
                ("Fmaj7", [-4, 0, 5, 9]), ("Am", [0, 3, 7, 12])]),
    # major, resolves every four bars — for wins, fixes, things that work
    "bright":  dict(prog=[("Cmaj7", [0, 4, 7, 11]), ("G", [-5, -2, 2, 7]),
                ("Am7", [0, 3, 7, 10]), ("Fmaj7", [-4, 0, 5, 9])]),
    # minor but a different shape from "urgent" — a longer eight-chord cycle so it
    # doesn't read as the same track transposed. For a slow-build reveal or a warning
    # that escalates rather than one that's urgent from the first bar.
    "tense":   dict(prog=[("Dm7", [0, 3, 7, 10]), ("Bbmaj7", [-3, 1, 6, 10]),
                ("Gm7", [-5, -2, 2, 5]), ("A7", [-3, 4, 7, 9]),
                ("Dm7", [0, 3, 7, 10]), ("F", [-9, -5, -2, 3]),
                ("Gm7", [-5, -2, 2, 5]), ("A7", [-3, 4, 7, 9])]),
    # major and forward-moving, faster harmonic rhythm than "bright" — for a fix that
    # unfolds in real time rather than a single win landed on.
    "drive":   dict(prog=[("G", [0, 4, 7, 11]), ("D", [-5, -1, 2, 6]),
                ("Em7", [-8, -3, 0, 4]), ("C", [-7, -3, 0, 5])]),

    # ---- round 2: same instrument set, deliberately different builds of it ----

    # almost nothing playing — sub bass and a slow sine chime, huge silence between
    # notes. For a minimalist reveal or a single-fact explainer that needs no bed
    # fighting for attention under it.
    "sparse":     dict(prog=[("Am7", [0, 3, 7, 10]), ("Fmaj7", [-4, 0, 5, 9])],
                arp=False, perc="none", wave="sine", swell=28.0, decay=2.4, mix=0.20, chord_hold=2.0),
    # short plucky triangle notes instead of a held pad, swung eighth-note arp out
    # front instead of buried — bouncy, major, for lighthearted or beginner content.
    "playful":    dict(prog=[("Cmaj7", [0, 4, 7, 11]), ("Fmaj7", [-4, 0, 5, 9]),
                ("G", [-2, 2, 7, 11]), ("Am7", [0, 3, 7, 10])],
                arp=True, perc="shaker", wave="tri", swell=8.0, decay=0.7, mix=0.16, chord_hold=0.5),
    # clean, steady, no arpeggio and barely-there percussion — safe and unobtrusive.
    # For the "sell this to a business" content: confident, not moody.
    "corporate":  dict(prog=[("Cmaj7", [0, 4, 7, 11]), ("Am7", [0, 3, 7, 10]),
                ("Dm7", [-7, -3, 0, 3]), ("G", [-2, 2, 7, 11])],
                arp=False, perc="soft", wave="saw", swell=23.0, decay=1.2, mix=0.24, chord_hold=1.0),
    # irregular, dissonant, no fixed chord hold — a workflow visibly misbehaving.
    # For an agent-failure cold open, never for a whole episode.
    "glitch":     dict(prog=[("Am", [0, 1, 6, 7]), ("E7", [-1, 0, 6, 10]),
                ("Fmaj7", [-4, -3, 5, 6]), ("Am", [0, 1, 6, 7])],
                arp=True, perc="clockwork", wave="tri", swell=3.0, decay=0.4, mix=0.34, chord_hold=0.5),
    # one chord per two bars, huge slow pad swell, no percussion at all — a big
    # reveal or a stakes-setting cold open, not a whole 45s explainer.
    "cinematic":  dict(prog=[("Am7", [0, 3, 7, 10]), ("Fmaj7", [-4, 0, 5, 9]),
                ("Cmaj7", [3, 7, 12, 14]), ("E7", [-1, 4, 7, 10])],
                arp=False, perc="none", wave="saw", swell=34.0, decay=2.8, mix=0.34, chord_hold=2.0),
    # warm and filtered, slow swung arp, soft — a wind-down or a calmer explainer
    # that doesn't need the room the default "neutral" bed takes up.
    "lofi":       dict(prog=[("Dm7", [0, 3, 7, 10]), ("Gm7", [-5, -2, 2, 5]),
                ("Cmaj7", [3, 7, 12, 14]), ("Fmaj7", [-4, 0, 5, 9])],
                arp=True, perc="soft", wave="tri", swell=14.0, decay=2.0, mix=0.40, chord_hold=1.3),
    # fast triangle-wave sixteenth arpeggio, bright, no pad swell to speak of — the
    # channel's own nostalgia setting, for a "remember when" or a tools-through-time bit.
    "retro":      dict(prog=[("Cmaj7", [0, 4, 7, 11]), ("Am7", [0, 3, 7, 10]),
                ("Fmaj7", [-4, 0, 5, 9]), ("G", [-2, 2, 7, 11])],
                arp=True, perc="kick", wave="tri", swell=6.0, decay=0.5, mix=0.16, chord_hold=0.5),
    # sparse minor-second dissonance, tremolo swell far faster than any other mood —
    # a slow-build dread rather than "tense"'s escalating warning. Use sparingly.
    "suspense":   dict(prog=[("Am", [0, 1, 7, 12]), ("Bdim", [-1, 2, 6, 11])],
                arp=False, perc="none", wave="sine", swell=4.0, decay=3.2, mix=0.30, chord_hold=2.0),
    # full pad, arp, and a kick on every beat instead of two — the only mood that
    # resolves AND hits hard. For a genuine "it works, and here's the proof" close.
    "triumphant": dict(prog=[("Cmaj7", [0, 4, 7, 11]), ("Fmaj7", [-4, 0, 5, 9]),
                ("G", [-2, 2, 7, 11]), ("Cmaj7", [0, 4, 7, 11])],
                arp=True, perc="every-beat", wave="saw", swell=10.0, decay=1.4, mix=0.30, chord_hold=1.0),
    # steady mechanical sixteenth-note pulse, no swell, no rubato — for automation
    # and workflow content where the point is that the machine doesn't waver.
    "clockwork":  dict(prog=[("Am7", [0, 3, 7, 10]), ("Dm7", [-7, -3, 0, 3]),
                ("Fmaj7", [-4, 0, 5, 9]), ("G", [-2, 2, 7, 11])],
                arp=True, perc="clockwork", wave="tri", swell=999.0, decay=1.0, mix=0.22, chord_hold=1.0),

    # ---- round 3: plucked-string synthesis (Karplus-Strong), not a sample library ----

    # bright, fast decay, no pad swell — the pad chord is struck once per bar and
    # left to die away rather than held, so it reads as a piano's hammer-strike
    # rather than a synth pad wearing a piano's name. For a calm walkthrough or a
    # skills explainer that wants warmth without the room a full pad bed takes.
    "piano":      dict(prog=[("Cmaj7", [0, 4, 7, 11]), ("Am7", [0, 3, 7, 10]),
                ("Fmaj7", [-4, 0, 5, 9]), ("G", [-2, 2, 7, 11])],
                arp=False, perc="soft", wave="pluck", swell=999.0, decay=1.1, mix=0.20, chord_hold=1.3,
                pluck_damping=0.42, pluck_decay=0.9935, pluck_brightness=0.75),
    # warmer and longer-ringing than "piano" — more of the delayed signal kept each
    # cycle (higher damping), less overall energy lost per cycle, so a chord rings
    # into the next one instead of striking and dying. For a personal or
    # behind-the-scenes bit, or anything that wants an organic rather than digital feel.
    "guitar":     dict(prog=[("G", [0, 4, 7, 11]), ("Em7", [-8, -3, 0, 4]),
                ("Cmaj7", [-9, -5, 0, 4]), ("D", [-5, -1, 2, 6])],
                arp=True, perc="none", wave="pluck", swell=12.0, decay=1.8, mix=0.28, chord_hold=1.0,
                pluck_damping=0.62, pluck_decay=0.9975, pluck_brightness=0.45),
}
for _name, _cfg in MOODS.items():
    for _k, _v in DEFAULT_STYLE.items():
        _cfg.setdefault(_k, _v)
STYLE = MOODS["neutral"]

def build(total, bpm=82, root=55.0, mood="neutral"):
    global STYLE
    STYLE = MOODS.get(mood, MOODS["neutral"])
    PROG = STYLE["prog"]
    beat = 60.0/bpm
    bar  = beat*4 * STYLE["chord_hold"]
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

        voice = {
            "saw": saw, "tri": lambda f, n: tri(f, n), "sine": lambda f, n: sine(f, n),
            "pluck": lambda f, n: pluck(f, n, damping=STYLE["pluck_damping"],
                        decay=STYLE["pluck_decay"], brightness=STYLE["pluck_brightness"]),
        }[STYLE["wave"]]

        # pad — four detuned voices an octave up (skipped entirely for a style built
        # without one, e.g. "glitch", which has no sustained voice at all)
        e = env(n, 0.55, 0.35, 0, bar*0.55, sus=0.62)
        for k, iv in enumerate(ivs):
            f = root*2*(2**(iv/12))
            if STYLE["wave"] == "saw":
                v = (saw(f, n, detune=0.0035*(k-1.5)) + saw(f, n, detune=-0.0028*(k-1.5)))*0.5
            else:
                v = voice(f, n)
            pad[start:start+n] += v*e*(0.30 - 0.03*k)

        # sub — root, one octave down
        nb = min(int(bar*SR), n_total-start)
        bass[start:start+nb] += sine(root*(2**(ivs[0]/12)), nb)*env(nb, 0.02, 0.25, 0, bar*0.5, sus=0.5)*0.5

        # arpeggio — eighth notes, two octaves up, quiet. Off entirely for styles
        # built without one ("sparse", "corporate", "cinematic", "suspense").
        if STYLE["arp"]:
            for i in range(8):
                s2 = start + int(i*beat/2*SR)
                n2 = min(int(beat*0.75*SR), n_total-s2)
                if n2 <= 0: break
                f = root*4*(2**(ivs[[0,2,1,3,2,0,3,1][i]]/12))
                arp[s2:s2+n2] += tri(f, n2)*env(n2, 0.005, 0.10, 0, 0.28, sus=0.18)*0.16

        # percussion — the one voice that most defines a style's identity: a plain
        # kick-on-1-and-3, a soft/near-absent pulse, a shaker's noise-only hits, a
        # kick on every beat for something that should hit harder, or a mechanical
        # sixteenth-note pulse with no swing at all.
        rng = np.random.default_rng(b)
        style_perc = STYLE["perc"]
        if style_perc == "kick":
            for i in (0, 2):
                s3 = start + int(i*beat*SR); n3 = min(int(0.16*SR), n_total-s3)
                if n3 <= 0: break
                f = np.linspace(95, 46, n3)
                perc[s3:s3+n3] += np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-np.linspace(0, 9, n3))*0.36
            for i in (1, 3):
                s3 = start + int(i*beat*SR); n3 = min(int(0.05*SR), n_total-s3)
                if n3 <= 0: break
                perc[s3:s3+n3] += rng.normal(0, 1, n3)*np.exp(-np.linspace(0, 12, n3))*0.05
        elif style_perc == "every-beat":
            for i in range(4):
                s3 = start + int(i*beat*SR); n3 = min(int(0.16*SR), n_total-s3)
                if n3 <= 0: break
                f = np.linspace(105, 48, n3)
                perc[s3:s3+n3] += np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-np.linspace(0, 8, n3))*0.42
        elif style_perc == "soft":
            for i in (0, 2):
                s3 = start + int(i*beat*SR); n3 = min(int(0.20*SR), n_total-s3)
                if n3 <= 0: break
                f = np.linspace(80, 44, n3)
                perc[s3:s3+n3] += np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-np.linspace(0, 11, n3))*0.18
        elif style_perc == "shaker":
            for i in range(4):
                s3 = start + int(i*beat*SR); n3 = min(int(0.06*SR), n_total-s3)
                if n3 <= 0: break
                perc[s3:s3+n3] += rng.normal(0, 1, n3)*np.exp(-np.linspace(0, 10, n3))*0.10
        elif style_perc == "clockwork":
            for i in range(16):
                s3 = start + int(i*beat/4*SR); n3 = min(int(0.035*SR), n_total-s3)
                if n3 <= 0: break
                amp = 0.20 if i % 4 == 0 else 0.07
                perc[s3:s3+n3] += rng.normal(0, 1, n3)*np.exp(-np.linspace(0, 20, n3))*amp
        # style_perc == "none": no percussion voice at all

    pad = lowpass_fast(pad, 2400)
    arp = lowpass_fast(arp, 7000)
    bass = lowpass_fast(bass, 160)
    mix = reverb(pad*0.80 + arp*1.9, decay=STYLE["decay"], mix=STYLE["mix"]) + bass*0.62 + perc*0.5
    # gentle high shelf so it has air rather than sitting under a blanket
    mix = mix + lowpass_fast(mix, 220)*(-0.35) + (mix - lowpass_fast(mix, 4500))*0.55

    # slow swell so it never sits still, plus top and tail — "clockwork" sets swell
    # to a period far longer than any real clip so it reads as flat and unwavering.
    t = np.arange(n_total)/SR
    mix *= 0.86 + 0.14*np.sin(2*np.pi*t/STYLE["swell"])
    fade = int(2.2*SR)
    mix[:fade]  *= np.linspace(0, 1, fade)**1.5
    mix[-fade:] *= np.linspace(1, 0, fade)**1.5

    mix /= (np.abs(mix).max() or 1)
    return (mix*0.82)

if __name__ == "__main__":
    total = float(sys.argv[1]); out = sys.argv[2]
    bpm  = float(sys.argv[sys.argv.index("--bpm")+1]) if "--bpm" in sys.argv else 82.0
    root = float(sys.argv[sys.argv.index("--key")+1]) if "--key" in sys.argv else 55.0
    mood = sys.argv[sys.argv.index("--mood")+1] if "--mood" in sys.argv else "neutral"
    a = build(total, bpm, root, mood)
    with wave.open(out, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((a*32767).astype(np.int16).tobytes())
    print("wrote %s  %.1fs  %d bpm  %s" % (out, len(a)/SR, bpm, mood))
