#!/usr/bin/env bash
cd "$(dirname "$0")"
# render with spliced-b hook (passes voice gate); then build narration for the excited splice without rendering
VOICE=voice/v8b WORDS=voice/words-v8b.json python3 build8.py --render v8c 2>&1 | grep -E "rror|D="
cp out/narration-short.wav out/narration-v8c.wav; cp cues-short.json cues-v8c.json; cp hf/index.html out/index-v8c.html
VOICE=voice/v8a WORDS=voice/words-v8a.json python3 build8.py 2>&1 | grep -E "rror|D="
cp out/narration-short.wav out/narration-v8d.wav; cp cues-short.json cues-v8d.json
echo finished
