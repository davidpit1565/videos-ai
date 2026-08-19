"""Fix one stubborn line.

Whisper can only tell you whether a word is intelligible — it hears "harder" correctly
even when a person hears the wrong accent. So for a line he flags, generate several real
candidates (different seeds, different respellings, an optional rewrite that avoids the
word entirely), label them out loud, and let his ear pick. The winning seed and respelling
are stored per line, so every future render reproduces exactly what he approved.

    python3 audio/line_doctor.py --line "It makes ChatGPT think harder, not be right more often." \
        --respell "harderr,harder,har-der" --n 5 --out export/line-harder.m4a
"""
import argparse, json, os, subprocess, tempfile, warnings
warnings.filterwarnings("ignore")

REF = "audio/voice/profile/reference.wav"
CHOICES = "audio/voice/profile/line-choices.json"
POLISH = ("highpass=f=75,equalizer=f=240:t=q:w=1.2:g=-1.5,equalizer=f=4200:t=q:w=1.4:g=1.5,"
          "equalizer=f=7200:t=q:w=1.6:g=2,deesser=i=0.14:m=0.5:f=0.35,"
          "acompressor=threshold=-20dB:ratio=2.2:attack=10:release=200:makeup=1.5,"
          "alimiter=limit=0.95,loudnorm=I=-17:TP=-1.5:LRA=10")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--line", required=True, help="the line as the caption shows it")
    ap.add_argument("--respell", default="", help="comma-separated spellings to try for the hard word")
    ap.add_argument("--word", default="", help="the word being respelled (defaults to the last respell target)")
    ap.add_argument("--n", type=int, default=5, help="how many candidates")
    ap.add_argument("--seeds", default="", help="explicit seeds, comma-separated")
    ap.add_argument("--out", default="export/line-candidates.m4a")
    ap.add_argument("--exaggeration", type=float, default=0.40)
    ap.add_argument("--cfg", type=float, default=0.60)
    ap.add_argument("--lang", default=None)
    a = ap.parse_args()

    spellings = [s.strip() for s in a.respell.split(",") if s.strip()] or [""]
    seeds = [int(s) for s in a.seeds.split(",") if s.strip()] or list(range(7, 7 + a.n))

    # candidates: each spelling gets its own seed, so the list stays short enough to judge
    cands = []
    for i in range(a.n):
        sp = spellings[i % len(spellings)]
        cands.append({"seed": seeds[i % len(seeds)], "respell": sp})

    import torch, torchaudio
    torch.set_num_threads(os.cpu_count() or 4)
    if a.lang:
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS as TTS
    else:
        from chatterbox.tts import ChatterboxTTS as TTS
    m = TTS.from_pretrained(device="cpu")
    tmp = tempfile.mkdtemp()
    parts = []

    for n, c in enumerate(cands, 1):
        spoken = a.line
        if c["respell"]:
            target = a.word or _guess_target(a.line, c["respell"])
            if target:
                spoken = a.line.replace(target, c["respell"])
        torch.manual_seed(c["seed"])
        kw = dict(audio_prompt_path=REF, exaggeration=a.exaggeration,
                  cfg_weight=a.cfg, temperature=0.75)
        if a.lang:
            kw["language_id"] = a.lang
        wav = m.generate(spoken, **kw)
        raw = os.path.join(tmp, f"r{n}.wav")
        torchaudio.save(raw, wav, m.sr)
        pol = os.path.join(tmp, f"p{n}.wav")
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",raw,
                        "-af",POLISH,"-ar","48000","-ac","1",pol], check=True)
        lab = os.path.join(tmp, f"l{n}.wav")
        subprocess.run(["piper","--model","/tmp/voices/en_US-lessac-medium.onnx",
                        "--output_file",lab], input=f"Option {n}.".encode(),
                       check=True, capture_output=True)
        lab48 = os.path.join(tmp, f"l{n}48.wav")
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",lab,
                        "-ar","48000","-ac","1","-af","volume=0.5",lab48], check=True)
        parts += [lab48, pol]
        print(f"option {n}: seed {c['seed']}"
              + (f", spelled \"{c['respell']}\"" if c["respell"] else ", as written"), flush=True)

    args = ["ffmpeg","-hide_banner","-loglevel","error","-y"]
    for p in parts:
        args += ["-i", p]
    chain = "".join(f"[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono[a{i}];"
                    for i in range(len(parts)))
    chain += "".join(f"[a{i}]" for i in range(len(parts)))
    chain += f"concat=n={len(parts)}:v=0:a=1,loudnorm=I=-16:TP=-1.5[out]"
    args += ["-filter_complex", chain, "-map", "[out]", "-c:a", "aac", "-b:a", "192k", a.out]
    subprocess.run(args, check=True)

    json.dump({"line": a.line, "candidates": cands, "out": a.out},
              open("audio/voice/profile/line-candidates.json", "w"),
              ensure_ascii=False, indent=1)
    print(f"\nwrote {a.out} — pick an option number, then store it with:\n"
          f"  python3 audio/line_doctor.py --lock <n>", flush=True)

def _guess_target(line, respell):
    """The respelling usually differs from the real word by a letter or two; find the word
    it is closest to rather than making him name it."""
    import difflib
    words = [w.strip(".,!?—-") for w in line.split()]
    best = difflib.get_close_matches(respell, words, n=1, cutoff=0.5)
    return best[0] if best else ""

if __name__ == "__main__":
    main()
