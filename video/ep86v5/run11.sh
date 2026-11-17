#!/usr/bin/env bash
cd "$(dirname "$0")"
VOICE=voice/v11 WORDS=voice/words-v11.json python3 build11.py --render v11short 2>&1 | grep -E "rror|D="
N=v11short; cp out/narration-short.wav out/narration-$N.wav; cp cues-short.json cues-$N.json; cp hf/index.html out/index-$N.html
echo finished
