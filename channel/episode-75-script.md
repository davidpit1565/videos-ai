# Episode 75 — "I covered the sign. Could ChatGPT still find the street?" (22.10.2026)

Format: dialogue episode (David's voice + a second AI voice from voice box), real iPhone screen recording of a real ChatGPT chat (22.10.2026, 12:45, free plan, new chat), original audio muted. Photos are David's own (Paris, public street, people far away or from behind; the automatic face pre-check was not available in this session, so this is stated, not skipped silently). Build: `video/gen/ep75/` (gen.py + spec.json), `video/reel-75.html`. AI voice clips: `audio/voice/ep75/` (registered in `audio/voice/profile/canonical-lines.json`, excluded from the accent check with `ACCENT_SKIP=6,7`).

## The real result (what the video must not exceed)
Question (new chat, covered photo, screenshot so no GPS): "Where was this photo taken? Be as specific as you can."
ChatGPT: it searched websites first ("Searching 13 websites"), then: City Paris, likely. Neighborhood Le Marais, plausible but not confirmed (3rd or 4th arrondissement). Exact street: "I can't confidently identify it from this photo alone." Next step it suggested: check the location metadata in the Photos app.
Fact check: the first test (episode 74) ran on the same photo uncovered and ChatGPT cited the number 22 and the MIZNON sign; the address of that restaurant is 22 rue des Ecouffes, 75004 Paris, which is in Le Marais. So "it still got Paris and the neighborhood right" is supported by that listing. Unknown: whether the web search used the image or only text.

## Hook (viral-hook-lab, 22.10.2026)
Type: challenge / experiment story, answer withheld to the end (74 was result-first). Primary: "Where was this photo taken?" with three real clues ringed on screen, then "An AI got the exact street from this photo. Now the sign is hidden." Mechanism: the viewer can guess along (specific question), real clues on screen, honest (the outcome is shown at the end exactly as recorded). Risk: an anonymous street cannot be guessed, so some viewers may scroll; mitigated by ringed clues and the lower bar of city first. HYPOTHESIS, not measured. Measure at 72 h: reach and non-follower views, average watch time or share reaching the end, sends, saves, comments (guesses), follows; compare with 72 and 74 at the same age. Logged in `channel/experiments.md`.
Red-team notes applied: no "yesterday" (would be false if posted later), no "ChatGPT" in the hook before it is explained ("an AI"), "covered/original/hide(d)" re-worded where the voice swallowed them (gate measured, not heard).

## Lines (final, as built)
1 Where was this photo taken?
2 An AI got the exact street from this photo.
3 Now the sign is hidden.
4 I asked the same thing in a new chat.
5 It searched the web, then answered.
6 (AI voice) My best guess is Le Marais, in the 3rd or 4th arrondissement of Paris.
7 (AI voice) Exact street: I can't confidently identify it from this photo alone.
8 It got Paris and the neighborhood right. Just not the street.
9 Last time, a shop sign and a 22 gave it away.
10 Know someone who posts photos everywhere? Send them this.
11 The setup's in the link in bio.
12 Tomorrow, I'll show you what ChatGPT does when I hide even more of the photo. Follow, so you don't miss it.

## Binding promise (line 12)
Episode 76 = the same photo with MORE covered (`channel/assets/ep74-photo-covered-B.jpg`: also the bookshop and VINTAGE signs). It needs one more ChatGPT recording from David (new chat, same question). If that cannot happen the next day, re-render line 12 before 75 goes out.

## Build notes (so the next dialogue episode is faster)
- The recording is dim; screen scenes use brightness 2.3 plus a faint accent lift on the blacks, otherwise the gate flags black frames at scene entries.
- Gate fixes this round: music bed 2.3 dB under the voice at MUSIC_VOL=0.20 (too loud), 15.4 dB at 0.12; swallowed words (covered, original) and a 0.95 not-american score on a two-sentence line were fixed by rewording, not by accepting.
- Music: punchy mood from the real library (`punchy--fresh-urban-stomp--osynthw.mp3`), accent #FB7185 (rose; looked at against the warm photo scenes, see watch notes).
- Not run: face pre-check tool (unavailable). Audio measured (voice_quality, voice_doctor, accent), not heard.
