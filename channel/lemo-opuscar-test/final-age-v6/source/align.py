"""align.py <cues.json> [narration.wav] [--out voices] : writes voices/{cues,dur,words,meta}.json for the page.
cues.json = [{n,line,start,end}]. The words are the lines of script.json (the page's own script), NOT the cue file's text.
With a narration.wav it forces wav2vec2 alignment per line (needs torch: run with ALIGN_PY, default /opt/v311/bin/python); on any failure a line falls back to character-count timing and says so."""
import json, sys, os, re
args = [a for a in sys.argv[1:] if not a.startswith('--')]
cues = json.load(open(args[0])); wav = args[1] if len(args) > 1 else None
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, 'voices'); os.makedirs(out, exist_ok=True)
script = json.load(open(os.path.join(here, 'script.json')))
words, dur, starts, how = {}, {}, {}, {}
def fallback(n, c):
    toks = script[f'l{n}'].split(); d = (c['end'] - c['start']) * .96
    wt = [len(re.sub(r"[^a-z0-9']", '', t, flags=re.I)) + 1.1 for t in toks]; tot = sum(wt); a = 0; res = []
    for t, w in zip(toks, wt): res.append([t.lower(), round(a / tot * d, 3), round((a + w - 1.1) / tot * d, 3)]); a += w
    return res
model = None; wavdur = None
if wav:
    try:
        import torch, torchaudio, soundfile as sf, soxr, torchaudio.functional as F
        from torchaudio.pipelines import WAV2VEC2_ASR_BASE_960H as B
        model = B.get_model().eval(); lab = B.get_labels(); dct = {c: i for i, c in enumerate(lab)}
        x, sr = sf.read(wav, dtype='float32'); x = x.mean(1) if x.ndim > 1 else x
        x16 = soxr.resample(x, sr, 16000).astype('float32'); wavdur = len(x) / sr
    except Exception as e:
        print('ALIGN UNAVAILABLE, using character-count fallback for every line:', repr(e)[:200]); model = None; wavdur = None
for c in cues:
    n = c['n']; starts[f'l{n}'] = c['start']; dur[f'l{n}'] = round(c['end'] - c['start'], 3)
    try:
        if model is None: raise RuntimeError('no model')
        a = max(0, c['start'] - .25); b = c['end'] + .35
        seg = torch.from_numpy(x16[int(a * 16000):int(b * 16000)])[None]
        with torch.no_grad(): em, _ = model(seg)
        em = torch.log_softmax(em, -1); toks_txt = script[f'l{n}'].split()
        ws = [re.sub(r"[^A-Z']", '', t.upper()) for t in toks_txt]
        toks, idx = [], []
        for wi, w in enumerate(ws):
            for ch in w: toks.append(dct[ch]); idx.append(wi)
            if wi < len(ws) - 1: toks.append(dct['|']); idx.append(-1)
        al, sc = F.forced_align(em, torch.tensor([toks], dtype=torch.int32), blank=0)
        sp = torchaudio.functional.merge_tokens(al[0], sc[0].exp()); ratio = (seg.shape[1] / em.shape[1]) / 16000
        assert len(sp) == len(toks)
        st, en = {}, {}
        for s, wi in zip(sp, idx):
            if wi < 0: continue
            st.setdefault(wi, a + s.start * ratio); en[wi] = a + s.end * ratio
        words[f'l{n}'] = [[toks_txt[i].lower(), round(st[i] - c['start'], 3), round(en[i] - c['start'], 3)] for i in range(len(ws))]; how[f'l{n}'] = 'aligned'
    except Exception as e:
        words[f'l{n}'] = fallback(n, c); how[f'l{n}'] = 'fallback(' + repr(e)[:60] + ')'
last = max(c['end'] for c in cues)
meta = {'dur': round((wavdur + .3) if wavdur else last + 1.1, 3), 'how': how}
for k, v in (('words', words), ('dur', dur), ('cues', starts), ('meta', meta)): json.dump(v, open(os.path.join(out, k + '.json'), 'w'))
print('align:', {k: v[:9] for k, v in how.items()}, 'dur', meta['dur'])
