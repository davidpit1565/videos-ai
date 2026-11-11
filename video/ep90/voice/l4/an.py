import sys, json, numpy as np, soundfile as sf, librosa
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
for f in sys.argv[1:]:
    x, s = sf.read(f); x = x if x.ndim == 1 else x[:, 0]
    seg, _ = m.transcribe(f, language="en", word_timestamps=True)
    ws = [(w.word.strip(), w.start, w.end) for sg in seg for w in sg.words]
    f0, v, _ = librosa.pyin(x.astype(float), fmin=70, fmax=350, sr=s, frame_length=2048, hop_length=240)
    t = np.arange(len(f0)) * 240 / s
    med = np.nanmedian(f0)
    def st(a, b):
        k = (t >= a) & (t <= b) & ~np.isnan(f0)
        return 12 * np.log2(np.nanmedian(f0[k]) / med) if k.sum() > 2 else float('nan')
    w = ws[1] if len(ws) > 1 else ws[0]
    a = w[2]
    print(f, [x_[0] for x_ in ws], "begged end:", round(w[2], 2), "pitch last 90ms of word vs median: %.1f st; before-word mid: %.1f st; next word start: %.1f st" % (st(a - .09, a), st(w[1], a - .09), st(a + .02, a + .2)))
