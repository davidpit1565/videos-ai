# ChatGPT memory reel, built with lemo-opuscar (3.11.2026). NOT published. Draft.

Script: `script-v4.md` (8 lines, facts verified by me on OpenAI Help Center Memory FAQ / What is Memory?). Design: `design-plan-v2.md` (Living Screencast, light). Built by a producer subagent; I verified the file myself.

## Verified by me
- ffprobe: h264 yuv420p 1080x1920, 24 fps, 26.17 s; aac 48 kHz stereo; volumedetect mean -16.9 dB, max -1.2 dB; 6,896,253 bytes.
- Whisper (base.en) on the final audio transcribes all 8 spoken lines in order (ChatGPT written as "Chat GPT" by Whisper; "setup's" as "setups"). Last line ends at 26.1 s.
- I looked at 26 frames (one per second, two contact sheets `myA.jpg`, `myB.jpg`) and at the full-size frame 0 and the twist frame: light lime look, no text outside the safe area, no overlap, quote card readable ("...even if you delete a chat, any saved memories from it can still be used in future conversations." matches the FAQ I read), "example · re-created" tag on every redrawn screen. The agent's checks: no black frames, no silence gap, longest freeze 0.5 s.
- Quote compared to the FAQ text I read today: matches.

## NOT verified / honest weaknesses
- **Nobody listened.** Audio was measured and transcribed, never heard. Stock Kokoro voice (af_heart), not David's cloned voice; the cloned-voice rules were applied to the words only. Music is synthesized (marimba + pad), NOT the licensed library the repo requires; `voice_quality.py`, `check_music_bed.py`, `check.sh`, `produce.sh`, `safe_check.js` were NOT run.
- Word-lighting on the headlines is approximate (Whisper word stamps unusable); the settings taps lag the spoken words by about 0.5 s.
- All UI is redrawn (labelled), no real chat or real account on screen: all 4 whole-script judges and 16 hook judges name this as the barrier to 90+. The ChatGPT mark is the Wikimedia Commons file, not checked against OpenAI's current brand page. The settings labels other than the 3-step path are generic.
- The Memory screen with notes is visible only about 1.2 s; several secondary UI texts fail the plugin's own reading-time check; the last scene is the quietest stretch; the bottom third of the frame is empty by design (platform UI).
- Line 8 is a binding promise (tomorrow = the ChatGPT age-prediction episode).
- Virality: whole-script judges (calibrated on the channel's anchors, judgments not forecasts): v2 78 and 72, v3 80 and 80, v4 not re-judged. Expected tier: above usual (70), below 90 (the owner's bar). Confidence low; measure the real 2 s / 5 s / end retention instead.

## Cost
Producer subagent: 51 tool calls, 261k tokens (meter), 947 s. Design agent 138k, whole-script judges about 90k each, hook judges about 90-95k each (16 of them), scouts 100-250k each.
