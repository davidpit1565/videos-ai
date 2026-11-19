# /opt/v311/bin/python inctx.py <hookwav> <hooktxt> "<body line numbers>" : the accent classifier scores a line differently inside the stitched file than alone,
# so each body take is chosen by its score IN the stitched narration (a hook as context), among takes whose Whisper text matched (ok-cands.json, from pickbody.py). Greedy per line; writes body-picks.json.
import json, os, re, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__)) + '/'
hookwav, hooktxt, only = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split()]
picks = json.load(open(D + 'body-picks.json')); OK = json.load(open(D + 'ok-cands.json'))
def score(pk, line):
    json.dump(pk, open(D + 'ctx-picks.json', 'w'))
    env = dict(os.environ, PICKS=D + 'ctx-picks.json', HOOKWAV=hookwav, HOOKTXT=hooktxt)
    subprocess.run(['/opt/v311/bin/python', D + 'stitch.py', 'ctx'], env=env, capture_output=True, check=True)
    subprocess.run(['python3', '/home/user/videos-ai/export/hf_cues.py', D + 'cues-ctx.json', '/tmp/ctx-vd.json'], capture_output=True)
    r = subprocess.run(['/opt/v311/bin/python', '/home/user/videos-ai/audio/check_accent.py', D + 'narration-ctx.wav', '--cues', '/tmp/ctx-vd.json'], capture_output=True, text=True, cwd='/home/user/videos-ai')
    m = re.search(r'ln\s+%d\s+top=\S+ [0-9.]+\s+not-american=([0-9.]+)' % (line + 1), r.stdout)
    return float(m.group(1)) if m else 9
for i in only:
    best = None
    for rel in OK[str(i)]:
        pk = dict(picks); pk[str(i)] = rel; sc = score(pk, i); print(i, rel, sc, flush=True)
        if best is None or sc < best[0]: best = (sc, rel)
    picks[str(i)] = best[1]; print('PICK', i, best, flush=True)
json.dump(picks, open(D + 'body-picks.json', 'w'), indent=1)
