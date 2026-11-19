# eval_ivy.py <voice>: per take Whisper text match, word gaps, pitch range/end, last-90ms energy, RMS (run with /opt/v311/bin/python)
import sys, re, glob, numpy as np, librosa, soundfile as sf
from faster_whisper import WhisperModel
D = '/home/user/videos-ai/video/ad-ivy/voice/'; V = sys.argv[1]
L = [l.strip() for l in open(D + 'lines-ivy.txt') if l.strip()]
m = WhisperModel('small.en', device='cpu', compute_type='int8')
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace('-', ' ')).split()
for n, exp in enumerate(L, 1):
    for p in sorted(glob.glob(D + f'takes/{V}-L{n}-s*.wav')):
        segs, _ = m.transcribe(p, language='en', word_timestamps=True); w = [x for s in segs for x in s.words]
        got = norm(' '.join(x.word for x in w)); ok = got == norm(exp) or got == norm(exp.replace('ChatGPT', 'chat GPT'))
        y, sr = librosa.load(p, sr=16000); d = len(y) / sr
        f0, _, _ = librosa.pyin(y, fmin=70, fmax=450, sr=sr, frame_length=1024); v = ~np.isnan(f0); st = 12 * np.log2(f0 / np.nanmedian(f0))
        rng = np.nanpercentile(st[v], 90) - np.nanpercentile(st[v], 10); t = np.arange(len(f0)) * 512 / sr; tail = (t >= d - .7) & v
        end = float(np.nanmean(st[tail])) if tail.sum() > 2 else float('nan')
        sp = np.abs(y) > 10 ** (-40 / 20) * np.abs(y).max(); idx = np.where(sp)[0]; last = y[idx[-1] - int(.09 * sr):idx[-1]]
        rms = lambda z: 20 * np.log10(np.sqrt((z ** 2).mean()) + 1e-9)
        gaps = [(w[k].word.strip(' .,?!'), w[k + 1].word.strip(' .,?!'), round(w[k + 1].start - w[k].end, 2)) for k in range(len(w) - 1) if w[k + 1].start - w[k].end > .1]
        print(f"L{n} {p.split('-')[-1][:-4]} {'OK ' if ok else 'TXT'} dur {d:.2f} rng {rng:.1f} end {end:+.1f} last90 {rms(last) - rms(y):+.1f} rms {rms(y):.1f} gaps {gaps} | {' '.join(x.word.strip() for x in w)}")
