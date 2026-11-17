#!/usr/bin/env bash
cd "$(dirname "$0")"
VOICE=voice/v10 WORDS=voice/words-v10.json python3 build10.py --render v10short 2>&1 | grep -E "rror|D="
N=v10short; cp out/narration-short.wav out/narration-$N.wav; cp cues-short.json cues-$N.json; cp hf/index.html out/index-$N.html
echo finished
