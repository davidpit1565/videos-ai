# /opt/v311/bin/python fixaccent.py <tag> <hookwav> <hooktxt> : the accent classifier is context sensitive (the same body take scored 0.04 under one hook and 0.98 under another).
# Scores the stitched narration-<tag>.wav; every body line above 0.2 gets its take re-chosen IN this stitch among the cached takes whose text matched (ok-cands.json).
# Writes picks-<tag>.json (never touches the shared body-picks.json) and prints "CHANGED" if a re-stitch is needed.
import json, os, re, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__)) + '/'; tag, hookwav, hooktxt = sys.argv[1:4]
picks = json.load(open(D + 'body-picks.json')); OK = json.load(open(D + 'ok-cands.json')); changed = False
def accent(pk, name):
    json.dump(pk, open(D + f'picks-{tag}-tmp.json', 'w'))
    env = dict(os.environ, PICKS=D + f'picks-{tag}-tmp.json', HOOKWAV=hookwav, HOOKTXT=hooktxt)
    subprocess.run(['/opt/v311/bin/python', D + 'stitch.py', name], env=env, capture_output=True, check=True)
    subprocess.run(['python3', '/home/user/videos-ai/export/hf_cues.py', D + f'cues-{name}.json', f'/tmp/{name}-vd.json'], capture_output=True)
    r = subprocess.run(['/opt/v311/bin/python', '/home/user/videos-ai/audio/check_accent.py', D + f'narration-{name}.wav', '--cues', f'/tmp/{name}-vd.json'], capture_output=True, text=True, cwd='/home/user/videos-ai')
    return {int(m.group(1)): float(m.group(2)) for m in re.finditer(r'ln\s+(\d+)\s+top=\S+ [0-9.]+\s+not-american=([0-9.]+)', r.stdout)}
for rnd in range(3):
    sc = accent(picks, 'fx-' + tag); bad = [n for n, v in sc.items() if n >= 2 and v > 0.2]
    print('round', rnd, 'flagged lines', bad, flush=True)
    if not bad: break
    for n in bad:
        i = n - 1; best = None
        for rel in OK[str(i)]:
            pk = dict(picks); pk[str(i)] = rel; v = accent(pk, 'fx-' + tag).get(n, 9)
            if best is None or v < best[0]: best = (v, rel)
        print('line', n, 'take', picks[str(i)], '->', best, flush=True)
        if best[1] != picks[str(i)]: picks[str(i)] = best[1]; changed = True
json.dump(picks, open(D + f'picks-{tag}.json', 'w'), indent=1)
for f in (f'picks-{tag}-tmp.json', f'cues-fx-{tag}.json', f'narration-fx-{tag}.wav'):
    try: os.remove(D + f)
    except OSError: pass
print('CHANGED' if changed else 'UNCHANGED')
