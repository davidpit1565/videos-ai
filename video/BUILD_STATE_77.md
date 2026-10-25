# Episode 77 build state (25.10.2026): SHIPPED. Merged in PR #480; reel-77.gate.txt ends with ALL CHECKS PASSED. The text below is the earlier mid-build note, kept for history only; it is no longer current.

# Episode 77 build state (25.10.2026, 17:55 UTC) — STOPPED, NOT SHIPPED
Gate result: only failure = accent check on lines 1 and 2 ("Your phone can write a map pin into your photos!", "It is saved as coordinates inside the file."). Rewordings tried: 3 rounds for line 1, 3 for line 2; classifier keeps saying "indian" 0.94-0.99. All other checks passed (safe area, render qa, loudness -14 LUFS, music bed, setup guide not reached).
Done: sources verified, script, video/reel-77.html (video/gen/ep77/gen.py), article in studio/lib/articles.ts, captions, publish-order, experiments/memory entries, voice cache for 6 of 8 lines.
Not done: lines 1-2 re-roll (try a hook/second line with different words, e.g. start with a different sound), re-run gate, voice_quality.py, watch twice, setup-guide check, merge, deploy verify.
Resume: FORCE_TRACK=bright--feel-good-music--paulyudin.mp3 ./export/produce.sh 77 video/reel-77.html 38 "" 90 confident  (after: pip install "av==15.1.0"; symlink /opt/pw-browsers/chromium-1194/chrome-linux/chrome -> chromium-1243/chrome-linux64/chrome). Edit lines in video/gen/ep77/gen.py then python3 video/gen/ep77/gen.py; delete audio/reel77-narration* before re-running.
NOTE: studio/lib/publish-order.ts already lists 77 and articles.ts has /e/77: do not merge this branch until the reel exists.
