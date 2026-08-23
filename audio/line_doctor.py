"""Fix one stubborn line, and rank the candidates instead of guessing.

Whisper only tells you whether a word is intelligible — it heard "harder" correctly even
in the take he says swallows it. What he is actually hearing is a final consonant with no
energy in it: the R, T and D at the ends of words arrive soft. That is measurable.

For every candidate this tool locates each target word by its Whisper timestamp and scores
the last 90 ms of it — high-frequency energy relative to the word's own body, plus how fast
the word was spoken. A swallowed R or T shows up as a low tail. The candidates are ranked,
the best few are announced out loud in one file, and his pick is stored per line so future
renders reproduce exactly what he approved.

    python3 audio/line_doctor.py \
      --line "It makes ChatGPT think harder, not be right more often." \
      --targets harder,right \
      --subs '[{}, {"harder":"har-der"}, {"harder":"har-der","right":"rite"}]' \
      --params '[[0.50,0.30],[0.45,0.45]]' --top 3 --out export/line-harder.m4a
"""
import argparse, json, os, subprocess, tempfile, warnings
import numpy as np
warnings.filterwarnings("ignore")

REF = "audio/voice/profile/reference.wav"
CHOICES = "audio/voice/profile/line-choices.json"
POLISH = ("highpass=f=75,equalizer=f=240:t=q:w=1.2:g=-1.5,equalizer=f=4200:t=q:w=1.4:g=1.5,"
          "equalizer=f=7200:t=q:w=1.6:g=2,deesser=i=0.14:m=0.5:f=0.35,"
          "acompressor=threshold=-20dB:ratio=2.2:attack=10:release=200:makeup=1.5,"
          "alimiter=limit=0.95,loudnorm=I=-17:TP=-1.5:LRA=10")

