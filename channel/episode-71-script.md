# Episode 71 — "Improve the model for everyone" (script + voice PREPARED 16.10.2026, NOT built, NOT shipped)

**Status:** script and voice only. No picture yet: it needs David's own real iPhone screen recording of ChatGPT
(Settings > Data controls), same method as episode 70 (video 2 of the 10-video viral-format test, see `channel/experiments.md`).
Topic chosen by David from three options on 16.10.2026 ("if you think this is the next reel, prepare it").

## Product check (done 16.10.2026, WEB RESEARCH ONLY, NOT verified on a device)
OpenAI's help pages returned HTTP 403, so nothing below was read on an OpenAI page; the facts come from search snippets that quote
OpenAI's "Data Controls FAQ" (help.openai.com/en/articles/7730893) and from third-party guides.
- Label and path: Settings > Data controls > "Improve the model for everyone" — third-party only. **Confirm the exact label on David's phone before filming.**
- Off = new conversations are not used for training; it does not delete saved chats — snippet quoting the FAQ.
- Default: "on for Free and Plus" is third-party only; Pro conflicts; Belgium/EU default is UNCONFIRMED. **The script therefore never says the setting is on for the viewer; it says "may be" and "can".** The recording shows the switch state on David's own account.
- Temporary Chat: not saved, not used for training, deleted within 30 days — FAQ snippet (not used in this cut).
- NOT SAID, unconfirmed: whether past chats were already used; anything Belgium-specific; anything about Pro; that humans read chats; that OpenAI sells data.

## Hook research (two research agents, 16.10.2026) — thin, say so
No view counts could be read anywhere (TikTok/YouTube pages return only the site shell, Reddit blocked, no Instagram reel found). So **there is no
evidence which hook performs best**. What exists: recurring patterns by title/caption only — negative command ("Turn this OFF now"), "settings you
need to change right now", "by default your chats are used to train it", "most people never opened this". Claims we avoid because the agents found
no support: "sharing your secrets", "your chats are being read", "nothing is saved", "delete chats to remove it from training".
Own history (`hooks-guide.md`): 70 = negative command / direct address, so this one is NOT a negative command; 62 already used "Delete a ChatGPT chat..." (retention).
Chosen type: **Direct address / personal stakes, softened with "may"** — about the viewer's own last chat, not a number or a prohibition.

## Spoken lines (v3, built and gated 16.10.2026, 35.0s, ALL CHECKS PASSED; replaces v1 after David's feedback: boring delivery, weak hook, closing screens "jumping")
1. One switch in ChatGPT decides if your chats get used. (hook, white bar; screen: Data controls, switch ON)
2. Mine was on. (own beat, big text; the red ON tag appears on the real switch)
3. That means OpenAI, which runs it, can use them to train its AI.
4. Here's how to check your own.
5. Open the menu, top left. (slow zoom push on the button, continuing from line 4)
6. Press the gear at the bottom.
7. Open Data controls.
8. Find Improve model for everyone. (ON tag)
9. Switch it off if you don't want that. (the real flip; the tag turns green OFF at the flip)
10. Your voice chats have their own switch, just below it.
11. Send this to someone who uses ChatGPT.
12. The setup's in the link in bio. (locked)
13. Follow for the setup that actually works. (locked; no episode 72 is published yet, so no promise)
Hook choice: from a hook-ranking agent that read hooks-guide.md and the studio's own numbers. The only consistent winner pattern is a plain, checkable fact about a product the viewer uses in the first clause;
"Mine was on." adds the personal stake and is checkable on the first frame. NO evidence it beats other hooks (about 4 grid points per pattern, all 300-450 views, no shares). The runner-up for a Trial Reels A/B:
"ChatGPT can train on your chats. This switch stops it." (needs "stops it" softened to "stops future use").
Delivery: exaggeration 0.66 (hook 0.74, "Mine was on." 0.80, CTA 0.70) instead of 0.50, shorter lines, a beat before "Mine was on.". Measured on the final audio: pitch variation 3.6 -> 4.5 semitones (std), range about the same,
pace NOT faster. This is a measurement, not an ear test: if it sounds worse to David, his ear wins and the old setting (0.50) is in profile.json.
Visual: ON/OFF tags, a zoom push, one constant closing screen (the three last lines used to re-fade the same screen, which read as a jump).
Known weak spot left: about 3 s on the empty home screen before the menu.

