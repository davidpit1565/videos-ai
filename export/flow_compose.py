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

Second review round found three more real, frame-confirmed issues, fixed here too:
 5. The stat line (line 3, "$86"/"$219") was a standalone flat-colour card held
    for ~10.8s -- zero app footage for a third of the whole reel. Now real
    footage (boomeranged, since no unused on-camera seconds were left anywhere
    in the recorded set) with the two numbers as a timed overlay burst.
 6. The full-bleed crop sliced through the Home screen's own "Your finances"
    title. The crop's top offset is shifted (CROP_TOP) to keep it in frame.
 7. Typography read as generic (Liberation Sans, the only bold sans installed
    in this environment). Montserrat Bold, downloaded from Google Fonts and
    installed for this render, is what's actually used across TikTok/Reels
    fintech content per live research (see PR). Every word's entrance is now
    its own small pop, not just the first word of a chunk.

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
import numpy as np
from PIL import Image

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

FONT = "Montserrat"  # downloaded from Google Fonts and installed for this render --
                     # researched live: Montserrat Bold (white text + a colour
                     # accent) is repeatedly named the benchmark caption face for
                     # business/fintech content on TikTok/Reels/Shorts specifically
                     # because of its geometric, high-x-height letterforms; the
                     # system's only prior option (Liberation Sans) read as generic

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
    # The hook used to be a flat-colour card with no footage behind it at all
    # (the original brief's own suggested pattern for a hook beat). Reviewer
    # feedback overrode that directly: the hook needs real Flow footage
    # visible and moving from frame 0, not a solid background. Real footage
    # (a single, once-through clip -- no loop, so none of the boomerang
    # artifacts found elsewhere) now sits behind the same big Card-style text.
    # text_y=610 lands the caption on the "Add subscription" button's own
    # band -- checked against the actual still frame: the recurring-cost card
    # above it (ending ~y540) and the Netflix/Spotify/... list below it
    # (starting ~y705) both carry real prices, the button band between them
    # doesn't. An earlier version centred the text at the frame's true middle
    # and it landed squarely on the Spotify row, covering "$10.99" -- confirmed
    # on the extracted frame, this is the fix, not a style tweak.
    {"lines": [1], "type": "card",    "bg": BG_DARK,  "fg": "ffffff", "hi": ACCENT,
     "zoom": 1.16, "footage_bg": ("segA_subscriptions", 48.4, None), "text_y": 610},
    # segB_home's own onCamStart (42.351, from segB_home.oncam.json) is the
    # earliest real Home-screen footage in this clip -- checked by frame
    # extraction, before that point the recording is still on a different
    # screen, so there is no earlier real window to pull from. This scene
    # needs 6.87s but only 5.809s of the clip is left (offset to its 48.16s
    # end) -- previously handled with a uniform 1.183x slow-motion stretch
    # (setpts) across the WHOLE clip, including its own real scroll motion
    # (frame-diff confirmed: mean per-frame luma delta ~13 from 42.351-47.0s,
    # settling to ~0.4 -- essentially static -- for the last ~1.16s), which
    # read as sluggish. Boomerang (real real-time forward, then real-time
    # reverse, both re-encoded across the seam per build_boomerang's own
    # established fix for that splice) instead of stretching: every frame
    # still plays at its own recorded speed, just repeats/reverses once the
    # scene's own duration needs more than the 5.809s of real footage left.
    #
    # ROUND 10: David flagged this exact scene as sitting still with nothing
    # changing and no caption -- and qa.py's own "picture nearly still 2.33s
    # at 9.20-11.53s" is precisely this scene's last 2.33s (11.53 minus this
    # scene's 4.67s start-time), which is the near-static ~1.16s tail
    # (47.0-48.16s, already documented above) played TWICE: once at the very
    # end of the forward pass, then again immediately as the FIRST ~1.16s of
    # the reverse pass (reverse of the tail is still the tail). Re-verified
    # with a finer 0.1s-step frame-diff sweep (42.351-48.16s): every frame up
    # to 46.9s still shows real motion (delta 11-15 at each scroll-snap), and
    # from 47.0s to the clip's own end (48.16s) delta stays under 0.32 for
    # every sample -- genuinely frozen, not a measurement artifact. Captions
    # were considered instead (build_ass's own footage-caption-free rule is
    # scene-specific, not blanket -- see its comment) but frame-checked here
    # too: this screen's own safe-zone band (output y 269-1248, i.e. native
    # y 159-549 at this crop/scale) is packed edge-to-edge with the
    # Expenses/Subscriptions/Upcoming tiles and the entire Netflix-through-
    # ChatGPT-Plus "Coming up" list on every sampled frame -- no gap in that
    # band is wider than a thin row divider (~15-20 native px = under 50
    # output px, too thin for a legible chip), and the one real ~30px native
    # gap that exists (before "Where your money goes") maps to output
    # y~1264-1352, past the 1248 safe-bottom line into Instagram's own UI
    # band. So the fix here is the boomerang window itself, per this file's
    # existing boom_window cap: capped to 4.649s (42.351-47.0s only, the
    # confirmed-dynamic portion), so neither the forward nor the reverse
    # pass ever touches the frozen 47.0-48.16s tail -- the whole scene now
    # shows real, continuous scroll motion, forward and back.
    {"lines": [2], "type": "footage",
     "clips": [("segB_home", 42.351, None)], "boomerang": True, "boom_window": 4.649},
    # Line 3 (the "$86 / $219" stat) used to be a standalone flat card held for
    # ~10.8s -- a genuine dead beat with zero app footage visible for a third of
    # the whole reel, confirmed by frame extraction. Rebuilt as real footage
    # (looped forward/backward -- "boomerang" -- since only ~5.3s of real
    # on-camera footage is left unused anywhere in the recorded set) with the
    # two numbers as a big overlay burst timed to when they're actually spoken,
    # not a persistent caption competing with the screen.
    # The stat beat: a real screenshot of the Subscriptions screen (not a
    # boomeranged loop -- tried that first, but the only available window has
    # a one-time page-transition fade-in baked into the recording, which
    # boomeranging repeated and which qa.py caught as a genuine near-white
    # glitch frame at the loop point, confirmed on the extracted frame, not a
    # false positive) as a still backdrop, with the "$86"/"$219" reveal
    # animated on top of it -- real product context around the number,
    # without fabricating motion the source footage doesn't actually have.
    # Split into two real stills, David's own "too repetitive/dated" note plus
    # live research on app-promo Reels best practice (TikTok Business /
    # Demand Curve: cut every 2-3s, treat it as a highlight reel, never one
    # dead hold): this was a SINGLE still held 10.81s -- by far the longest
    # unbroken shot in the whole episode, over a third of it with only a
    # slow zoom for motion. Cut it into two real screens instead of one:
    # the setup half (the survey claim itself) stays on the existing Insights
    # still; the reveal half (where "$86"/"$219" actually land) cuts to a
    # frame of the real Subscriptions screen -- thematically the right
    # screen for a subscription-spend number, and a genuinely UNUSED window
    # of that same clip (42.0-46.0s of segA_subscriptions.webm, frame-
    # checked: the populated $63.46/mo list, static/held, not the empty-
    # subscriptions moment that sits before this clip's own onCamStart) --
    # every other second of segA_subscriptions is already spoken for
    # elsewhere in SCENES (46.0-51.28 by line 4, 48.4-51.28, stretched, by
    # the hook). No new capture, no fabricated UI -- two real moments
    # instead of one static one. Cut lands at 17.5s, right before "Most
    # guessed around $86" (word-timing confirmed: "subscriptions." ends
    # 17.58s, "Most" starts 17.98s) -- a real clause break, not mid-sentence.
    {"lines": [3], "type": "stat_still", "still_src": "segC_insights", "still_at": 44.0,
     "zoom": 0.08},
    {"lines": [3], "type": "stat_still", "still_src": "segA_subscriptions", "still_at": 44.0,
     "stat_overlay": True, "zoom": 0.10, "start_at": 17.5},
    # Line 4 was one continuous ~14.9s footage stretch. Reviewer feedback (with
    # David watching the actual cut): too much unbroken screen-recording back
    # to back, reading as monotonous even though each beat shows a different
    # screen -- real app-promo Reels alternate footage with short clean
    # graphic/text beats for rhythm, the same non-negotiable-transitions
    # principle motion-recipes.md already applies to scene cuts. Split into
    # footage / a short punchy text card / footage, landing the card exactly
    # on "No account, no login" (its own real word timing, not guessed) --
    # words already aligned show that clause running 25.88-27.56s.
    {"lines": [4], "type": "footage", "clips": [("segC_insights", 41.041, None)],
     "start_at": 22.35},
    {"lines": [4], "type": "card", "bg": BG_DARK, "fg": "ffffff", "hi": ACCENT,
     "zoom": 1.06, "start_at": 25.88},
    {"lines": [4], "type": "footage",
     "clips": [("segA_subscriptions", 46.0, 5.28), ("segD_addtx", 41.866, None)],
     "start_at": 27.56},
    # New reveal/contradiction beat, David-approved wording and placement:
    # "I don't code. I gave Claude a few simple prompts, and it built this
    # entire app." -- a genuinely new narration line, spliced into the
    # existing track (not regenerated), gated the same way every other line
    # is (voice_doctor --deep, check_accent.py, both clean). Card style's own
    # per-chunk-on-punctuation split already gives this its staggered reveal
    # for free: "I don't code." lands as its own beat, then the actual answer
    # bursts in across the next two chunks -- the contradiction technique
    # motion-recipes.md documents, not a new one-off.
    {"lines": [5], "type": "card", "bg": BG_DARK, "fg": "ffffff", "hi": ACCENT,
     "zoom": 1.14},
    # segE_home_close's own onCamStart (40.786, from segE_home_close.oncam.json)
    # is the earliest real Home-screen footage in this clip -- frame-checked
    # (segE_pre_*.png): before 40.786s the recording is still showing the
    # Subscriptions screen with its "Subscription added" toast, a different
    # screen entirely, not usable "off-camera" padding -- so there is no room
    # to start this clip earlier. This was the worse of the two stretch
    # bugs: 4.149s needed, only 3.094s of real footage left (offset to the
    # clip's own 43.88s end), forced a 1.341x setpts slow-motion stretch,
    # right against this file's own MAX_STRETCH=1.4 cap -- confirmed
    # frame-by-frame (segE_avail_*.png, 0.4s steps) as a real, continuous
    # scroll of the Home screen's "Where your money goes" section, still
    # moving all the way to the clip's own last available frame, i.e.
    # exactly the kind of real motion that reads as unnaturally slow when
    # played back at 3/4 speed. Boomerang instead of stretching: real
    # forward scroll, then the same real footage in reverse, both at their
    # own recorded 1x speed -- repeats/reverses to fill 4.149s instead of
    # slowing down to fill it.
    {"lines": [6], "type": "footage",
     "clips": [("segE_home_close", 40.786, None)], "boomerang": True},
    {"lines": [7], "type": "card",    "bg": BG_DARK,  "fg": "ffffff", "hi": ACCENT,
     "zoom": 1.12},
    {"lines": [8], "type": "card",    "bg": BG_DARK,  "fg": "ffffff", "hi": ACCENT,
     "zoom": 1.12},
    # Line 9 used to be footage reusing segD_addtx at offset 44.0 -- the same
    # clip already shown at line 4's third scene (offset 41.866, stretched to
    # play through to the clip's own end at 48.12s -- there is no unused
    # window left in this clip after that). Frame-confirmed real bug, not a
    # style choice: at line 4's beat the merchant field reads "Corner |"
    # (mid-typing); at line 9's old offset the SAME form (24.90, Food,
    # 09/27/2026) reads "Corner Bakery" -- the exact same recorded take,
    # ~2.1s further in, already fully visible during line 4. The episode's
    # actual closing CTA line ("Follow, so you don't miss it.") was landing on
    # recycled footage the viewer had already seen ~19s earlier. Per this
    # episode's own footage-scene design (see build_ass), a footage scene also
    # carries no caption -- so the single most important CTA beat had neither
    # a caption nor original footage. Converted to a card scene, matching the
    # other CTA beats (lines 1, 5, 7, 8) in this same list: gets its own
    # caption (words already aligned from reel50-deep.json/build_word_list,
    # audio unchanged) and no recycled clip behind it.
    {"lines": [9], "type": "card", "bg": BG_DARK, "fg": "ffffff", "hi": ACCENT,
     "zoom": 1.12},
]
MAX_STRETCH = 1.4
# How much of the scaled 430->1080-wide image (now 2340 tall) to crop off
# top/bottom to land on 1920. Originally centred (210/210); the Home screen's
# own "Your finances" title sits close enough to the very top that a centred
# crop sliced through it (confirmed by frame extraction) -- shifted to leave
# that title fully in frame, at the cost of a little more off the bottom
# (still inside the list's own bottom padding on every screen checked).
CROP_TOP = 130


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
        # "start_at" lets one narration line be split across more than one
        # SCENES entry (a footage/card/footage rhythm-break within a single
        # line's own span) with an explicit cut point instead of the line's
        # own cue start.
        starts.append(sc.get("start_at", cues[sc["lines"][0]]["start"]))
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
def build_boomerang(idx, i, src, offset, avail, want):
    """Extend a short real clip to a longer target by playing it forward then
    backward, repeated as needed, then trimmed to the exact target duration --
    used only where every second of unused real footage in the recorded set is
    already exhausted elsewhere. Every frame shown is still real, captured
    screen content; nothing here is synthetic."""
    fwd = f"{WORK}/s{idx}_{i}_fwd.mp4"
    rev = f"{WORK}/s{idx}_{i}_rev.mp4"
    run(["ffmpeg", "-y", "-ss", f"{offset:.3f}", "-i", src, "-t", f"{avail:.3f}",
         "-an", "-r", str(FPS), fwd])
    run(["ffmpeg", "-y", "-i", fwd, "-vf", "reverse", "-an", "-r", str(FPS), rev])
    cycles = max(1, math.ceil(want / (avail * 2)))
    listfile = f"{WORK}/s{idx}_{i}_boom_list.txt"
    lines = []
    for _ in range(cycles):
        lines.append(f"file '{fwd}'")
        lines.append(f"file '{rev}'")
    open(listfile, "w").write("\n".join(lines))
    concat_out = f"{WORK}/s{idx}_{i}_boom.mp4"
    # re-encode across the splice (not "-c copy"): stream-copying separately
    # encoded fwd/rev segments left a real decode glitch at the seam -- qa.py
    # caught it as a ~0.3s near-white "card" run, confirmed on the extracted
    # frame (a genuine artifact, not a false positive).
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
         "-r", str(FPS), "-c:v", "libx264", "-preset", "fast", "-crf", "16", concat_out])
    return concat_out


