#!/usr/bin/env python3
"""Several takes of the Flemish voice from the reference he picked, so he can choose again.

He chose option 1 — the window at 0-14s of his recording — and named one defect: the
word "persoon". So the reference is fixed and only the generation varies: two settings
that change how animated the delivery is, and a respelling of the word he flagged.

  python3 audio/flemish_variants.py
"""
import os, subprocess
import torch, torchaudio, warnings
warnings.filterwarnings("ignore")
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

REF = "audio/voice/profile/flemish/ref-1.wav"
LINE = ("Agenten mislukken vol zelfvertrouwen. Ze sturen een mail naar de {p}, "
        "heel vriendelijk. De test is simpel: als het niks kan doen zonder jou, "
        "is het gewoon een chatbot met een schonere naam.")
POLISH = ("highpass=f=75,equalizer=f=4200:t=q:w=1.4:g=1.5,equalizer=f=7200:t=q:w=1.6:g=2,"
          "deesser=i=0.14:m=0.5:f=0.35,"
          "acompressor=threshold=-20dB:ratio=2.2:attack=10:release=200:makeup=1.5,"
          "alimiter=limit=0.95,loudnorm=I=-17:TP=-1.5:LRA=10")
# (label, exaggeration, cfg, spelling of "verkeerde persoon")
TAKES = [
    ("a", 0.50, 0.30, "verkeerde persoon"),
    ("b", 0.50, 0.30, "verkeerde per-sohn"),
    ("c", 0.42, 0.45, "verkeerde persoon"),
    ("d", 0.58, 0.25, "verkeerde per-sohn"),
]

torch.set_num_threads(int(os.environ.get("VOICE_THREADS", "3")))
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
for label, ex, cfg, spell in TAKES:
    torch.manual_seed(7)
    wav = m.generate(LINE.format(p=spell), language_id="nl", audio_prompt_path=REF,
                     exaggeration=ex, cfg_weight=cfg, temperature=0.75)
    raw = f"/tmp/fv-{label}.wav"
    torchaudio.save(raw, wav, m.sr)
    out = f"export/flemish-1{label}.m4a"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", raw,
                    "-af", POLISH, "-c:a", "aac", "-b:a", "192k", out], check=True)
    print(f"wrote {out}  exaggeration {ex} cfg {cfg}  \"{spell}\"", flush=True)
