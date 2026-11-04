---
name: send-with-sound
description: >-
  Use every time you send David a video or an audio-carrying file in the chat
  (a reel, a voice test, a music option, a render). He follows from his phone,
  the chat does not play sound there, and downloading each file is a chore. Trigger
  words: "send the video", "here is the reel", "voice test", "music options",
  "שלח לי", "שמע", "אני לא שומע", "אין סאונד". Also use before SendUserFile on any .mp4/.mov/.wav.
---

# Send it so he can hear it, without downloading

**Rule (David, 4.11.2026):** he cannot hear sound in the chat on his phone and should never have to download a file to listen. Every time a video (or any file with sound) goes to him, send it in a form he can play from the chat.

## Steps
1. Run `export/phone_preview.sh <video.mp4>`. It writes next to the source: `*-phone.mp4` (720x1280, small, sound on), `*-sound.m4a` and `*-sound.mp3` (audio only, a normal audio file the phone's player plays).
2. Send with SendUserFile, in one call: the `-phone.mp4` first, then the `-sound.m4a`. Caption in Hebrew says plainly which file is the audio-only one.
3. Because the inline video is silent for him, ALSO publish a private Artifact page (a `<video controls>`, a "Play with sound" button that sets `muted=false`, and an `<audio controls>` with the mp3) and send the link. Published files must be .mp4/.mp3 (not .m4a). If he says the m4a does not play, send the `-sound.mp3` next time. If neither plays, publish a private Artifact page with a `<video controls>` and an `<audio controls>` (small files only; 15 MB per file limit) and send the link. Write down which one worked below, and stop trying the others.
4. Never claim he heard it. Audio is measured by tools; his ear is the test (CLAUDE.md voice rules).
5. The full-quality file still goes to the repo/studio; the phone copies are previews, never what ships.

## What works for him (UNKNOWN until he says; update this list)
- Inline video in chat (SendUserFile): no sound on his phone, he can only see it (reported 4.11.2026, twice). Do not rely on it.
- Artifact page with a video and an audio player: published 4.11.2026 (Artifact tool; `.m4a` is NOT a served type there, use `.mp3`; video at 720p is about 4 MB). Result pending his answer.
- m4a / mp3 as a file in chat: not tested yet.
- Artifact page with player: not tested yet.
