import sys, numpy as np, soundfile as sf, librosa
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
for f in sys.argv[1:]:
    x, s = sf.read(f); x = x if x.ndim == 1 else x[:, 0]
    seg, _ = m.transcribe(f, language="en", word_timestamps=True)
    ws = [(w.word.strip(), w.start, w.end) for sg in seg for w in sg.words]
    f0, v, _ = librosa.pyin(x.astype(float), fmin=70, fmax=400, sr=s, frame_length=2048, hop_length=240, fill_na=np.nan)
    t = np.arange(len(f0)) * 240 / s
    b = ws[1]; nxt = ws[2]
    k = (t >= b[2] - .18) & (t <= b[2]) & ~np.isnan(f0)
    slope = np.polyfit(t[k], 12 * np.log2(f0[k] / np.nanmedian(f0)), 1)[0] if k.sum() >= 4 else float('nan')
    # end energy of "begged" and the pause before "Can"
    e = lambda a, c: 20 * np.log10(np.sqrt(np.mean(x[int(a * s):int(c * s)] ** 2)) + 1e-9)
    print(f, ' '.join(w[0] for w in ws), "| begged slope last180ms %.1f st/s (voiced frames %d)" % (slope, k.sum()), "| pause begged->next %.2fs" % (nxt[1] - b[2]), "| end level %.0f dB" % e(b[2] - .08, b[2]))
