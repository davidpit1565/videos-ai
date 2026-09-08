#!/usr/bin/env bash
# Restart-safe wrapper for produce.sh: if the sandbox VM kills the pipeline process
# mid-run (a real, recurring problem in this environment — see SUNDAY.md), this
# relaunches it. Safe to relaunch blindly because build_voice.py now caches each
# line's finished take to audio/.voice-cache/<episode>/ the moment it's produced
# (see build_voice.py), so a restart only re-does the one line that was in flight,
# not the whole episode.
#
#   ./export/watchdog.sh <episode> <build.html> <duration> [accept_words] [bpm] [mood]
#
# Same arguments as produce.sh. Run it with nohup + disown so it survives the
# calling shell exiting:
#   nohup ./export/watchdog.sh 27 video/reel-27.html 47.35 "" 80 suspense \
#     > /tmp/watchdog27.log 2>&1 &
#   disown
set -uo pipefail
cd "$(dirname "$0")/.."

EP="$1"; BUILD="$2"; DUR="$3"; ACCEPT="${4:-}"; BPM="${5:-82}"; MOOD="${6:-neutral}"
LOG_DIR="/tmp/produce-${EP}-logs"
mkdir -p "$LOG_DIR"
MAX_RESTARTS=30
n=0

shipped() {
  [ -f "studio/public/reels/reel-${EP}.mp4" ] && [ -f "studio/public/reels/reel-${EP}.gate.txt" ] \
    && grep -q "ALL CHECKS PASSED" "studio/public/reels/reel-${EP}.gate.txt" 2>/dev/null
}

echo "$(date -Is) watchdog started for episode ${EP}" >> "$LOG_DIR/watchdog.log"
while true; do
  if shipped; then
    echo "$(date -Is) SHIPPED — watchdog exiting" >> "$LOG_DIR/watchdog.log"
    exit 0
  fi
  if ! pgrep -f "produce.sh ${EP} " > /dev/null; then
    n=$((n+1))
    if [ "$n" -gt "$MAX_RESTARTS" ]; then
      echo "$(date -Is) GIVING UP after $MAX_RESTARTS restarts — needs a human look at $LOG_DIR/run$n.log" >> "$LOG_DIR/watchdog.log"
      exit 1
    fi
    echo "$(date -Is) produce.sh not running and not shipped — restarting (run$n)" >> "$LOG_DIR/watchdog.log"
    nohup ./export/produce.sh "$EP" "$BUILD" "$DUR" "$ACCEPT" "$BPM" "$MOOD" \
      > "$LOG_DIR/run$n.log" 2>&1 &
    disown
  fi
  sleep 45
done
