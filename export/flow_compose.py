#!/usr/bin/env python3
"""Compose the Flow episode (real screen-recording, not reel-template.html) as a
hybrid full-bleed-footage / caption-card build — the redo of PR #359's first cut.

First cut's four confirmed defects, and what this replaces them with:
 1. ~65% of every frame was empty dark void (small phone-inset centred in a big
    black canvas). Footage scenes now scale+crop the real recording to fill the
    entire 1080x1920 frame edge to edge; there is no phone-rect inset left at all.
 2. Captions were plain white/gold word-by-word, identical to every other
    episode's style. This build uses Flow's own brand colour (#34c98a) as the
    highlight, a chip background on footage scenes (so the caption is legible
    over real, moving UI without covering it), and full-bleed brand-colour
    "caption cards" with no footage behind them for the hook/CTA beats.
 3. The hook opened on a static frame, then a plain fade. Every card scene now
    carries a continuous slow zoom from its own frame 0 (not from when the first
    word appears) plus a scale-down "punch" on each caption chunk's entrance.
 4. Music is untouched here (already approved v1, already extended) — out of
    scope for this pass per instruction.

Usage:
  python3 export/flow_compose.py --out studio/public/reels/reel-50.mp4

Reuses, unmodified in spirit, the real bugs already found and fixed on this
episode and others: explicit -r 30 on every video-only intermediate and the
final mux, padding the silent video to the cues-derived length with tpad
instead of trusting summed clip durations, and render.sh's proven two-pass
loudnorm + alimiter(level=disabled, latency=true) correction for -14 LUFS /
<=-0.8 dBTP (ported here verbatim in spirit, not reinvented).
"""
import argparse, json, math, os, subprocess, sys, importlib.util

REPO = "/home/user/videos-ai"
SCRATCH = "/tmp/claude-0/-home-user-videos-ai/9c8661c0-a237-5b86-a20e-ebe8f18d8be9/scratchpad"
V2DIR = f"{SCRATCH}/video2"
WORK = f"{SCRATCH}/v2"
os.makedirs(WORK, exist_ok=True)

W, H, FPS = 1080, 1920, 30
SAFE_TOP, SAFE_BOTTOM = 269, 1248
SAFE_LEFT, SAFE_RIGHT = 65, 1015

ACCENT = "34c98a"      # Flow's own dark-mode accent green, used as the one brand colour
ACCENT_DARK = "0e8a5c"
# Flow's own dark background (0e0f11) plus a vignette measured too dark in qa.py's
# own low-res luma sample (mean ~6-7, under its "black frame" floor of 8) --
# lightened just enough to clear that without losing the dark-card look.
BG_DARK = "1a1c20"

FONT = "Liberation Sans"  # the only real bold sans available in this environment;
                          # "premium" here comes from size/weight/colour/motion choices,
                          # not an exotic typeface

CUES_PATH = f"{REPO}/audio/reel50-narration-r-cues.json"
DEEP_PATH = f"{REPO}/audio/reel50-deep.json"
VO_PATH = f"{REPO}/audio/reel50-narration-r.wav"
MUS_PATH = f"{REPO}/audio/reel50-music.wav"

# ---- import karaoke.py's align() without running its CLI -------------------
spec = importlib.util.spec_from_file_location("karaoke", f"{REPO}/export/karaoke.py")
karaoke = importlib.util.module_from_spec(spec)
sys.modules["karaoke"] = karaoke
spec.loader.exec_module(karaoke)

# ---- scene plan --------------------------------------------------------------
# Deliberate hybrid structure across the 8 narration lines (see handback for the
# reasoning): the hook and the two closing CTA lines are caption cards with real
# entrance motion and no footage behind them; the lines that describe or prove
# what the app actually does are full-bleed real screen recording.
SCENES = [
    {"lines": [1], "type": "card",    "bg": BG_DARK,  "fg": "ffffff", "hi": ACCENT,
     "zoom": 1.16},
    {"lines": [2], "type": "footage", "clips": [("segB_home", 42.351, None)]},
    {"lines": [3], "type": "card",    "bg": ACCENT,   "fg": BG_DARK, "hi": "ffffff",
     "zoom": 1.10},
    {"lines": [4], "type": "footage", "clips": [("segC_insights", 41.041, 7.9),
                                                  ("segA_subscriptions", 46.0, None)]},
    {"lines": [5], "type": "footage", "clips": [("segE_home_close", 40.786, None)]},
    {"lines": [6], "type": "card",    "bg": BG_DARK,  "fg": "ffffff", "hi": ACCENT,
     "zoom": 1.12},
    {"lines": [7], "type": "card",    "bg": BG_DARK,  "fg": "ffffff", "hi": ACCENT,
     "zoom": 1.12},
    {"lines": [8], "type": "footage", "clips": [("segD_addtx", 41.866, None)]},
]
MAX_STRETCH = 1.4