## v4 (17.10.2026, 36.0s, ALL CHECKS PASSED; replaces v3 after David's feedback: boring start, wrong music, flat voice, stills instead of motion)
- Lines changed: 1 "One switch in ChatGPT controls if your chats get used!" ("decides" kept being swallowed), 2 "Mine was on!" (written "ON" the voice spelled it out), 8 "Tap Improve model for everyone." ("Find" was held too long), 9 ends with "!".
- Picture: real motion segments from the recording (menu opening, Data controls opening, the real switch flip) instead of held frames; red ON tag on the switch from the first second.
- Voice: exaggeration 0.78 (line 1 0.78, 2 0.90, 6 and 8 0.64, 9 0.85, 10 0.68, 11 0.80). Lines 6 and 8 were flagged as sounding Indian by the accent check at higher settings, so those two sit lower. Enthusiasm is still the reference voice's ceiling: only David's ear can say if it is enough.
- Music: mood 'bright', picked by the rotation from the library (the 54 new tracks are now in main). Different tracks were chosen in different runs; the shipped file used upbeat-energetic--lnplusmusic.
- 18.10.2026 fix after David's watch: the menu swipe was slow-motion (0.45s of source stretched over 2.4s); now plays at real speed (0.7s) during "check your own", and the empty home screen is no longer held. Same music track pinned (FORCE_TRACK). David's verdict: much better, enthusiasm improved, small voice glitches remain ("Mine was on").
- Process note: the cloud container is suspended when a turn ends, which kills background jobs; the voice loop and render only progress while a turn is active.

## Build facts and what the real recording showed (16.10.2026, two recordings; the 16.7s one, 13:09, was used)
- Real label: "Improve model for everyone" (not "Improve the model for everyone" as the third-party guides say). Text on screen: "Allow your content to be used to improve our models for you and other users. We take steps to protect your privacy."
- Both switches ("Improve model for everyone", "Include audio recordings") were ON on David's account before the recording: that is FACT for this one account only. The default for other accounts, plans and countries is still UNCONFIRMED and the video does not claim it.
- Accent #818CF8 (indigo), mood 'drive' (video-editing--alexmorgan.mp3, a real library track). The gate first refused 'urgent': same mood as episode 70, and it would have been the same track.
- Voice: 8 rounds of per-line seed rerolls until nothing was flagged; line 2 and 5 were reworded because they kept flagging.
- Privacy: raw recordings and the masked frames (channel/assets/ep71-screen, git-excluded) are NOT in git. Chat titles are blurred in the side menu; email and phone only appear in frames that are not used and were blurred anyway. Checked by eye twice on the final MP4 (contact sheets at 4 fps, plus a 4-frame crop of the side menu at full size); there is no OCR.
- Watched twice: both clean. One thing noticed and left: the switch flips right as "Switch it off" begins, which matches the narration.
- Not verified: OpenAI's help page (403). "New chats stay out of training" was NOT said in the final cut.

## What the recording must show (so the picture can follow the lines)
Home screen with the menu button; the open side menu (chat titles blurred in the finished video, like 70); Settings with the gear; the "Data controls" row; the
"Improve the model for everyone" row with its switch visible (on or off); ideally also Temporary Chat if David wants it added later. No face. Email/phone rows get blurred as in 70.

## Done / still open
Done: picture, captions, music, gate, setup guide (`/e/71`, English only), caption and YouTube text, design row.
Open: David posts it by hand after 70 (publish order [70, 71]); then reads Instagram Insights (views from non-followers, sends, saves, follows).