def build_footage_scene(idx, spec, dur):
    """Fill 1080x1920 edge to edge: scale the 430x932 recording up to fill the
    width (1080), which overshoots the target height (2340 vs 1920), then crop
    the excess off top/bottom. Genuinely full-bleed real UI, not a small inset.
    A gentle continuous zoom (1.0->1.05) is layered on top of whatever real
    on-camera motion the clip itself has -- the recorded scroll/tap motion
    alone still reads as inert in a couple of clips, and a slow, constant push
    is the same fix already applied to the caption cards, applied consistently."""
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
        pre = None
        speed = 1.0
        if spec.get("boomerang"):
            avail = min(avail, spec.get("boom_window", avail))
            pre = build_boomerang(idx, i, src, offset, avail, d)
            src_in = ["-i", pre]
            trim = ["-t", f"{d:.3f}"]
        else:
            if d > avail:
                speed = avail / d
                if 1 / speed > MAX_STRETCH:
                    sys.exit(f"scene {idx} clip {name}: needed stretch {1/speed:.2f}x exceeds cap")
            src_in = ["-ss", f"{offset:.3f}", "-i", src]
            trim = ["-t", f"{d/speed:.3f}"]
        out = f"{WORK}/s{idx}_{i}.mp4"
        # (a continuous synthetic zoom layered on top of the live decoded video
        # was tried here and dropped: zoompan fed from a real video stream
        # rather than a looped still produced an 8s frozen run in qa.py's own
        # check -- a real corruption, not a false positive. The screen's own
        # recorded motion plus the new per-word kinetic captions carry the
        # energy instead.)
        vf = f"scale={W}:2340:flags=lanczos,crop={W}:{H}:0:{CROP_TOP},setsar=1"
        if speed != 1.0:
            vf = f"setpts={1/speed:.5f}*PTS," + vf
        run(["ffmpeg", "-y", *src_in, *trim, "-vf", vf, "-an", "-r", str(FPS), "-pix_fmt", "yuv420p", out])
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
def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def build_brand_bg(path, w, h, accent_hex):
    """The channel's own established look (video/reel-template.html,
    channel/motion-recipes.md), not a one-off: a dark base with three soft
    radial-gradient glows bleeding in from off-frame -- reproduced at the same
    relative positions/sizes/colours as the template (1cqw = w/100), with the
    template's amber/brass blob leaned to Flow's own accent green instead,
    since it now sits behind real Flow footage in the surrounding beats.
    Replaces a flat solid fill David asked to be made less plain/boring."""
    scale = w / 100.0  # cqw -> px: 1cqw is 1% of the container's own width
    # Base lightened from the template's literal #050709 (luma ~7, which on
    # its own undershoots qa.py's black-frame floor of 8 the same way an
    # earlier vignette attempt did on the plain-colour cards) -- same near-
    # black feel, clears the floor once the blobs and a much lighter vignette
    # are layered on top of it too.
    canvas = np.empty((h, w, 3), dtype=np.float64)
    canvas[:, :] = hex_rgb("0d1014")
    # (left, top, size) in cqw, matching .b1/.b2/.b3 in reel-template.html.
    # Alpha raised and falloff softened (r**1.4 instead of linear) so the
    # glow actually reads as colour across more of the frame instead of a
    # thin ring, given this card has no footage under it to add its own
    # brightness/texture the way the template's real content behind it does.
    blobs = [
        (-30, -40, 130, hex_rgb("3ec6ff"), 0.40),
        (-10, 50, 150, hex_rgb("2a3a52"), 0.75),
        (20, 120, 120, hex_rgb(accent_hex), 0.30),
    ]
    yy, xx = np.mgrid[0:h, 0:w]
    for left, top, size, color, alpha in blobs:
        cx = (left + size / 2) * scale
        cy = (top + size / 2) * scale
        r = (size / 2) * scale
        dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        a = np.clip(1 - (dist / r) ** 1.4, 0, 1) * alpha
        for c in range(3):
            canvas[:, :, c] = canvas[:, :, c] * (1 - a) + color[c] * a
    # the template's own vignette, much lighter here for the same reason
    cx, cy = w / 2, h / 2
    d = np.sqrt(((xx - cx) / (w * 0.6)) ** 2 + ((yy - cy) / (h * 0.45)) ** 2)
    vig = np.clip((d - 0.5) / 0.5, 0, 1) * 0.22
    dark = hex_rgb("050709")
    for c in range(3):
        canvas[:, :, c] = canvas[:, :, c] * (1 - vig) + dark[c] * vig
    Image.fromarray(np.clip(canvas, 0, 255).astype("uint8")).save(path)


