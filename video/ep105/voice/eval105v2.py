# eval105v2.py <line> <seed...>: per-take Whisper text, gaps, pitch range/end, last-90ms energy (run with /opt/v311/bin/python)
import sys, re, json, numpy as np, librosa
from faster_whisper import WhisperModel
D = '/home/user/videos-ai/video/ep105/voice/'
lines = [l.strip() for l in open(D + 'lines105.txt') if l.strip()]
m = WhisperModel("small", device="cpu", compute_type="int8")
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("-", " "))
NUM = {'200': 'two hundred', '6': 'six', '10000': 'ten thousand', '1200': 'twelve hundred', '10,000': 'ten thousand'}
i = int(sys.argv[1]); exp = lines[i - 1]
for s in sys.argv[2:]:
    p = D + f'pl/V2-L{i}-{s}.wav'
    seg, _ = m.transcribe(p, language='en', word_timestamps=True); w = [x for g in seg for x in g.words]
    got = " ".join(x.word for x in w); gn = norm(got)
    c = json.load(open(D + f'pl/V2-L{i}-{s}-cues.json'))[0]; a, b = c['start'], c['end']
    y, sr = librosa.load(p, sr=16000, offset=a, duration=b - a)
    f0, _, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr, frame_length=1024); ok = ~np.isnan(f0)
    st = 12 * np.log2(f0 / np.nanmedian(f0)); rng = np.nanpercentile(st[ok], 90) - np.nanpercentile(st[ok], 10)
    t = np.arange(len(f0)) * 512 / sr; tail = (t >= (b - a) - .7) & ok; end = float(np.nanmean(st[tail])) if tail.sum() > 2 else float('nan')
    rms = lambda z: 20 * np.log10(np.sqrt((z ** 2).mean()) + 1e-9)
    e90 = rms(y[-int(.17 * sr):-int(.08 * sr)]) - rms(y)  # last 90 ms of speech vs line level
    gaps = [(w[k].word.strip(' .,?!'), w[k + 1].word.strip(' .,?!'), round(w[k + 1].start - w[k].end, 2)) for k in range(len(w) - 1) if w[k + 1].start - w[k].end > .1]
    print(f"V2-L{i}-{s}  dur {b - a:.2f}  range {rng:.1f}  end {end:+.1f}  last90 {e90:+.1f} dB  | {got.strip()}\n    gaps {gaps}")
