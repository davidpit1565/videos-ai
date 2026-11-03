import sys, numpy as np, librosa, soundfile as sf
sys.path.insert(0, ".")
import thctc, rword, torch
from faster_whisper import WhisperModel
W = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=2)
def asr(f):
    y, _ = librosa.load(f, sr=16000); y = np.concatenate([np.zeros(8000), y, np.zeros(8000)]).astype(np.float32)
    sg, _ = W.transcribe(y, language="en", beam_size=5); return " ".join(s.text.strip() for s in sg)
def click(f, a, b):
    x, sr = sf.read(f); x = x if x.ndim == 1 else x[:, 0]; d = np.abs(np.diff(x)); n = np.percentile(d, 99.9)
    return round(float(d[int(a * sr):int(b * sr)].max() / n), 2), round(float(np.abs(x).max()), 2)
for tag, f0, f1, a, b in (("line2", "voice/final2-before-v7.wav", "voice/l2-v7.wav", 0.04, 0.63), ("line9", "voice/l9-v4c.wav", "voice/l9-v7.wav", 0.60, 1.34)):
    print(tag, "BEFORE heard:", asr(f0), "| click ratio, peak", click(f0, a, b))
    print(tag, "AFTER  heard:", asr(f1), "| click ratio, peak", click(f1, a, b))
y, _ = librosa.load("voice/l9-v4c.wav", sr=16000); y /= np.abs(y).max() + 1e-9; print("line9 TH margin before", thctc.score(y))
y, _ = librosa.load("voice/l9-v7.wav", sr=16000); y /= np.abs(y).max() + 1e-9; print("line9 TH margin after ", thctc.score(y))
for nm, f in (("line2 before", "voice/final2-before-v7.wav"), ("line2 after", "voice/l2-v7.wav")):
    y, _ = librosa.load(f, sr=16000); y = y[int(0.04 * 16000):int(0.616 * 16000)]; y = np.concatenate([np.zeros(3200), y, np.zeros(3200)]); y /= np.abs(y).max() + 1e-9
    with torch.no_grad(): em, _ = rword._M(torch.tensor(y, dtype=torch.float32)[None])
    base = thctc.nll(em, "ANTHROPIC"); al = {a.rstrip("S").rstrip("'"): thctc.nll(em, a.replace("'S", "").rstrip("S")) for a in thctc.ALT}; b = min(al, key=al.get); print(nm, "TH margin (word only)", round(al[b] - base, 2), b)
