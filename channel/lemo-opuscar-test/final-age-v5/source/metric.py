import sys, subprocess, numpy as np
def win(f, fps=24):
    w, h = 108, 192
    p = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-vf', f'fps={fps},scale={w}:{h},format=gray', '-f', 'rawvideo', '-'], capture_output=True)
    a = np.frombuffer(p.stdout, np.uint8).reshape(-1, h, w).astype(np.float32); d = np.abs(np.diff(a, axis=0)).mean((1, 2)); n = int(fps * .5)
    return np.array([d[i:i + n].mean() for i in range(0, len(d) - n + 1, n)]), d
for f in sys.argv[1:]:
    wv, d = win(f)
    print(f.split('/')[-1], 'dur %.2f' % ((len(d) + 1) / 24), '| median %.2f | windows>5: %d | >10: %d | min %.2f (at %.1fs) | <0.4: %d of %d | max %.1f' % (np.median(wv), (wv > 5).sum(), (wv > 10).sum(), wv.min(), wv.argmin() * .5, (wv < .4).sum(), len(wv), wv.max()))
    print(' windows:', ' '.join('%.1f' % x for x in wv))
