#!/usr/bin/env python3
"""TH listen-proxy: how much more likely is the CTC (wav2vec2 char model) reading with a TH than the readings a missing/changed TH would give?
margin = min over alternatives of [-logP(alt|audio)] - [-logP("ANTHROPIC'S"|audio)]  (nats; positive = the audio supports the real spelling).
Also reports the best alternative. Context = the whole sentence, so the language-free char model hears the word in place.
usage: thctc.py <take.wav> ...   or  thctc.py <wav:a:b> for the line-2 word window (context-free word, text ANTHROPIC)"""
import sys, json, numpy as np, librosa, torch
sys.path.insert(0, ".")
import rword
SR = 16000
d = {c: i for i, c in enumerate(rword._LAB)}
def nll(em, txt):
    tok = torch.tensor([[d[c] for c in txt]]); lp = em.log_softmax(-1).transpose(0, 1)
    return float(torch.nn.functional.ctc_loss(lp, tok, torch.tensor([em.shape[1]]), torch.tensor([len(txt)]), blank=0, reduction="sum", zero_infinity=True))
ALT = ["ANTROPIC'S", "ANTFROPIC'S", "ANTOPIC'S", "ANTIPIC'S", "ANPROPIC'S", "ANTFOPIC'S", "ANTHOPIC'S", "ANTROPIK'S", "ANTIPICS", "ANTFIK'S"]
def score(y, ctx_before="THE|LINKS|TO|", word="ANTHROPIC'S", ctx_after="|OWN|REPORT|ARE|IN|THE|CAPTION"):
    with torch.no_grad(): em, _ = rword._M(torch.tensor(y, dtype=torch.float32)[None])
    base = nll(em, ctx_before + word + ctx_after)
    alts = {a: nll(em, ctx_before + a + ctx_after) for a in [x.replace("'S", "'S") for x in ALT]}
    b = min(alts, key=alts.get); return round(alts[b] - base, 2), b
if __name__ == "__main__":
    out = {}
    for arg in sys.argv[1:]:
        p, *ab = arg.split(":")
        y, _ = librosa.load(p, sr=SR); y = y / (np.abs(y).max() + 1e-9)
        if ab:
            y = y[int(float(ab[0]) * SR):int(float(ab[1]) * SR)]
            y = np.concatenate([np.zeros(int(0.2 * SR)), y, np.zeros(int(0.2 * SR))])
            with torch.no_grad(): em, _ = rword._M(torch.tensor(y, dtype=torch.float32)[None])
            base = nll(em, "ANTHROPIC"); alts = {a.rstrip("S").rstrip("'"): nll(em, a.replace("'S", "").rstrip("S")) for a in ALT}
            b = min(alts, key=alts.get); m, bb = round(alts[b] - base, 2), b
        else: m, bb = score(y)
        out[arg.split("/")[-1]] = (m, bb); print(arg.split("/")[-1], m, bb, flush=True)
    json.dump(out, open("thctc.json", "w"))
