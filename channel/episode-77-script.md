# Episode 77: "Your phone can write a map pin into your photos" (25.10.2026)

Why this episode: episode 76 (the promised "even more hidden" ChatGPT test) needs a real recording that does not exist yet. 77 is a different, honest episode. No ChatGPT test, no screen recording, no ChatGPT answer, no AI voice other than David's cloned voice. Photos are reused faceless stock from channel/assets (ep59, ep57, ep67). Logos: Apple (ep69 file), ChatGPT (ep70 file), icon only.

## Verified live on 25.10.2026 (primary sources)
- Apple, "Manage location metadata in Photos": with Location Services on for the Camera, coordinates are embedded in each photo and video; people you share with may be able to access the location metadata and learn where it was taken. Steps: Share > Options > Location off; Adjust Info > Adjust Location > No Location; Settings > Privacy & Security > Location Services > Camera > Never. https://support.apple.com/guide/personal-safety/manage-location-metadata-in-photos-ips0d7a5df82/web
- OpenAI, "ChatGPT Image Inputs FAQ" (updated about 19.10.2026): "The model doesn't process original file names or metadata, and images are resized before analysis." https://help.openai.com/en/articles/8400551-chatgpt-image-inputs-faq
- NOT claimed: what any app does with the file before it reaches the model; whether a given app strips the location on send; that ChatGPT can or cannot find a place from the picture alone (the earlier episodes 74/75 are cited only on the /e/77 page as "my earlier tests").

## Spoken lines (8, about 37 s)
1. Your phone can write a map pin into your photos! (hook: surprise statement, "a thing your phone does to you"; hypothesis, not measured)
2. It is saved as coordinates inside the file.
3. Send one, and the person who gets it may see the exact place.
4. OpenAI says ChatGPT does not process a photo's metadata.
5. It only looks at the picture itself. And a picture can still give a place away.
6. To keep it off, tap the send arrow, then Options, and switch Location off.
7. The setup's in the link in bio.
8. Next, I'll show you what ChatGPT does when I hide even more of the photo. Follow, so you get the full story.

Line 5 "a picture can still give a place away" rests on episodes 74 and 75 (own tests, one photo, one try each), stated as a limit on /e/77.

## Measured vs not heard
Measured by tools: script_lint, voice_doctor, accent check, safe_check, qa.py, music bed check, voice_quality (see build log). The audio was measured, not heard by any person. The picture was checked by sampled frames, not by a person watching it.

## Honest compromises
- Voice lines were reworded after the accent check flagged them (lines 1 and 2 twice; "hidden data", "taken" and "map pin inside" dropped).
- Built under a same-day deadline: 8 scenes of reused stock photos with on-screen text, no new photo sourcing.
- Chromium path in the container differed from the hardcoded one in export/safe_check.js and frames.js: a symlink was made in /opt, no gate file was edited.
