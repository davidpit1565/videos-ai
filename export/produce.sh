#!/usr/bin/env bash
# The whole pipeline for one reel, unattended, from a build HTML to a checked file in
# the studio. Exists because running each stage by hand and waiting for a go-ahead
# between them is what was actually slow — not the TTS itself, which was already the
# genuine bottleneck (CPU-bound, no way around it) but ran one command at a time with
# a human in the loop for every step in between.
#
#   ./export/produce.sh <episode> <build.html> <duration> [accept_words] [bpm] [mood]
#
# <episode> e.g. "03" — used to name every intermediate file consistently.
# Requires the build's CUES array to already be final; this does not write scripts,
# it only turns a finished build into a checked, shipped file.
# <bpm> the music bed's tempo — pick it per episode, not a fixed default: a warning
# or exposé earns something more urgent (90-100), a calm walkthrough something
# lower (72-80). Default 82 if you don't have an opinion yet.
# <mood> neutral | urgent | bright — a different chord progression per mood, not just
# a different tempo on the same one. Every episode sounding the same was the bug;
# tempo alone did not fix it.
set -uo pipefail
cd "$(dirname "$0")/.."

EP="$1"; BUILD="$2"; DUR="$3"; ACCEPT="${4:-}"; BPM="${5:-82}"; MOOD="${6:-neutral}"
VO="audio/reel${EP}-narration.wav"
CUES="audio/reel${EP}-narration-cues.json"
VO_R="audio/reel${EP}-narration-r.wav"
CUES_R="audio/reel${EP}-narration-r-cues.json"
BUILD_T="video/reel-${EP}-timed.html"
BUILD_K="video/reel-${EP}-kar.html"
MUSIC="audio/reel${EP}-music.wav"
MP4="/tmp/reel-${EP}.mp4"
DEEP="/tmp/reel${EP}-deep.json"
GATE="/tmp/reel${EP}-gate.txt"

echo "=== [0/11] pronunciation lint"
# The other pipeline wrapper (make_reel.sh) ran this before generating anything;
# this one never did, and it is a free, seconds-long check that catches a whole
# class of "sounds soft/wrong" complaints (see audio/script_lint.py) before
# burning 90-100s per line on a script that needed a wording fix anyway.
python3 audio/script_lint.py --cues "$BUILD" || exit 1

echo "=== [1/11] voice"
if [ ! -f "$VO" ]; then
  python3 audio/build_voice.py --cues "$BUILD" --out "$VO" --exaggeration 0.50 --cfg 0.30 || exit 1
else
  echo "  $VO already exists, reusing"
fi

echo "=== [2/11] level repair"
# The same word list accepted at the final gate has to be accepted here too — this call
# runs the identical shipped-file check and can exit 1 on its own, before the pipeline
# ever reaches check.sh. reel-06 hit exactly this: --accept was wired to the gate only,
# so an already ear-approved word ("three") still failed the build at this earlier stage.
python3 audio/voice_doctor.py "$VO" --cues "$CUES" --repair "$VO_R" ${ACCEPT:+--accept "$ACCEPT"} || exit 1
cp "$CUES" "$CUES_R"

echo "=== [3/11] retime picture to natural pacing (0.9s closing tail)"
python3 export/retime.py "$BUILD" "$CUES_R" --out "$BUILD_T" --tail 0.9 --wav "$VO_R" || exit 1

echo "=== [4/11] word-level captions"
python3 audio/word_stamps.py "$VO_R" --out "$DEEP" || exit 1
python3 export/karaoke.py "$BUILD_T" "$DEEP" --words-cues "$CUES_R" --out "$BUILD_K" || exit 1

echo "=== [5/11] safe-area check"
node export/safe_check.js "$BUILD_K" --every 0.5 || exit 1

echo "=== [6/11] design variety check"
# "Never two episodes back to back in the same design" was a stated rule that nothing
# actually enforced — channel/used-designs.json tracked what shipped, but nothing
# compared a new build against it before rendering. Read straight from the build's own
# --brass/--ember CSS variables, same as the studio's /templates page does, not
# retyped by hand. Checked BEFORE the render/gate steps below so a repeat fails in
# seconds, not after minutes of rendering something that would get rejected anyway.
DESIGNS="channel/used-designs.json"
BRASS=$(grep -o -- '--brass:#[0-9A-Fa-f]\{6\}' "$BUILD_K" | head -1 | cut -d: -f2)
EMBER=$(grep -o -- '--ember:#[0-9A-Fa-f]\{6\}' "$BUILD_K" | head -1 | cut -d: -f2)
if [ -z "$BRASS" ] || [ -z "$EMBER" ]; then
  echo "  could not find --brass/--ember in $BUILD_K — skipping this check for this run"
else
  python3 - "$DESIGNS" "$EP" "$BRASS" "$EMBER" "$MOOD" <<'PYEOF' || exit 1
import json, sys
path, ep, brass, ember, mood = sys.argv[1:6]
try:
    with open(path) as f:
        designs = json.load(f)
except FileNotFoundError:
    designs = []