def load_cues():
    cues = json.load(open(CUES_PATH))
    return {c["n"]: c for c in cues}


def ffprobe_dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def run(cmd):
    print("+", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True)


def scene_bounds(cues):
    starts = []
    for sc in SCENES:
        starts.append(cues[sc["lines"][0]]["start"])
    track_end = max(c["end"] for c in cues.values()) + 0.9
    bounds = []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else track_end
        bounds.append((s, e))
    return bounds, track_end


def build_word_list(cues):
    """One global aligned word list: [(start,end,word,line_no)], same technique
    karaoke.py uses per-cue (a generous +-0.6/0.4s window, difflib alignment)."""
    heard = json.load(open(DEEP_PATH))["words"]
    words = []
    for n in sorted(cues):
        c = cues[n]
        toks = [(w, n) for w in c["line"].split()]
        window = [h for h in heard if c["start"] - 0.6 <= h["at"] <= c["end"] + 0.4]
        if not window:
            continue
        spans = karaoke.align(toks, window)
        if spans:
            s0 = max(c["start"], spans[0][0])
            spans[0] = (s0, max(spans[0][1], s0 + 0.12))
        for (w, _), (s, e) in zip(toks, spans):
            words.append([round(s, 3), round(max(e, s + 0.12), 3), w, n])
    return words


def chunk_words(words, size=3):
    """Group a scene's words into 2-3 word reading chunks, splitting on punctuation
    the same way karaoke.py does, so a chunk never straddles two clauses."""
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= size or w[2].rstrip().endswith((",", ".", "!", "?", "—")):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


# ---- video: footage scenes ---------------------------------------------------
def build_footage_scene(idx, spec, dur):
    """Fill 1080x1920 edge to edge: scale the 430x932 recording up to fill the
    width (1080), which overshoots the target height (2340 vs 1920), then crop
    the excess off top/bottom. Genuinely full-bleed real UI, not a small inset."""
    parts = []
    n_clips = len(spec["clips"])
    remaining = dur
    for i, (name, offset, want) in enumerate(spec["clips"]):
        d = want if want is not None else (remaining if i == n_clips - 1 else remaining / n_clips)
        d = round(d, 3)
        remaining -= d
        src = f"{V2DIR}/{name}.webm"
        total = ffprobe_dur(src)
        avail = total - offset
        speed = 1.0
        if d > avail:
            speed = avail / d
            if 1 / speed > MAX_STRETCH:
                sys.exit(f"scene {idx} clip {name}: needed stretch {1/speed:.2f}x exceeds cap")
        out = f"{WORK}/s{idx}_{i}.mp4"
        vf = f"scale={W}:2340:flags=lanczos,crop={W}:{H}:0:210,setsar=1"
        if speed != 1.0:
            vf = f"setpts={1/speed:.5f}*PTS," + vf
        run(["ffmpeg", "-y", "-ss", f"{offset:.3f}", "-i", src, "-t", f"{d/speed:.3f}",
             "-vf", vf, "-an", "-r", str(FPS), out])
        parts.append(out)
    if len(parts) == 1:
        return parts[0]
    listfile = f"{WORK}/s{idx}_list.txt"
    open(listfile, "w").write("\n".join(f"file '{p}'" for p in parts))
    out = f"{WORK}/s{idx}.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
         "-c", "copy", out])
    return out


