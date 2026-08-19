Usage: python3 audio/compare_voices.py
Writes audio/voice/test/v*.wav and export/voice-test-5-versions.m4a.

"""One labelled listening test that separates the three things that changed between the
version he liked and the one he rejected: which reference, which generation parameters,
and how hard the polish chain pushes. Same three sentences in every variant."""
import os, subprocess, tempfile, numpy as np, librosa, torch, torchaudio, warnings
warnings.filterwarnings("ignore")
from safetensors.torch import load_file
from chatterbox.models.voice_encoder import VoiceEncoder
from chatterbox.tts import ChatterboxTTS

ANCHOR = "/root/.claude/uploads/1f1cff20-40a4-5c42-978b-9ebf1a6d6d56/38989033-New_Recording.m4a"
VEW = "/root/.cache/huggingface/hub/models--ResembleAI--chatterbox/snapshots/5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18/ve.safetensors"
OLD_REF = "audio/voice/profile/reference-take1.wav"
NEW_REF = "audio/voice/profile/reference.wav"
LINES = [
    "Your ChatGPT gives you generic answers.",
    "Not because it's dumb. Nobody told it how to think.",
    "It makes ChatGPT think harder — not be right more often.",
]
HEAVY = ("highpass=f=80,equalizer=f=240:t=q:w=1.2:g=-2,equalizer=f=2600:t=q:w=1.3:g=2.5,"
 "equalizer=f=4200:t=q:w=1.4:g=2.5,equalizer=f=5000:t=q:w=1.4:g=3,equalizer=f=7200:t=q:w=1.6:g=4.5,"
 "treble=g=2.5:f=10000,deesser=i=0.18:m=0.5:f=0.35,"
 "acompressor=threshold=-20dB:ratio=2.6:attack=8:release=180:makeup=2,alimiter=limit=0.95,"
 "loudnorm=I=-17:TP=-1.5:LRA=10")
LIGHT = ("highpass=f=75,equalizer=f=240:t=q:w=1.2:g=-1.5,equalizer=f=4200:t=q:w=1.4:g=1.5,"
 "equalizer=f=7200:t=q:w=1.6:g=2,deesser=i=0.14:m=0.5:f=0.35,"
 "acompressor=threshold=-20dB:ratio=2.2:attack=10:release=200:makeup=1.5,alimiter=limit=0.95,"
 "loudnorm=I=-17:TP=-1.5:LRA=10")

VARIANTS = [
    ("1", OLD_REF, 0.45, 0.45, HEAVY, "the recipe behind the version he liked"),
    ("2", OLD_REF, 0.45, 0.45, LIGHT, "same, softer polish"),
    ("3", NEW_REF, 0.45, 0.45, HEAVY, "new reference, old parameters and polish"),
    ("4", NEW_REF, 0.40, 0.60, LIGHT, "current default — the one he calls Indian"),
    ("5", OLD_REF, 0.50, 0.30, HEAVY, "old reference, following his prosody harder"),
]

ve = VoiceEncoder(); ve.load_state_dict(load_file(VEW)); ve.eval()
def emb(y, sr):
    if sr != 16000: y = librosa.resample(y, orig_sr=sr, target_sr=16000)
    with torch.no_grad():
        e = ve.embeds_from_wavs([y/(np.abs(y).max()+1e-9)], sample_rate=16000, as_spk=True)
    e = np.asarray(e).reshape(-1); return e/(np.linalg.norm(e)+1e-9)
a, _ = librosa.load(ANCHOR, sr=16000, mono=True); anchor = emb(a, 16000)

torch.set_num_threads(os.cpu_count() or 4)
m = ChatterboxTTS.from_pretrained(device="cpu")
tmp = tempfile.mkdtemp()
os.makedirs("audio/voice/test", exist_ok=True)

def label(n, path):
    raw = path + ".raw.wav"
    subprocess.run(["piper", "--model", "/tmp/voices/en_US-lessac-medium.onnx",
                    "--output_file", raw],
                   input=f"Version {n}.".encode(), check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", raw,
                    "-ar", "48000", "-ac", "1", "-af", "volume=0.5", path], check=True)

parts = []
print(f"{'variant':10}{'similarity':>12}  what it is", flush=True)
for name, ref, exag, cfg, chain, what in VARIANTS:
    outs = []
    for i, text in enumerate(LINES):
        torch.manual_seed(7 + i)
        wav = m.generate(text, audio_prompt_path=ref, exaggeration=exag, cfg_weight=cfg, temperature=0.75)
        r = os.path.join(tmp, f"r{name}{i}.wav"); torchaudio.save(r, wav, m.sr)
        q = os.path.join(tmp, f"p{name}{i}.wav")
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",r,"-af",chain,
                        "-ar","48000","-ac","1",q], check=True)
        outs.append(q)
    sims = []
    for q in outs:
        y, sr = librosa.load(q, sr=None, mono=True); sims.append(float(anchor @ emb(y, sr)))
    print(f"{name:10}{np.mean(sims):12.4f}  {what}", flush=True)
    joined = f"audio/voice/test/v{name}.wav"
    lst = os.path.join(tmp, f"l{name}.txt")
    with open(lst, "w") as f:
        for q in outs: f.write(f"file '{q}'\n")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0",
                    "-i",lst,"-ar","48000","-ac","1",joined], check=True)
    lab = os.path.join(tmp, f"lab{name}.wav"); label(name, lab)
    parts += [lab, joined]

# The concat filter rather than the demuxer: it resamples every input instead of
# trusting that they already match, which is what silently truncated the first montage
# to under a second.
args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
for p in parts:
    args += ["-i", p]
chain = "".join(
    f"[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono[a{i}];"
    for i in range(len(parts))
)
chain += "".join(f"[a{i}]" for i in range(len(parts)))
chain += f"concat=n={len(parts)}:v=0:a=1,loudnorm=I=-16:TP=-1.5[out]"
args += ["-filter_complex", chain, "-map", "[out]", "-c:a", "aac", "-b:a", "192k",
         "export/voice-test-5-versions.m4a"]
subprocess.run(args, check=True)
print("wrote export/voice-test-5-versions.m4a", flush=True)