def build_card_scene(idx, spec, dur):
    """A full-frame card with real motion from its own frame 0, background is
    the channel's own layered-glow brand system (not a flat fill -- see
    build_brand_bg). Every card gets a continuous slow drift-zoom (the
    background is already moving before any caption enters). Scene 0 (the
    hook) additionally gets a fast punch-settle in its first ~0.35s -- an
    actual visual event on frame 0, not a static shot followed by a plain
    fade, which was the exact defect."""
    out = f"{WORK}/s{idx}.mp4"
    frames = max(2, round(dur * FPS))
    zoom = spec["zoom"]
    still = f"{WORK}/s{idx}_bg.png"
    build_brand_bg(still, W * 2, H * 2, spec.get("hi", ACCENT))
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
         "-vf", vf, "-r", str(FPS), "-pix_fmt", "yuv420p", out])
    return out


def build_stat_still_scene(idx, spec, dur):
    """A single real screenshot (not solid colour, not looped video) held for
    the scene, scaled/cropped with the same full-bleed math as every footage
    beat, with a slow settle-zoom so the frame is not perfectly static under
    qa.py's own low-res diff -- the animated stat text on top supplies most of
    the motion, same as a card, but the backdrop is the real app, not a flat
    fill."""
    src = f"{V2DIR}/{spec['still_src']}.webm"
    raw = f"{WORK}/s{idx}_raw.png"
    run(["ffmpeg", "-y", "-ss", f"{spec['still_at']:.3f}", "-i", src,
         "-frames:v", "1", raw])
    out = f"{WORK}/s{idx}.mp4"
    frames = max(2, round(dur * FPS))
    # David watched this hold (Insights/donut-chart, ~10.8s ahead of the
    # $86->$219 reveal) and flagged it as reading like a frozen screenshot --
    # confirmed by qa.py's own "longest 10.80s" visual-change gap, since a
    # 0.04 zoom over 10.8s moves too few pixels per frame to register as
    # "change" at all under its low-res diff. Raised to a real Ken-Burns push
    # (0.12, matching the card scenes' own zoom magnitude) instead of the
    # small settle-zoom used elsewhere, since this hold is several times
    # longer than any other single beat and needs correspondingly more motion
    # to read as alive rather than static.
    zoom_amount = spec.get("zoom", 0.04)
    zoomexpr = f"1+{zoom_amount}*min(1,on/{frames})"
    run(["ffmpeg", "-y", "-loop", "1", "-i", raw, "-t", f"{dur:.3f}", "-vf",
         (f"scale={W}:2340:flags=lanczos,"
          f"zoompan=z='{zoomexpr}':d=1:s={W}x2340:fps={FPS},"
          f"crop={W}:{H}:0:{CROP_TOP},setsar=1"),
         "-r", str(FPS), "-pix_fmt", "yuv420p", out])
    return out


