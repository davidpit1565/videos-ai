"""Chatterbox conditions prosody on the reference's first 6 seconds and the decoder on
its first 10 — so which 10 seconds open the file matters more than anything else about it.
Search for the window that scores highest against his real voice, and lead with it."""
import json, numpy as np, librosa, soundfile as sf, torch, warnings
warnings.filterwarnings("ignore")
from safetensors.torch import load_file
from chatterbox.models.voice_encoder import VoiceEncoder

SRC = "audio/voice/work/t1-v1.wav"
ANCHOR = "/root/.claude/uploads/1f1cff20-40a4-5c42-978b-9ebf1a6d6d56/38989033-New_Recording.m4a"
W = "/root/.cache/huggingface/hub/models--ResembleAI--chatterbox/snapshots/5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18/ve.safetensors"

ve = VoiceEncoder(); ve.load_state_dict(load_file(W)); ve.eval()
def emb(y, sr=16000):
    with torch.no_grad():
        e = ve.embeds_from_wavs([y], sample_rate=sr, as_spk=True)
    e = np.asarray(e).reshape(-1)
    return e / (np.linalg.norm(e) + 1e-9)

a, sr16 = librosa.load(ANCHOR, sr=16000, mono=True)
anchor = emb(a / (np.abs(a).max() + 1e-9))

y, sr = librosa.load(SRC, sr=24000, mono=True); y = y / (np.abs(y).max() + 1e-9)
y16 = librosa.resample(y, orig_sr=sr, target_sr=16000)

# candidate starts: utterance onsets, so a window never opens mid-word
segs = librosa.effects.split(y, top_db=32, frame_length=1024, hop_length=256)
starts = sorted({int(s / sr * 100) / 100 for s, _ in segs})
best = []
for st in starts:
    if st + 10 > len(y) / sr: continue
    w = y16[int(st * 16000):int((st + 10) * 16000)]
    if len(w) < 16000 * 9: continue
    best.append((float(anchor @ emb(w)), st))
best.sort(reverse=True)
print("best 10s windows (similarity to his real voice):")
for s, st in best[:6]: print(f"  {s:.4f}  starts {st:5.2f}s")
worst = best[-3:]
print("worst:", ", ".join(f"{s:.4f}@{st:.1f}s" for s, st in worst))

top_score, top_start = best[0]
# then append the highest-scoring utterances that follow, to ~30s total for the embedding
rest = []
for s0, s1 in segs:
    t0, t1 = s0 / sr, s1 / sr
    if t1 <= top_start + 10 and t0 >= top_start: continue
    if t1 - t0 < 0.8: continue
    seg16 = y16[int(t0 * 16000):int(t1 * 16000)]
    if len(seg16) < 16000 * 0.8: continue
    rest.append((float(anchor @ emb(seg16)), s0, s1))
rest.sort(reverse=True)
gap = np.zeros(int(0.2 * sr), dtype=np.float32)
parts = [y[int(top_start * sr):int((top_start + 10) * sr)], gap]
tot = 10.0
picked = []
for s, s0, s1 in rest:
    d = (s1 - s0) / sr
    if tot + d > 32: continue
    parts += [y[s0:s1], gap]; tot += d + 0.2; picked.append((s, round(d, 1)))
    if tot >= 28: break
out = np.concatenate(parts)
sf.write("audio/voice/profile/reference.wav", (out / (np.abs(out).max() + 1e-9) * 0.89).astype(np.float32), sr)
full = emb(librosa.resample(out, orig_sr=sr, target_sr=16000))
print(f"\nreference: {tot:.1f}s | opening window {top_score:.4f} | whole file {float(anchor@full):.4f}")
print("appended:", ", ".join(f"{s:.3f}/{d}s" for s, d in picked))
json.dump({
 "source": "38989033-New_Recording.m4a (take 1), 60 Hz rumble cut only",
 "why": ("Measured, not judged: the voice encoder that does the cloning scores take 1 against "
         "itself at 1.00, take 2 at 0.846, and the take-2 clone he rejected at 0.817 — his ear "
         "and the number agree. Denoising cost identity (0.987) so it was dropped."),
 "construction": ("Chatterbox conditions on the reference's first 6-10 seconds, so the 10-second "
                  "window scoring highest against his real voice opens the file; the rest is the "
                  "next-highest utterances, for the speaker embedding."),
 "opening_window_start_s": top_start,
 "opening_window_similarity": round(top_score, 4),
 "whole_file_similarity": round(float(anchor @ full), 4),
 "duration_s": round(tot, 1),
}, open("audio/voice/profile/profile.json", "w"), indent=1)