# Compare against the last SHIPPED episode other than this one — not designs[-1] raw.
# Re-running produce.sh for an episode that already shipped once (a re-render after a
# fix, for instance) finds its own row already appended at the end of the list, which
# made every rerun compare an episode's design against itself and always "repeat." This
# was a known bug worked around by hand each time (deleting the row before rerunning);
# fixed here instead of left as a manual step.
others = [d for d in designs if d["episode"] != int(ep)]
if others:
    last = others[-1]
    if last["brass"].lower() == brass.lower() and last["ember"].lower() == ember.lower():
        print(f"DESIGN REPEAT: episode {ep} would use the exact same brass/ember as "
              f"episode {last['episode']} ({brass}/{ember}). Change the palette before shipping.")
        sys.exit(1)
    if last.get("mood") and last["mood"] == mood:
        print(f"DESIGN REPEAT: episode {ep} would use the same music mood "
              f"('{mood}') as episode {last['episode']}. Pick a different --mood.")
        sys.exit(1)
print(f"  ok — {brass}/{ember}, mood '{mood}', distinct from episode {others[-1]['episode'] if others else 'none shipped yet'}")
PYEOF
fi

NEWDUR=$(python3 -c "
import re
html = open('$BUILD_K').read()
m = re.search(r'var DUR=([\d.]+)', html)
print(m.group(1) if m else '$DUR')
")
# Rotate the key by episode number so two episodes sharing a mood (a real, repeated
# complaint: reel-03/04/07 were all "urgent" back to back) still land in a different
# key, not the same track transposed by nothing. Five roots spread across the cycle.
KEY=$(python3 -c "
roots = [55.0, 49.0, 61.7, 65.4, 73.4]  # A1, G1, B1, C2, D2
try: ep = int(''.join(c for c in '$EP' if c.isdigit()) or 0)
except Exception: ep = 0
print(roots[ep % len(roots)])
")
echo "=== [7/11] music bed at ${NEWDUR}s, ${BPM} bpm, ${MOOD}, key ${KEY}Hz"
python3 audio/build_music.py "$NEWDUR" "$MUSIC" --bpm "$BPM" --mood "$MOOD" --key "$KEY" || exit 1

echo "=== [8/11] render"
FRAMES=1 ./export/render.sh "$BUILD_K" 1080 1920 "$NEWDUR" "$VO_R" "$MP4" "$MUSIC" || exit 1

echo "=== [9/11] gate"
ACCEPT_WORDS="$ACCEPT" ./export/check.sh "$BUILD_K" "$VO_R" "$MP4" 2>&1 | tee "$GATE"
PASSED=$(grep -c "ALL CHECKS PASSED" "$GATE" || true)

if [ "$PASSED" -eq 0 ]; then
  echo ""
  echo "GATE FAILED — not shipped. See $GATE"
  exit 1
fi

echo "=== [10/11] captions"
# A reel that ships without these publishes broken: the Instagram button posts with an
# empty caption (nothing stops it — it just goes out blank), and the YouTube button
# refuses outright because the title comes from line 1 of this file. This isn't a
# reminder, it's a hard stop — a passed gate used to be enough to call a reel done, and
# "done" kept shipping without them. Numbered separately from the gate itself: a video
# can pass every technical check and still not be postable.
CAP="channel/episode-${EP}-caption.txt"
YT="channel/episode-${EP}-youtube.txt"
MISSING=()
[ -s "$CAP" ] || MISSING+=("$CAP")
[ -s "$YT" ] || MISSING+=("$YT")
if [ "${#MISSING[@]}" -gt 0 ]; then
  echo ""
  echo "CAPTIONS MISSING — not shipped:"
  printf '  %s\n' "${MISSING[@]}"
  echo "Write them (real content grounded in this episode's script — see channel/episode-12-caption.txt for the format), then re-run."
  exit 1
fi

echo "=== [10b/11] setup guide"
# Same class of gap as the caption check above, for a different rule: every episode is
# supposed to ship with a full, exact setup path a viewer can actually follow on its own
# /e/N page (CLAUDE.md, standing since episode 21) — not just spoken narration. That was
# a stated rule with nothing checking it: an episode could ship with no
# studio/lib/articles.ts entry, or a thin placeholder steps list, and /e/N would render
# with no "The exact clicks" section at all. Checked here, not just written down.
python3 export/check_setup_guide.py "$EP" || exit 1

if [ -n "$BRASS" ] && [ -n "$EMBER" ]; then
  python3 - "$DESIGNS" "$EP" "$BRASS" "$EMBER" "$MOOD" <<'PYEOF'
import json, sys
path, ep, brass, ember, mood = sys.argv[1:6]
try:
    with open(path) as f:
        designs = json.load(f)
except FileNotFoundError:
    designs = []
designs = [d for d in designs if d["episode"] != int(ep)]  # re-running the same episode replaces its row
designs.append({"episode": int(ep), "brass": brass, "ember": ember, "mood": mood})
designs.sort(key=lambda d: d["episode"])
with open(path, "w") as f:
    json.dump(designs, f, indent=2)
    f.write("\n")
PYEOF
fi

cp "$MP4" "studio/public/reels/reel-${EP}.mp4"
cp "$GATE" "studio/public/reels/reel-${EP}.gate.txt"
# Filesystem mtime does not survive a git checkout reliably — Vercel's build showed
# 2018 for every reel because that's what the checkout left on disk, not when it
# actually shipped. This records the real moment, read by lib/reels.ts instead.
date -u +"%Y-%m-%dT%H:%M:%SZ" > "studio/public/reels/reel-${EP}.built-at.txt"
echo ""
echo "SHIPPED: studio/public/reels/reel-${EP}.mp4  (caption + youtube text present)"
