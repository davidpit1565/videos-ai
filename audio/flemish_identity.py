#!/usr/bin/env python3
"""Keep the delivery he chose, and put more of him back into it.

He picked take c — the calmest of the four — and then said it still has to be
recognisably his voice. Measured against his real Flemish recording, c is in fact the
least like him of the four (0.8655 against 0.8846 for take a), so his ear and the
metric disagree, and both are right about different things: c has the delivery, a has
the identity.

The lever is the reference, not the settings. Chatterbox conditions prosody on the
first 6-10 seconds and takes the speaker embedding from the whole file — so keeping
c's opening window and appending more of his clean speech should hold the delivery
while giving the embedding more to work with. That is testable: same settings, three
references, measured similarity.

  python3 audio/flemish_identity.py <recording.wav>
"""
import os, subprocess, sys
import torch, torchaudio, warnings
warnings.filterwarnings("ignore")
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

OUT = "audio/voice/profile/flemish"
CLEAN = ("highpass=f=80,equalizer=f=3000:t=q:w=1.6:g=4,"
         "equalizer=f=6500:t=q:w=1.2:g=13,equalizer=f=8500:t=q:w=1.4:g=9,"
         "deesser=i=0.08:m=0.5:f=0.4,loudnorm=I=-19:TP=-2:LRA=11")
POLISH = ("highpass=f=75,equalizer=f=4200:t=q:w=1.4:g=1.5,equalizer=f=7200:t=q:w=1.6:g=2,"
          "deesser=i=0.14:m=0.5:f=0.35,"
          "acompressor=threshold=-20dB:ratio=2.2:attack=10:release=200:makeup=1.5,"
          "alimiter=limit=0.95,loudnorm=I=-17:TP=-1.5:LRA=10")
LINE = ("Agenten mislukken vol zelfvertrouwen. Ze sturen een mail naar de verkeerde "
        "per-sohn, heel vriendelijk. De test is simpel: als het niks kan doen zonder "
        "jou, is het gewoon een chatbot met een schonere naam.")
# take c's settings — the delivery he chose
EX, CFG = 0.42, 0.45
# (label, windows to concatenate; the first one is what the prosody is conditioned on)
REFS = [
    ("short", [(0, 14)]),
    ("long",  [(0, 14), (25, 39)]),
    ("full",  [(0, 14), (25, 39), (39, 53)]),
]


def ff(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def build_ref(src, windows, dst):
    parts = []
    for i, (t0, t1) in enumerate(windows):
        p = f"/tmp/fi-part{i}.wav"
        ff("-ss", str(t0), "-t", str(t1 - t0), "-i", src, "-af", CLEAN,
           "-ar", "24000", "-ac", "1", p)
        parts.append(p)
    if len(parts) == 1:
        ff("-i", parts[0], "-c", "copy", dst)
        return
    lst = "/tmp/fi-list.txt"
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    ff("-f", "concat", "-safe", "0", "-i", lst, "-ar", "24000", "-ac", "1", dst)


def main():
    src = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    torch.set_num_threads(int(os.environ.get("VOICE_THREADS", "3")))
    m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    for label, windows in REFS:
        ref = f"{OUT}/ref-c-{label}.wav"
        build_ref(src, windows, ref)
        secs = sum(t1 - t0 for t0, t1 in windows)
        torch.manual_seed(7)
        wav = m.generate(LINE, language_id="nl", audio_prompt_path=ref,
                         exaggeration=EX, cfg_weight=CFG, temperature=0.75)
        raw = f"/tmp/fi-{label}.wav"
        torchaudio.save(raw, wav, m.sr)
        out = f"export/flemish-c-{label}.m4a"
        ff("-i", raw, "-af", POLISH, "-c:a", "aac", "-b:a", "192k", out)
        print(f"wrote {out}  reference {secs:g}s from {windows}", flush=True)


if __name__ == "__main__":
    main()