def tail_energy(y, sr, t0, t1, tail_ms=90):
    """How much high-frequency energy is left at the end of the word, in dB relative to the
    word's body. A released R, T or D leaves energy up there; a swallowed one does not."""
    a, b = int(t0 * sr), int(t1 * sr)
    w = y[a:b]
    if len(w) < int(0.06 * sr):
        return None
    tail = w[-int(tail_ms / 1000 * sr):]
    def hf(x):
        S = np.abs(np.fft.rfft(x * np.hanning(len(x))))
        f = np.fft.rfftfreq(len(x), 1 / sr)
        band = (f >= 2000) & (f < 8000)
        return float(np.sqrt((S[band] ** 2).mean()) + 1e-9)
    body_rms = float(np.sqrt((w ** 2).mean()) + 1e-9)
    return 20 * np.log10(hf(tail) / (body_rms * len(tail) ** 0.5 + 1e-9) + 1e-12)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--line", required=True)
    ap.add_argument("--targets", default="", help="comma-separated words to score")
    ap.add_argument("--subs", default="[{}]", help="JSON list of respelling maps, one per variant")
    ap.add_argument("--params", default="[[0.45,0.45]]", help="JSON list of [exaggeration, cfg]")
    ap.add_argument("--seeds", default="7,8,9,10")
    ap.add_argument("--top", type=int, default=3, help="how many best candidates to put in the file")
    ap.add_argument("--out", default="export/line-candidates.m4a")
    ap.add_argument("--lang", default=None)
    a = ap.parse_args()

    targets = [t.strip().lower() for t in a.targets.split(",") if t.strip()]
    subs = json.loads(a.subs)
    params = json.loads(a.params)
    seeds = [int(s) for s in a.seeds.split(",") if s.strip()]

    import librosa, torch, torchaudio
    torch.set_num_threads(os.cpu_count() or 4)
    if a.lang:
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS as TTS
    else:
        from chatterbox.tts import ChatterboxTTS as TTS
    m = TTS.from_pretrained(device="cpu")
    from faster_whisper import WhisperModel
    asr = WhisperModel("small", device="cpu", compute_type="int8")
    tmp = tempfile.mkdtemp()

    cands = []
    n = 0
    for pi, (exag, cfg) in enumerate(params):
        for si, sub in enumerate(subs):
            n += 1
            spoken = a.line
            for real, spell in sub.items():
                spoken = spoken.replace(real, spell)
            seed = seeds[(n - 1) % len(seeds)]
            torch.manual_seed(seed)
            kw = dict(audio_prompt_path=REF, exaggeration=exag, cfg_weight=cfg, temperature=0.75)
            if a.lang:
                kw["language_id"] = a.lang
            wav = m.generate(spoken, **kw)
            raw = os.path.join(tmp, f"r{n}.wav")
            torchaudio.save(raw, wav, m.sr)
            pol = os.path.join(tmp, f"p{n}.wav")
            subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",raw,
                            "-af",POLISH,"-ar","48000","-ac","1",pol], check=True)
            sixteen = os.path.join(tmp, f"s{n}.wav")
            subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",pol,
                            "-ar","16000","-ac","1",sixteen], check=True)

            segs, _ = asr.transcribe(sixteen, language=a.lang or "en", word_timestamps=True)
            words = [(w.word.strip(" ,.!?—").lower(), w.start, w.end)
                     for s in segs for w in (s.words or [])]
            y, sr = librosa.load(pol, sr=None, mono=True)
            scores, rates, missing = [], [], []
            for t in targets:
                hit = next((w for w in words if w[0] == t), None)
                if not hit:
                    missing.append(t)
                    continue
                e = tail_energy(y, sr, hit[1], hit[2])
                if e is not None:
                    scores.append(e)
                rates.append(len(t) / max(0.12, hit[2] - hit[1]))
            cands.append({
                "n": n, "seed": seed, "exag": exag, "cfg": cfg, "sub": sub,
                "tail_db": None if not scores else round(float(np.mean(scores)), 2),
                "chars_per_s": None if not rates else round(float(np.mean(rates)), 1),
                "missing": missing, "path": pol,
            })
            print(f"{n:2}  exag {exag:.2f} cfg {cfg:.2f}  {json.dumps(sub, ensure_ascii=False):38}"
                  f"  tail {cands[-1]['tail_db']}  speed {cands[-1]['chars_per_s']}"
                  + (f"  MISSING {missing}" if missing else ""), flush=True)

    ranked = sorted([c for c in cands if c["tail_db"] is not None and not c["missing"]],
                    key=lambda c: -c["tail_db"])
    if not ranked:
        ranked = cands
    best = ranked[: a.top]
    print("\nranked by how much energy survives at the end of the target words:")
    for i, c in enumerate(best, 1):
        print(f"  option {i}: tail {c['tail_db']} dB · seed {c['seed']} · exag {c['exag']} "
              f"cfg {c['cfg']} · {json.dumps(c['sub'], ensure_ascii=False)}", flush=True)

    parts = []
    for i, c in enumerate(best, 1):
        lab = os.path.join(tmp, f"lab{i}.wav")
        subprocess.run(["piper","--model","/tmp/voices/en_US-lessac-medium.onnx",
                        "--output_file",lab], input=f"Option {i}.".encode(),
                       check=True, capture_output=True)
        lab48 = os.path.join(tmp, f"lab{i}48.wav")
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",lab,
                        "-ar","48000","-ac","1","-af","volume=0.5",lab48], check=True)
        parts += [lab48, c["path"]]

    # The codec has to match the container the extension asks for, not just always be
    # AAC: ffmpeg will happily wrap a raw AAC stream in a WAV file with no error, but the
    # WAV muxer writes no ADTS framing for it, so anything that demuxes the file again —
    # the studio's own "convert to m4a for playback" step — reads it as a corrupt
    # elementary stream and throws hundreds of decoder errors. That is what happened to
    # audio/voice/line12-candidates.wav: it was written with --out ending in .wav while
    # the encoder stayed hardcoded to AAC.
    ext = os.path.splitext(a.out)[1].lower()
    codec_for_ext = {".m4a": ["-c:a", "aac", "-b:a", "192k"],
                     ".wav": ["-c:a", "pcm_s16le"]}
    if ext not in codec_for_ext:
        sys.exit(f"--out must end in .m4a or .wav (got {ext}) — "
                 f"the encoder is chosen from the extension, not assumed")

    args = ["ffmpeg","-hide_banner","-loglevel","error","-y"]
    for p in parts:
        args += ["-i", p]
    chain = "".join(f"[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono[a{i}];"
                    for i in range(len(parts)))
    chain += "".join(f"[a{i}]" for i in range(len(parts)))
    chain += f"concat=n={len(parts)}:v=0:a=1,loudnorm=I=-16:TP=-1.5[out]"
    args += ["-filter_complex", chain, "-map", "[out]", *codec_for_ext[ext], a.out]
    subprocess.run(args, check=True)

    json.dump({"line": a.line, "targets": targets,
               "options": [{k: v for k, v in c.items() if k != "path"} for c in best],
               "all": [{k: v for k, v in c.items() if k != "path"} for c in cands]},
              open("audio/voice/profile/line-candidates.json", "w"),
              ensure_ascii=False, indent=1)
    print(f"\nwrote {a.out}", flush=True)

if __name__ == "__main__":
    main()
