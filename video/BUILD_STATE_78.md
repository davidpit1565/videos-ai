# Episode 78 build state (26.10.2026)
Done: recording analysed (frames in channel/assets/ep78-screen), spec video/gen/ep78/spec.json -> video/reel-78.html (generator video/gen/ep75/gen.py), safe_check clean on placeholder timing, script/caption/youtube/article written.
Waiting on David: AI voice WAV clips for the 2 AI lines (see channel/episode-78-script.md lines 3 and 5): save as audio/voice/ep78/ai-1.wav, ai-2.wav (convert to 48 kHz mono 16-bit first), register the exact line text in audio/voice/profile/canonical-lines.json.
Then: ACCENT_SKIP=3,5 FORCE_TRACK=<track> ./export/produce.sh 78 video/reel-78.html 37 "" 90 <mood not 'neutral'> ; voice_quality; view frames; PR; merge; verify deploy; PushNotification; add 78 to PUBLISH_ORDER after 76.
Do not merge the branch before the reel exists (articles.ts already has /e/78).