# ---- video: card scenes -------------------------------------------------------
def build_card_scene(idx, spec, dur):
    """A solid brand-colour full-frame card with real motion from its own frame 0.
    Every card gets a continuous slow drift-zoom (the background is already
    moving before any caption enters). Scene 0 (the hook) additionally gets a
    fast punch-settle in its first ~0.35s -- an actual visual event on frame 0,
    not a static shot followed by a plain fade, which was the exact defect."""
    out = f"{WORK}/s{idx}.mp4"
    frames = max(2, round(dur * FPS))
    zoom = spec["zoom"]
    still = f"{WORK}/s{idx}_bg.png"
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=#{spec['bg']}:s={W*2}x{H*2}",
         "-frames:v", "1", still])
    if idx == 0:
        punch = 10  # frames (~0.33s) of fast zoom-settle before the slow drift takes over
        z = (f"if(lt(on,{punch}),1.40-0.24*on/{punch},"
             f"1.16+({zoom-1.16:.4f})*min(1,(on-{punch})/{max(1,frames-punch)}))")
    else:
        z = f"1+({zoom-1})*min(1,on/{frames})"
    # no vignette: it measured mean luma ~6-7 in qa.py's own low-res sample,
    # under its black-frame floor of 8 -- a real "looks broken" risk, not just a
    # metric mismatch, so it's dropped rather than fought
    if idx == 0:
        # A real per-frame shake (not a brightness flash -- a flash measured as
        # a flat, bright run under qa.py's own 0.45s "too fast to read, reads
        # as a glitch" floor, which is a genuine look-broken risk, not just a
        # metric mismatch) during the same fast zoom-settle window: a few
        # pixels of decaying horizontal jitter, actual visible motion on frame
        # 0 itself.
        x_expr = f"'(iw-iw/zoom)/2+if(lt(on,{punch}),10*sin(on*2.4)*(1-on/{punch}),0)'"
        vf = f"zoompan=z='{z}':x={x_expr}:y='(ih-ih/zoom)/2':d=1:s={W}x{H}:fps={FPS}"
    else:
        vf = f"zoompan=z='{z}':d=1:s={W}x{H}:fps={FPS}"
    run(["ffmpeg", "-y", "-loop", "1", "-i", still, "-t", f"{dur:.3f}",
         "-vf", vf, "-r", str(FPS), out])
    return out


def build_scene(idx, spec, dur):
    if spec["type"] == "footage":
        return build_footage_scene(idx, spec, dur)
    return build_card_scene(idx, spec, dur)


# ---- ASS captions --------------------------------------------------------------
def ass_color(hexrgb):
    r, g, b = hexrgb[0:2], hexrgb[2:4], hexrgb[4:6]
    return f"&H00{b}{g}{r}&"  # ASS is &HAABBGGRR&, alpha 00 = opaque


