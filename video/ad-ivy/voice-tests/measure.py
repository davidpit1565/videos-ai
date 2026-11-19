# measure.py: F0 median, pitch range p10-p90, end offset, last-90ms energy, Whisper text for every ivy-*.wav (run with /opt/v311/bin/python)
import glob, re, numpy as np, librosa
from faster_whisper import WhisperModel
m = WhisperModel('small.en', device='cpu', compute_type='int8')
for p in sorted(glob.glob('ivy-*.wav')):
    y, sr = librosa.load(p, sr=16000)
    f0, _, _ = librosa.pyin(y, fmin=70, fmax=450, sr=sr, frame_length=1024); ok = ~np.isnan(f0)
    med = np.nanmedian(f0); st = 12 * np.log2(f0 / med)
    rng = np.nanpercentile(st[ok], 90) - np.nanpercentile(st[ok], 10)
    t = np.arange(len(f0)) * 512 / sr; d = len(y) / sr; tail = (t >= d - .7) & ok
    end = float(np.nanmean(st[tail])) if tail.sum() > 2 else float('nan')
    segs, _ = m.transcribe(p, language='en'); txt = ' '.join(s.text.strip() for s in segs)
    print(f'{p}  dur {d:.2f}  F0med {med:.0f} Hz  range {rng:.1f} st  end {end:+.1f}  | {txt}')
