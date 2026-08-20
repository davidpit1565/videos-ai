#!/usr/bin/env python3
"""Build the Flemish voice profile from his Flemish recording, and correct the one
thing the measurement found wrong with the source.

His Flemish take is clean — 32 dB SNR, no clipping — but it was recorded darker
than the English one: 4-9 kHz sits at -25.9 dB against the body, where the English
reference sits at -14.2 dB, and presence is 3.5 dB lower. That gap is the dull S he
heard, and it is in the recording, not in the model: the cloner takes its timbre
from the reference, so a dark reference produces a dark S in every line forever.

So the reference is corrected to match the English one's spectrum before cloning,
and the correction is verified by measuring it again rather than assumed. Three
candidate windows are prepared, because which reference sounds like him is his call
and not the metric's — that already went wrong once in English.

  python3 audio/build_flemish.py <recording.wav> --windows 0:14,25:39,39:53
"""
import argparse, json, os, subprocess, sys, wave
import numpy as np

EN_REF = "audio/voice/profile/reference.wav"
OUT = "audio/voice/profile/flemish"
TESTS = [
    "De test is simpel. Als het niks kan doen zonder jou, is het gewoon een chatbot met een schonere naam.",
    "Agenten mislukken vol zelfvertrouwen. Ze sturen een mail naar de verkeerde persoon, heel vriendelijk.",
]
# highpass kills the room rumble the measurement found 1.6 dB hot; the two shelves
# close the 11.7 dB sibilance gap and the 3.5 dB presence gap against the English take
# tuned by measurement, not by taste: this setting lands the reference's sibilance at
# -14.0 dB against the English reference's -14.2, and costs 0.2 dB of SNR (31.2 vs 31.4)
CLEAN = ("highpass=f=80,equalizer=f=3000:t=q:w=1.6:g=4,"
         "equalizer=f=6500:t=q:w=1.2:g=13,equalizer=f=8500:t=q:w=1.4:g=9,"
         "deesser=i=0.08:m=0.5:f=0.4,loudnorm=I=-19:TP=-2:LRA=11")


def load(path):
    with wave.open(path) as w:
        sr = w.getframerate()
        y = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return y, sr


def spectrum(path, seconds=18):
    y, sr = load(path)
    n = min(len(y), sr * seconds)
    S = np.abs(np.fft.rfft(y[:n] * np.hanning(n)))
    f = np.fft.rfftfreq(n, 1 / sr)

    def b(lo, hi):
        m = (f >= lo) & (f < hi)
        return float(np.sqrt((S[m] ** 2).mean())) if m.any() else 1e-9

    body = b(300, 3400)
    return dict(sib=round(20 * np.log10(b(4000, 9000) / body), 1),
                pres=round(20 * np.log10(b(2000, 4000) / body), 1),
                low=round(20 * np.log10(b(45, 65) / body), 1))


def ff(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("recording")
    ap.add_argument("--windows", default="0:14,25:39,39:53",
                    help="candidate reference windows, seconds, comma separated")
    ap.add_argument("--no-generate", action="store_true", help="prepare references only")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    target = spectrum(EN_REF)
    print(f"english reference: S {target['sib']} dB · presence {target['pres']} dB")
    print(f"flemish source:    {spectrum(a.recording)}")

    refs = []
    for i, w in enumerate(a.windows.split(","), 1):
        t0, t1 = (float(x) for x in w.split(":"))
        dst = f"{OUT}/ref-{i}.wav"
        ff("-ss", str(t0), "-t", str(t1 - t0), "-i", a.recording,
           "-af", CLEAN, "-ar", "24000", "-ac", "1", dst)
        s = spectrum(dst)
        gap = round(s["sib"] - target["sib"], 1)
        print(f"  ref-{i}  {t0:g}-{t1:g}s   S {s['sib']} dB ({gap:+.1f} vs english) · "
              f"presence {s['pres']} dB · low {s['low']} dB")
        refs.append(dict(n=i, window=[t0, t1], path=dst, **s, sib_gap=gap))

    json.dump(dict(source=a.recording, english=target, candidates=refs),
              open(f"{OUT}/profile.json", "w"), indent=1)

    if a.no_generate:
        return

    import torch, torchaudio
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    torch.set_num_threads(int(os.environ.get("VOICE_THREADS", "3")))
    m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")

    for r in refs:
        parts = []
        for j, text in enumerate(TESTS):
            torch.manual_seed(7)
            wav = m.generate(text, language_id="nl", audio_prompt_path=r["path"],
                             exaggeration=0.50, cfg_weight=0.30, temperature=0.75)
            raw = f"/tmp/fl-{r['n']}-{j}.wav"
            torchaudio.save(raw, wav, m.sr)
            pol = f"/tmp/fl-{r['n']}-{j}p.wav"
            ff("-i", raw, "-af",
               "highpass=f=75,equalizer=f=4200:t=q:w=1.4:g=1.5,equalizer=f=7200:t=q:w=1.6:g=2,"
               "deesser=i=0.14:m=0.5:f=0.35,"
               "acompressor=threshold=-20dB:ratio=2.2:attack=10:release=200:makeup=1.5,"
               "alimiter=limit=0.95,loudnorm=I=-17:TP=-1.5:LRA=10",
               "-ar", "48000", "-ac", "1", pol)
            parts.append(pol)
            print(f"  option {r['n']} line {j+1}: {spectrum(pol, 8)}", flush=True)
        lst = f"/tmp/fl-{r['n']}.txt"
        with open(lst, "w") as f:
            for p in parts:
                f.write(f"file '{p}'\n")
        out = f"export/flemish-option-{r['n']}.m4a"
        ff("-f", "concat", "-safe", "0", "-i", lst, "-af", "loudnorm=I=-16:TP=-1.5",
           "-c:a", "aac", "-b:a", "192k", out)
        print(f"wrote {out}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