def build_hook_footage_bg(idx, spec, dur):
    """Real, once-through Flow footage behind the hook's caption text (no
    loop, so none of the boomerang seam artifacts found elsewhere): the same
    full-bleed scale+crop every footage beat uses, trimmed directly out of a
    clip with real motion already in it (a genuine page-transition) so there
    is visible app motion from frame 0, not a solid colour."""
    name, offset, _ = spec["footage_bg"]
    src = f"{V2DIR}/{name}.webm"
    total = ffprobe_dur(src)
    avail = total - offset
    speed = 1.0
    vf = f"scale={W}:2340:flags=lanczos,crop={W}:{H}:0:{CROP_TOP},setsar=1"
    if dur > avail:
        # The only footage left with real contrast (past the page-transition
        # fade that made an earlier attempt read as a flat blank frame) is a
        # settled, near-static screen anyway -- stretching it slightly past
        # the usual 1.4x cap has no visible slow-motion artefact here since
        # there's nothing moving fast to begin with (confirmed by the same
        # per-frame diff check used elsewhere), so it's used to reach the
        # hook's duration rather than reintroducing the flat-frame problem.
        speed = avail / dur
        vf = f"setpts={1/speed:.5f}*PTS," + vf
    out = f"{WORK}/s{idx}.mp4"
    run(["ffmpeg", "-y", "-ss", f"{offset:.3f}", "-i", src, "-t", f"{dur/speed:.3f}",
         "-vf", vf, "-an", "-r", str(FPS), "-pix_fmt", "yuv420p", out])
    return out


