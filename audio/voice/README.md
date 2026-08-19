# The voice profile

David's voice, stored once. Every future episode is spoken from this profile —
no new recording, ever, unless the voice itself should change.

## Files

| File | What it is |
|---|---|
| `profile/reference.wav` | The stored voice. 18s, built from his six best-articulated lines |
| `profile/reference-raw.wav` | Same clips before cleanup, kept so the profile can be rebuilt |
| `profile/profile.json` | Which lines were used, and from which recording |
| `../build_voice.py` | Speaks any script in that voice |

## Speaking a new episode

```bash
# fit the narration into an existing video's caption slots — the cut doesn't move
python3 audio/build_voice.py --fit video/reel-02.html --out audio/voice/ep02.wav

# or lay out a fresh script and let the video be cut to it afterwards
python3 audio/build_voice.py --lines script.txt --out audio/voice/ep02.wav
```

Roughly six minutes of compute per minute of speech on this machine.

## How each line is verified

Generation is stochastic. An unlucky seed swallows a consonant — the first run
turned *"think harder"* into *"thing harder"*, which is exactly the kind of thing
nobody notices until it's published.

So every line is transcribed back and compared to what it was asked to say. If the
words don't match it regenerates with a new seed, up to `--retries`, and keeps the
closest take. The comparison ignores differences that aren't pronunciation —
"chat GPT" for "ChatGPT", a dropped possessive — so it only retries on real errors.

`--no-verify` skips it. Don't, for anything being published.

## How it measures up

| | His recording | The clone |
|---|---|---|
| Pitch (median f0) | 123.7 Hz | 125.7 Hz |
| Melodic range | 38 Hz | 56 Hz |
| Consonant band vs body | −27 dB | −16 dB |
| The S band (6–9k) | −27 dB | −18 dB |
| Words transcribed correctly | 92% confident | 92% confident, no errors |

The wider melodic range is the point: his read was flat because he was reading.
The clone carries his timbre with more natural intonation.

## Tuning

| Flag | Does what |
|---|---|
| `--exaggeration` | 0.3 flat · **0.45 default** · 0.7 animated |
| `--cfg` | Lower is looser and more natural. Default 0.45 |
| `--seed` | Changes the take. Same seed, same delivery |
| `--retries` | Attempts per line before accepting the closest. Default 3 |

## Rebuilding the profile

Worth doing if he records again with a better mic — everything downstream improves
at once, since every episode is generated from this one file.

1. Record 60–90 seconds, varied sentences, normal speaking pace.
2. Run the scoring in `git log` for `build the voice reference` to pick the cleanest lines.
3. Replace `profile/reference.wav`. Nothing else changes.

## Two things to know

**The output carries an inaudible AI watermark.** Chatterbox embeds one in everything
it generates, and so does every commercial cloning service. It doesn't affect how it
sounds. It does mean the audio is detectable as synthetic, which matters on platforms
that down-rank AI-generated media — the same risk flagged in the operating plan. His
own recorded voice carries no such mark. That is the real trade-off here, and it is
worth revisiting if reach ever looks suppressed.

**This voice belongs to him.** Don't point the profile at anyone else's recording.