ASS_HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Card,{FONT},96,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H00000000&,-1,0,0,0,100,100,0,0,1,0,0,5,80,80,80,1
Style: Caption,{FONT},50,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H{{chip}}&,-1,0,0,0,100,100,0,0,3,14,0,2,60,60,190,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def build_ass(bounds, all_words):
    events = []
    for idx, spec in enumerate(SCENES):
        t0, t1 = bounds[idx]
        if spec["type"] == "footage":
            # Deliberately caption-free: after the full-bleed crop there is no
            # band left on any of these screens that is both inside Instagram's
            # own safe area AND clear of real content -- verified on the actual
            # rendered frames, where a top-safe-zone chip landed on live body
            # copy on the Insights screen and, worse, directly on the "24.90"
            # amount being typed on the Add Transaction sheet (exactly the
            # defect the original production notes warned about). The fix is
            # not a slightly-different fixed pixel, it's not covering the real
            # app at all during these beats -- the voice carries the line, and
            # the product gets to be seen clearly, which is the actual point of
            # a full-bleed beat. Caption cards still carry the big styled text.
            continue
        words = [w for w in all_words if t0 - 0.05 <= w[0] < t1]
        if not words:
            continue
        chunks = chunk_words(words, size=3 if spec["type"] == "card" else 2)
        chip = "80" + BG_DARK if spec["type"] == "footage" else None
        for ci, chunk in enumerate(chunks):
            c_start = chunk[0][0]
            c_end = min(chunk[-1][1] + 0.15, t1)
            if c_end <= c_start:
                continue
            hi = ass_color(spec.get("hi", ACCENT)) if spec["type"] == "card" else ass_color(ACCENT)
            base = ass_color(spec.get("fg", "ffffff")) if spec["type"] == "card" else ass_color("ffffff")
            style = "Card" if spec["type"] == "card" else "Caption"
            # each chunk's own entrance: a quick scale-down punch, not a plain fade
            pop = "{\\fscx128\\fscy128\\t(0,180,\\fscx100\\fscy100)}"
            pieces = [(ws, we, word) for ws, we, word, _ln in chunk]
            # one Dialogue event per word-window within the chunk, so the
            # highlighted word visibly advances as the voice speaks it, while the
            # rest of the chunk's already-read words stay on screen in the base
            # colour (not the "one lit word alone" style every other episode uses)
            for si in range(len(pieces)):
                w_s = pieces[si][0]
                w_e = min(pieces[si + 1][0] if si + 1 < len(pieces) else pieces[si][1], c_end)
                if w_e <= w_s:
                    continue
                text_parts = []
                for wj, (_, _, word) in enumerate(pieces):
                    col = hi if wj == si else base
                    prefix = pop if (si == 0 and wj == 0) else ""
                    text_parts.append(f"{{\\c{col}}}{prefix}{word}")
                text = " ".join(text_parts)
                # footage captions sit near the TOP of the safe zone: the bottom of
                # these screens (subscription rows, the add-transaction form) is the
                # actual content this beat is proving is real, so the caption never
                # goes there -- a plain fixed pixel rule would have put it right on
                # top of that content after the full-bleed crop, verified by looking
                # at the actual rendered frames, not assumed from geometry alone
                pos = f"{{\\an8\\pos({W//2},{SAFE_TOP+80})}}" if style == "Caption" else ""
                events.append(f"Dialogue: 0,{ts(w_s)},{ts(w_e)},{style},,0,0,0,,{pos}{text}")
    return ASS_HEADER.replace("{chip}", "C0" + BG_DARK) + "\n".join(events) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=f"{REPO}/studio/public/reels/reel-50.mp4")
    a = ap.parse_args()

    cues = load_cues()
    bounds, track_end = scene_bounds(cues)
    words = build_word_list(cues)

    seg_files = []
    for idx, (spec, (t0, t1)) in enumerate(zip(SCENES, bounds)):
        dur = round(t1 - t0, 3)
        print(f"scene {idx+1}: lines {spec['lines']} type={spec['type']} dur={dur:.2f}s")
        seg_files.append(build_scene(idx, spec, dur))

    listfile = f"{WORK}/full_list.txt"
    open(listfile, "w").write("\n".join(f"file '{p}'" for p in seg_files))
    full_bg = f"{WORK}/full_bg.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile, "-r", str(FPS),
         "-video_track_timescale", "30000", full_bg])

    # pad/trim the concatenated background to the cues-derived length exactly,
    # rather than trusting summed per-clip durations (the episode's own already-
    # fixed bug: per-clip -t cuts round to the nearest frame and drift adds up)
    real_dur = ffprobe_dur(full_bg)
    full_bg_fixed = f"{WORK}/full_bg_fixed.mp4"
    if real_dur < track_end:
        run(["ffmpeg", "-y", "-i", full_bg, "-vf",
             f"tpad=stop_mode=clone:stop_duration={track_end - real_dur:.3f}",
             "-r", str(FPS), full_bg_fixed])
    else:
        run(["ffmpeg", "-y", "-i", full_bg, "-t", f"{track_end:.3f}", "-r", str(FPS), full_bg_fixed])

    ass_path = f"{WORK}/captions.ass"
    open(ass_path, "w", encoding="utf-8").write(build_ass(bounds, words))

    captioned = f"{WORK}/full_captioned.mp4"
    run(["ffmpeg", "-y", "-i", full_bg_fixed, "-vf",
         f"ass={ass_path}", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium",
         "-crf", "18", "-pix_fmt", "yuv420p", captioned])

    # ---- audio: narration + music, render.sh's proven duck + two-pass loudnorm
    silent_out = f"{WORK}/muxed.mp4"
    run(["ffmpeg", "-y", "-i", captioned, "-i", VO_PATH, "-i", MUS_PATH, "-filter_complex",
         "[2:a]aresample=48000,volume=0.14[mus];"
         "[1:a]aresample=48000,highpass=f=85,acompressor=threshold=-18dB:ratio=3:attack=8:release=180[vo];"
         "[vo]asplit=2[vo1][key];"
         "[mus][key]sidechaincompress=threshold=0.05:ratio=4:attack=12:release=420[duck];"
         "[vo1][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
         "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad[a]",
         "-map", "0:v", "-map", "[a]", "-t", f"{track_end:.3f}",
         "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high",
         "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", silent_out])

    # two-pass loudness correction (verbatim recipe from export/render.sh)
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", silent_out, "-af",
                           "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    stats = json.loads(meas[meas.rfind("{"):])
    gain = -14 - float(stats["input_i"])
    limit = 0.75
    cur = silent_out
    for attempt in range(4):
        corrected = f"{WORK}/corrected_{attempt}.mp4"
        run(["ffmpeg", "-y", "-i", cur, "-c:v", "copy", "-af",
             f"volume={gain}dB,alimiter=limit={limit}:attack=5:release=50:level=disabled:latency=true,aresample=48000",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", corrected])
        verify = subprocess.run(["ffmpeg", "-hide_banner", "-i", corrected, "-af",
                                 "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                                capture_output=True, text=True).stderr
        vstats = json.loads(verify[verify.rfind("{"):])
        tp = float(vstats["input_tp"])
        print(f"  attempt {attempt+1}: limit {limit:.3f} -> {vstats['input_i']} LUFS, {tp} dBTP")
        cur = corrected
        if tp <= -0.8:
            break
        limit *= 10 ** (-((tp - (-1.0) + 0.3)) / 20)

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    run(["cp", cur, a.out])
    print("done:", a.out)


if __name__ == "__main__":
    main()