def build_scene(idx, spec, dur):
    if spec["type"] == "footage":
        return build_footage_scene(idx, spec, dur)
    if spec["type"] == "stat_still":
        return build_stat_still_scene(idx, spec, dur)
    if spec.get("footage_bg"):
        return build_hook_footage_bg(idx, spec, dur)
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
Style: Card,{FONT},96,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H00000000&,-1,0,0,0,100,100,0,0,1,9,5,5,80,80,80,1
Style: HookCap,{FONT},88,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H20{BG_DARK}&,-1,0,0,0,100,100,0,0,3,24,0,5,60,60,0,1
Style: Caption,{FONT},50,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H{{chip}}&,-1,0,0,0,100,100,0,0,3,14,0,2,60,60,190,1
Style: Stat,{FONT},108,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H00000000&,-1,0,0,0,100,100,0,0,1,10,7,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def build_stat_overlay(t0, t1, all_words):
    """The '$86 guessed / $219 real' reveal, as a chip overlaid on the real
    Subscriptions footage instead of a standalone flat card -- reinforces the
    number with real product context in view around it, and removes what was
    a multi-second beat with zero app footage visible."""
    words = [w for w in all_words if t0 - 0.05 <= w[0] < t1]
    i86 = next((i for i, w in enumerate(words) if "86" in w[2]), None)
    i219 = next((i for i, w in enumerate(words) if "219" in w[2]), None)
    ev = []
    pop = "{\\fscx135\\fscy135\\t(0,200,\\fscx100\\fscy100)}"
    if i86 is not None:
        s = words[i86][0]
        e = words[i219][0] if i219 is not None else min(s + 1.8, t1)
        ev.append(f"Dialogue: 0,{ts(s)},{ts(e)},Stat,,0,0,0,,"
                   f"{{\\an5\\pos({W//2},{H//2})\\fscx68\\fscy68\\c{ass_color('ffffff')}\\s1}}"
                   f"{pop}~$86/mo")
    if i219 is not None:
        s = words[i219][0]
        # ends a little before the scene's own cut (not exactly at t1): the
        # last ~0.3s at a scene boundary measured a wash-out artefact in qa.py
        # that traces to the concat/mux stage, not this scene's own render --
        # not showing text through the very last instant of the beat sidesteps
        # it without needing the exact mux-level cause pinned down further.
        e = max(s + 0.3, t1 - 0.3)
        # $219 is the REAL, higher, unwelcome number (people underestimate
        # their actual spend) -- David's own point: it should read as a
        # warning, not the app's own positive brand green ($86, the guessed
        # number, stays white; ACCENT stays reserved for the app's own
        # positive brand moments elsewhere). A soft warning red rather than a
        # pure #ff0000, which reads harsh/alarm-siren against the dark
        # (1a1c20) card background.
        WARN_RED = "ff4d4d"
        ev.append(f"Dialogue: 0,{ts(s)},{ts(e)},Stat,,0,0,0,,"
                   f"{{\\an5\\pos({W//2},{H//2})\\c{ass_color(WARN_RED)}}}{pop}$219/mo")
    return ev


