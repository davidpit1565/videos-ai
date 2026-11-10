#!/usr/bin/env bash
# Weekly cleanup (David, 10.11.2026: delete everything that is no longer relevant, every week).
# Default = dry run (lists what would go and the sizes). --apply deletes ONLY the safe, regenerable items below.
# NEVER touched: tracked files, audio/voice/profile, audio/music-library, channel/, studio/, plan/, ~/.cache/huggingface (voice models).
# --list-tracked prints big tracked build outputs of already-shipped episodes (candidates for a clean-up PR; never deleted by this script).
set -u
APPLY=0; LIST=0
for a in "$@"; do case "$a" in --apply) APPLY=1;; --list-tracked) LIST=1;; esac; done
cd "$(dirname "$0")/.." || exit 1
del() { # path
  [ -e "$1" ] || return 0
  s=$(du -sk "$1" 2>/dev/null | cut -f1)
  echo "  ${s}K  $1"
  TOTAL=$((TOTAL + s))
  [ "$APPLY" = 1 ] && rm -rf "$1"
}
TOTAL=0
echo "== safe regenerable items ($( [ $APPLY = 1 ] && echo APPLY || echo DRY RUN ))"
for d in video/*/node_modules video/*/out/work-* video/*/out/.r-*hf-transaction* tools/real-sfx-run tools/earshot/.venv; do for p in $d; do del "$p"; done; done
while IFS= read -r p; do del "$p"; done < <(find . -name __pycache__ -type d -not -path './node_modules/*' 2>/dev/null)
for p in /root/.cache/uv /root/.cache/pip; do del "$p"; done
for p in $(find /tmp/claude-*/ -maxdepth 4 -path '*scratchpad/refs*' -mtime +7 2>/dev/null); do del "$p"; done
echo "== total: $((TOTAL/1024)) MB $( [ $APPLY = 1 ] && echo freed || echo would be freed )"
df -h / | tail -1
if [ "$LIST" = 1 ]; then
  echo "== tracked files over 5 MB under video/ (clean-up PR candidates, only for episodes whose reel is already in studio/public/reels):"
  git ls-files -z video | xargs -0 -I{} sh -c 's=$(stat -c %s "{}" 2>/dev/null || echo 0); [ "$s" -gt 5242880 ] && echo "$s {}"' | sort -rn | head -60
fi
