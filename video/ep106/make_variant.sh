#!/usr/bin/env bash
# make_variant.sh "<hook line>" <tag> ["<frame0 lines separated by |>"] [accent_line_index]
# New opening line only -> new finished version out/ep106-<tag>.mp4 from the cached body voice.  See VARIANTS.md.
# Steps: (1) hook voice: 3 seeds under flock (one TTS at a time), (2) Whisper text check + accent score picks the take,
# (3) stitch with cached body takes (voice/body-picks.json), re-time, (4) words, build, render, bed, mix, gate (run106.sh).
set -u; cd /home/user/videos-ai/video/ep106
HOOK=${1:?hook line}; TAG=${2:?tag (fresh name, e.g. V6)}; F0=${3:-}; ACC=${4:-}
[ -e out/ep106-$TAG.mp4 ] && { echo "out/ep106-$TAG.mp4 exists: use a fresh tag"; exit 2; }
if [ -z "$F0" ]; then   # default frame 0: the hook split into at most 3 short lines of its first words
  F0=$(python3 - "$HOOK" <<'PY'
import sys,re
w=re.sub(r"[.!]","",sys.argv[1]).upper().split(); n=len(w); k=min(3,n); out=[]; i=0
for j in range(k):
    c=-(-(n-i)//(k-j)); out.append(" ".join(w[i:i+c])); i+=c
print("|".join(out))
PY
)
fi
echo "hook: $HOOK | frame0: $F0"
python3 ../../audio/script_lint.py --file <(echo "$HOOK") | tail -4
echo "$HOOK" > voice/pl/H-$TAG.txt
voice/hook_take.sh $TAG "${SEEDS:-11 22 33}"
HOOKWAV=$(/opt/v311/bin/python voice/pickhook.py $TAG | tail -1); echo "picked: $HOOKWAV"
[ -f "$HOOKWAV" ] || { echo "no hook take matched its text: re-roll with SEEDS='44 55 66' EXAH=0.70"; exit 1; }
HOOKWAV=$HOOKWAV /opt/v311/bin/python voice/stitch.py $TAG | head -1
# accent classifier is context sensitive: re-choose flagged body takes inside this stitch (cached takes only), then re-stitch
/opt/v311/bin/python voice/fixaccent.py $TAG $HOOKWAV $PWD/voice/pl/H-$TAG.txt 2>&1 | grep -E "round|line|CHANGED" 
[ -f voice/picks-$TAG.json ] && PICKS=$PWD/voice/picks-$TAG.json HOOKWAV=$HOOKWAV /opt/v311/bin/python voice/stitch.py $TAG | head -1
./run106.sh $TAG "$F0" $ACC
