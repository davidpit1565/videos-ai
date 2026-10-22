# Episode 75 — "I covered the sign. Could ChatGPT still find the street?" (22.10.2026)

Format: dialogue episode (David's voice + a second AI voice from voice box), real iPhone screen recording of a real ChatGPT chat (22.10.2026, 12:45, free plan, new chat), original audio muted. Photos are David's own (Paris, public street, people far away or from behind; the automatic face pre-check was not available in this session, so this is stated, not skipped silently). Build: `video/gen/ep75/` (gen.py + spec.json), `video/reel-75.html`. AI voice clips: `audio/voice/ep75/` (registered in `audio/voice/profile/canonical-lines.json`, excluded from the accent check with `ACCENT_SKIP=6,7`).

## The real result (what the video must not exceed)
Question (new chat, covered photo, screenshot so no GPS): "Where was this photo taken? Be as specific as you can."
ChatGPT: it searched websites first ("Searching 13 websites"), then: City Paris, likely. Neighborhood Le Marais, plausible but not confirmed (3rd or 4th arrondissement). Exact street: "I can't confidently identify it from this photo alone." Next step it suggested: check the location metadata in the Photos app.
Fact check: the first test (episode 74) ran on the same photo uncovered and ChatGPT cited the number 22 and the MIZNON sign; the address of that restaurant is 22 rue des Ecouffes, 75004 Paris, which is in Le Marais. So "it still got Paris and the neighborhood right" is supported by that listing. Unknown: whether the web search used the image or only text.

## Hook (viral-hook-lab + Arena, 22.10.2026)
David rejected the first drafts ("really bad, I would skip it"), so the hook was chosen by the Arena skill (16 competitors, 4 rounds, ~90 sub-agent calls; every solution attacked, defended and scored by judges against the channel's own hook rules; the winner also beat the rejected draft in a blind final check, 80.5 to 17.5: these are model judges' scores, not audience data).
Winner (type: personal question + viewer challenge; 74 was result-first): spoken "Anyone can see your street photo. What do they know?" then "Here's mine. Guess the city." First frame: David's Paris photo with the sign and the 22 already blurred, ringed. Why: it puts the viewer's own post in beat 1, the challenge is winnable (the city), and the real ending actually grades it (Paris likely, Le Marais plausible). No hook line claims the AI found or failed anything. HYPOTHESIS, not measured. Measure at 72 h: reach and non-follower views, share reaching the end, sends, saves, comments (city guesses), follows; compare with 72 and 74 at the same age.
Runner-ups kept for later: "Which city is this? Two clues are gone. Now an AI gets the same question." and "Open your camera roll. Find a street photo. Now see what an AI makes of mine."
Known limits: the on-screen text is the spoken line (the build highlights spoken words), not the separate text the Arena proposed; the first frame shows blurred areas, not black bars.
Red-team notes applied: no "yesterday", "an AI" before ChatGPT is explained, words the voice swallows (covered, original, hide, number, asked, neighborhood) replaced, not accepted.

## Lines (final, as built)
1 Anyone can see your street photo. What do they know?
2 Here's mine. Guess the city.
3 In my last video, an AI got the exact street from this photo.
4 Now the sign and the 22 are blurred.
5 Same question, in a new chat.
6 It searched the web, then answered.
7 (AI voice) My best guess is Le Marais, in the 3rd or 4th arrondissement of Paris.
8 (AI voice) Exact street: I can't confidently identify it from this photo alone.
9 It got the city and the area right. Just not the street.
10 Know someone who posts photos everywhere? Send them this.
11 The setup's in the link in bio.
12 Tomorrow, I'll show you what ChatGPT does when I hide even more of the photo. Follow, so you don't miss it.
(AI voice lines are locked clips, excluded from the accent check with ACCENT_SKIP=7,8.)

## Binding promise (line 12)
Episode 76 = the same photo with MORE covered (`channel/assets/ep74-photo-covered-B.jpg`: also the bookshop and VINTAGE signs). It needs one more ChatGPT recording from David (new chat, same question). If that cannot happen the next day, re-render line 12 before 75 goes out.

## Build notes (so the next dialogue episode is faster)
- The recording is dim; screen scenes use brightness 2.3 plus a faint accent lift on the blacks, otherwise the gate flags black frames at scene entries.
- Gate fixes this round: music bed 2.3 dB under the voice at MUSIC_VOL=0.20 (too loud), 15.4 dB at 0.12; swallowed words (covered, original) and a 0.95 not-american score on a two-sentence line were fixed by rewording, not by accepting.
- Music: `bright--feel-good-music--paulyudin.mp3` (14% of the bed under 150 Hz, MUSIC_VOL 0.11, bed -13.9 dB under the voice in 300-3500 Hz; the first pick, a punchy track, was 68% sub-bass and failed `voice_quality.py` for phone speakers), accent #FB7185 (rose; looked at against the warm photo scenes).
- Not run: face pre-check tool (unavailable). Audio measured (voice_quality, voice_doctor, accent), not heard.