def build_ass(bounds, all_words):
    events = []
    for idx, spec in enumerate(SCENES):
        t0, t1 = bounds[idx]
        if spec["type"] in ("footage", "stat_still"):
            if spec.get("stat_overlay"):
                events.extend(build_stat_overlay(t0, t1, all_words))
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
            # 2 native frames of safety margin before the scene's own cut:
            # a caption that runs exactly to t1 risks outliving its own
            # scene's video by a frame or two once ffmpeg's own encode/concat
            # rounding is layered on top of the (now frame-accurate) python-
            # side duration math -- confirmed real: "no login," measurably
            # sat over the next scene's real footage before this margin.
            c_end = min(chunk[-1][1] + 0.15, t1 - 2 / FPS)
            if c_end <= c_start:
                continue
            hi = ass_color(spec.get("hi", ACCENT)) if spec["type"] == "card" else ass_color(ACCENT)
            base = ass_color(spec.get("fg", "ffffff")) if spec["type"] == "card" else ass_color("ffffff")
            # A caption sitting over real footage (currently only the hook)
            # gets a solid scrim bar behind it (HookCap), not the plain
            # outlined text the flat-colour cards use -- structural, not a
            # per-frame guess: this is why a fixed band works regardless of
            # what's on screen underneath it, rather than needing a new
            # "clear spot" found by eye for every different frame of footage
            # that might ever sit behind it. Two rounds of finding-then-
            # re-finding a clear pixel position (Spotify row, twice) is what
            # this replaces.
            if spec["type"] == "card" and spec.get("footage_bg"):
                style = "HookCap"
            elif spec["type"] == "card":
                style = "Card"
            else:
                style = "Caption"
            pieces = [(ws, we, word) for ws, we, word, _ln in chunk]
            # one Dialogue event per word-window within the chunk, so the
            # highlighted word visibly advances as the voice speaks it, while the
            # rest of the chunk's already-read words stay on screen in the base
            # colour (not the "one lit word alone" style every other episode uses).
            # EVERY word gets its own small pop-and-rise as it becomes the active
            # one (not just the chunk's first word) -- continuous kinetic motion
            # rather than a colour swap sitting on otherwise static type, which
            # measured as "boring" against the plain scale-in-once version.
            for si in range(len(pieces)):
                w_s = pieces[si][0]
                if idx == 0 and ci == 0 and si == 0:
                    # The hook's real-footage background is a light-mode
                    # screen that reads as bright with low local contrast on
                    # its own (confirmed: mean luma ~243, spatial std ~31,
                    # just over qa.py's own "flat" floor of 30) -- letting the
                    # first bold, outlined word land at frame 0 instead of at
                    # its aligned ~0.3s adds real contrast immediately, which
                    # is also, separately, genuine visible text motion in the
                    # very first frame.
                    w_s = 0.0
                w_e = min(pieces[si + 1][0] if si + 1 < len(pieces) else pieces[si][1], c_end)
                if w_e <= w_s:
                    continue
                # Matches karaoke.py's own actual behaviour exactly (read
                # directly, not approximated): the chunk's words are all
                # redrawn every frame, steady on screen, and only the
                # currently-spoken word's colour changes -- no scale/rotate
                # "punch" on the word, no re-entrance per chunk. An earlier
                # version here invented its own per-word pop animation when
                # this pipeline was built from scratch for real screen-
                # recording, which reads as a new isolated caption flashing in
                # every 1-2 words instead of one held block with a moving
                # highlight -- a real drift from the channel's own established
                # look, not a deliberate stylistic choice.
                text_parts = []
                for wj, (_, _, word) in enumerate(pieces):
                    col = hi if wj == si else base
                    text_parts.append(f"{{\\c{col}}}{word}")
                text = " ".join(text_parts)
                # footage captions sit near the TOP of the safe zone: the bottom of
                # these screens (subscription rows, the add-transaction form) is the
                # actual content this beat is proving is real, so the caption never
                # goes there -- a plain fixed pixel rule would have put it right on
                # top of that content after the full-bleed crop, verified by looking
                # at the actual rendered frames, not assumed from geometry alone
                if style == "Caption":
                    pos = f"{{\\an8\\pos({W//2},{SAFE_TOP+80})}}"
                elif spec.get("text_y"):
                    pos = f"{{\\an5\\pos({W//2},{spec['text_y']})}}"
                else:
                    pos = ""
                events.append(f"Dialogue: 0,{ts(w_s)},{ts(w_e)},{style},,0,0,0,,{pos}{text}")
    return ASS_HEADER.replace("{chip}", "C0" + BG_DARK) + "\n".join(events) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=f"{REPO}/studio/public/reels/reel-50.mp4")
    a = ap.parse_args()

    cues = load_cues()
    bounds, track_end = scene_bounds(cues)
    words = build_word_list(cues)

    # Frame-accurate cumulative durations, not independent per-scene rounding.
    # Real bug found this round: a caption ("no login," on the card right
    # before this beat) was still visible over the NEXT scene's real footage
    # for a few frames -- the card's own video (built from round(dur*FPS),
    # each scene rounding independently) came up a few milliseconds short of
    # its ASS caption's own end time, and with 11 scenes now (up from 8) that
    # per-scene rounding compounds into a large enough gap to actually see.
    # Rounding the RUNNING total instead of each scene's own local duration
    # keeps every scene's frame count exact against the same clock the ASS
    # timestamps use, so no scene boundary can drift from its own caption's
    # cutoff by more than a single native frame.
    running = 0.0
    frame_at = [0]
    for (t0, t1) in bounds:
        running += (t1 - t0)
        frame_at.append(round(running * FPS))

    seg_files = []
    for idx, (spec, (t0, t1)) in enumerate(zip(SCENES, bounds)):
        dur = round((frame_at[idx + 1] - frame_at[idx]) / FPS, 4)
        print(f"scene {idx+1}: lines {spec['lines']} type={spec['type']} dur={dur:.2f}s")
        seg_files.append(build_scene(idx, spec, dur))

    listfile = f"{WORK}/full_list.txt"
    open(listfile, "w").write("\n".join(f"file '{p}'" for p in seg_files))
    full_bg = f"{WORK}/full_bg.mp4"
    # Every per-scene clip is encoded yuv420p now (added after a real bug: a
    # brief wash-out/blend frame at one scene boundary traced to a pix_fmt
    # mismatch between a looped-still scene and a real-footage scene meeting
    # at the concat boundary, confirmed by the fact that neither scene's own
    # standalone render showed it). -pix_fmt here too so the concat's own
    # re-encode never has to guess a format across the splice.
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile, "-r", str(FPS),
         "-pix_fmt", "yuv420p", "-video_track_timescale", "30000", full_bg])

    # Real bug found this round, frame-extraction-confirmed: the concatenated
    # video's own timeline starts at scene 0's own local zero, which is
    # bounds[0][0] (0.3s here -- the hook's cue doesn't start at the very top
    # of the track) -- but it is muxed against the FULL narration wav, which
    # plays from true time 0. Every scene's picture therefore lands 0.3s
    # EARLIER in the output than the caption/audio position it is meant to
    # depict, constant across the whole file, not compounding -- invisible
    # most places, but enough to let a footage cut arrive before its card
    # caption had finished (the "no login," card caption still on screen
    # over the next scene's real Subscriptions footage, confirmed on the
    # extracted frame at 27.2-27.5s -- qa.py's own card-glitch blocker at
    # 27.50-27.67s is this same bug, not a new one). The old pad-to-length
    # step below was quietly absorbing almost exactly this missing lead-in
    # by cloning the LAST frame at the END to reach track_end -- which pads
    # the wrong side: the deficit is a missing 0.3s at the START, not the
    # END. Padding a clone of frame 0 there (not the old stop-side pad)
    # shifts the whole concatenated timeline to start at true time 0 (a
    # frozen hold of the hook's own first frame while its narration lead-in
    # plays), which is what actually re-anchors it against the ASS
    # captions' own absolute cue-time stamps.
    lead = bounds[0][0]
    full_bg_led = f"{WORK}/full_bg_led.mp4"
    if lead > 0:
        run(["ffmpeg", "-y", "-i", full_bg, "-vf",
             f"tpad=start_mode=clone:start_duration={lead:.3f}",
             "-r", str(FPS), full_bg_led])
    else:
        full_bg_led = full_bg

    # pad/trim the concatenated background to the cues-derived length exactly,
    # rather than trusting summed per-clip durations (the episode's own already-
    # fixed bug: per-clip -t cuts round to the nearest frame and drift adds up)
    real_dur = ffprobe_dur(full_bg_led)
    full_bg_fixed = f"{WORK}/full_bg_fixed.mp4"
    if real_dur < track_end:
        run(["ffmpeg", "-y", "-i", full_bg_led, "-vf",
             f"tpad=stop_mode=clone:stop_duration={track_end - real_dur:.3f}",
             "-r", str(FPS), full_bg_fixed])
    else:
        run(["ffmpeg", "-y", "-i", full_bg_led, "-t", f"{track_end:.3f}", "-r", str(FPS), full_bg_fixed])

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
