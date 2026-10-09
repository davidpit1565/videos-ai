# Episode 63 — Is the AI chat you use one of the risky ones?

Built 8.10.2026 (David approved the script the same night). Episode 62's last line promises
a ranking of AI chats by privacy risk — this is that episode (binding). Final line points at
episode 64 (what Microsoft's Copilot does with your chats) — flowing format, no "Tomorrow:"
label (CLAUDE.md, 6.10.2026).

## Topic choice (from the data, not picked fresh)

- Promised on air by episode 62. Same family as the strongest recent episodes ("something is
  already happening to your data"), and it has a real viewer action (the ChatGPT training switch).
- Not a repeat: 60 was Meta ads, 61 Gemini reviewers, 62 ChatGPT deleted-chat retention — this
  one compares many chats on one scale instead of going deep on one.

## Product / claims verified live (8.10.2026)

- Incogni's own write-up, "Gen AI and LLM Data Privacy Ranking 2026" (blog.incogni.com/gen-ai-llm-privacy-ranking-2026):
  13 platforms scored on 11 criteria in three groups (what happens to user data, how transparent
  the platform is, what data is collected and shared). Mistral's Vibe (formerly Le Chat) and ChatGPT
  scored lowest risk; Microsoft Copilot, Meta AI and Moonshot's Kimi scored the highest risk.
- OpenAI's help center, "Data controls in ChatGPT" (help.openai.com/en/articles/7730893): web:
  account menu > Settings > Data controls > "Improve the model for everyone" > turn off > Done;
  phone: sidebar > profile icon > Settings > Data controls > turn off the same setting. Turning it off
  means new conversations are not used to train OpenAI models; they can still appear in chat history.
- **UNCONFIRMED / not said in the video:** exact per-platform scores (not read; only the order of the
  two ends is claimed). One secondary article placed Meta AI and DeepSeek at the bottom — it conflicts
  with the other sources and is not used. Older Incogni studies (9 platforms) ranked differently — not used.
- **The honest caveats, spoken in line 6:** the ranking scores what each company writes in its own policy,
  not what it actually does; and Incogni sells data-removal services (a commercial interest).

## Hook rules check

- Hook: "Is the AI chat you use one of the risky ones?"
- Type: Question / curiosity gap (62 was The Specific Number, 61 Shock, 60 Stakes, 58 Direct Address).
- Understandable from second one: "AI chat" is plain; line 2 names the company, what it checked, and examples.
- Feel-it-in-3-seconds: it asks about the chat the viewer is using right now.
- Delivery note (David, 8.10.2026): the voice must grab in the first fraction of a second — hard onset,
  energetic, no lead-in silence. The hook take is picked for onset energy, not only for clean endings.

## Spoken script (plain language)

1. Is the AI chat you use one of the risky ones?
2. A company called Incogni checked 13 AI chats, like ChatGPT, Copilot and Meta AI, on how they use your data.
3. It scored 11 things, like what data they collect, who gets it, and how open they are about it.
4. Mistral's Vibe scored safest, and ChatGPT came second. Copilot, Meta AI and Kimi got the highest risk scores.
5. (merged into scene 4 — same spoken words)
6. But it only scores what each company writes in its own policy, and Incogni sells data removal.
7. In ChatGPT, open Settings, then Data controls, and switch off Improve the model for everyone.
8. Show this to someone who uses Copilot every day.
9. The setup's in the link in bio. (locked)
10. Tomorrow, I'll show you what Microsoft's Copilot does with your chats. Follow, so you get the full story.

(Wording notes: "three" avoided on purpose — his voice bursts on it; "Show this to" instead of "Send this to"
— two speech models heard "Send" as "Fend" in episode 61.)

## Binding promise

Line 10 promises episode 64 tomorrow: what Microsoft's Copilot does with your chats. The Copilot privacy
pages must be read live before 64 is written. If 64 changes or does not go out the next day, re-render
line 10 before 63 goes out.

## Photos / design

Faceless Unsplash photos, new files `channel/assets/ep63-scene-*.jpg`. Logos (icon only, no caption under
them): Incogni, ChatGPT, Copilot, Meta, Mistral, Kimi — real marks sourced from official/brand/Wikimedia
pages, never redrawn. Accent: `#A78BFA` (not used in the last 7 days). Mood: confident (62 was urgent).

## Voice settings — to rebuild the same narration elsewhere (9.10.2026)

The narration .wav files are not in git; this is what produced the candidate render
(`channel/episode-63-candidate.mp4`):

- `python3 audio/build_voice.py --cues video/reel-63.html --out audio/reel63-narration.wav --exaggeration 0.50 --cfg 0.30 --prosody-rolls 6 --line-seeds "1:4080,2:3097,3:5114,4:1131,5:4148,6:4165,7:4182,9:4216"`
- Line 8 ("The setup's in the link in bio.") is the locked canonical clip (`audio/voice/profile/canonical-lines.json`), no seed.
- Lead-in before the first line: 0.08 s (`LEAD` in `audio/build_voice.py`, changed from 0.30 on 8.10.2026).
- Pipeline: `./export/produce.sh 63 video/reel-63.html 50 "model,risky,company,scored,about" 90 confident`
  (scene times in `video/reel-63.html` were fitted to this narration: last scene `data-out="49"`, `DUR=49.0`).
- Line 3 was re-rolled alone (seed 5114) to clear "scored"; the other seeds are from the 5th optimizer round.

## Gate result — NOT SHIPPED

`check.sh` failed on **one thing only: the accent heuristic**, which flags lines 2 ("A company called Incogni...")
and 6 ("In ChatGPT, open Settings...") as less like his reference voice (not-american 0.30 and 0.39, file median
0.06). It is a heuristic; his ear decides. Everything else passed: safe area (8 px past the top line, within
tolerance), -14.0 LUFS, peak -3.0 dBFS, no frozen picture over 4 s, first frame carries picture, music bed 15 dB
under the voice. One warning: picture nearly still 3.1 s at 12.7-15.9 s (scene C, magnifier photo).
The words `model`, `risky`, `company`, `scored`, `about` were passed to `--accept` because they sit within
0.004 s per syllable of the "swallowed" threshold — this was NOT an ear approval by David; he has not listened yet.
Because the gate failed, nothing was copied to `studio/public/reels/`.
Speech-recognition transcript of the render matches the script word for word.

Next: David listens. If lines 2/6 are fine -> re-run `check.sh` with `ACCEPT_WORDS` as above and `--accept` for the
accent lines (or lower the accent flag by ear), finish `produce.sh` steps 10-11, delete the candidate mp4 and draft mp3
from the branch, merge to main. If a line is wrong -> re-roll only that line (seed change, others locked).
