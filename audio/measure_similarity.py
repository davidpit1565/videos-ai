"""Speaker similarity, measured rather than guessed: cosine distance between his real
recording and every candidate, using the same voice encoder the cloner itself uses."""
import sys, numpy as np, librosa, torch, warnings
warnings.filterwarnings("ignore")
from safetensors.torch import load_file
from chatterbox.models.voice_encoder import VoiceEncoder

W = "/root/.cache/huggingface/hub/models--ResembleAI--chatterbox/snapshots/5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18/ve.safetensors"
ve = VoiceEncoder()
ve.load_state_dict(load_file(W))
ve.eval()

def emb(p):
    y, sr = librosa.load(p, sr=16000, mono=True)
    y = y / (np.abs(y).max() + 1e-9)
    with torch.no_grad():
        e = ve.embeds_from_wavs([y], sample_rate=16000, as_spk=True)
    e = np.asarray(e).reshape(-1)
    return e / (np.linalg.norm(e) + 1e-9)

anchor = emb(sys.argv[1])
print(f"anchor: {sys.argv[1].split('/')[-1]}")
rows = []
for p in sys.argv[2:]:
    rows.append((float(anchor @ emb(p)), p.split("/")[-1]))
for s, n in sorted(rows, reverse=True):
    print(f"  {s:.4f}  {n}")
