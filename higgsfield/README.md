# higgsfield/ — talking-head ad clips via the Higgsfield API

Wraps Higgsfield's "Speak v2" endpoint (the same feature shown in the
`talecomlaunch` AI-ad reel that prompted this) to generate a talking-head
clip from a portrait image + narration audio, without touching Higgsfield's
consumer web app.

## Setup (one time)

```bash
pip install -r higgsfield/requirements.txt
cp higgsfield/.env.example higgsfield/.env
# then edit higgsfield/.env and fill in HF_API_KEY / HF_SECRET
# from https://cloud.higgsfield.ai/api-keys
```

`.env` is already covered by the repo's `.gitignore` (`.env` pattern) — it
never gets committed, same as every other secret in this repo.

## Usage

```bash
python3 higgsfield/generate_talking_ad.py \
  --image-url "https://.../portrait.jpg" \
  --audio-url "https://.../narration.wav" \
  --prompt "handheld selfie-style UGC ad, warm lighting" \
  --duration 10
```

Both `--image-url` and `--audio-url` must already be publicly reachable
URLs — Higgsfield's API fetches from them, it doesn't accept local file
uploads directly. Host a local file somewhere reachable first (this
repo already has plenty of assets served from `studio/public/`, or use
any file host) before passing it in.

The script polls until the job finishes, saves the full raw response to
`--out` (default `result.json`), and tries to pull the finished video's
URL out of it automatically.

## What's verified vs. what isn't

- **Verified** (from Higgsfield's own open-source MCP integration,
  github.com/QalaLabs/claude-higgsfield-mcp — the closest thing to a
  public reference implementation, since the official docs site isn't
  scrapable): the base URL (`platform.higgsfield.ai`), the endpoint
  (`POST /v1/speak/higgsfield`), the auth header shape
  (`Authorization: Key {api_key}:{secret}`), the request body shape, the
  polling endpoint (`GET /v1/job-sets/{id}`), and the submit response's
  top-level shape (`{"id", "type", "jobs"}`).
- **Not verified — flagging honestly rather than guessing**: the exact
  field path to the finished video's URL inside a *completed* job-set
  response. No public source (docs, SDK examples, or the MCP's own test
  suite) shows a real completed response. `extract_video_url()` tries a
  few plausible paths and falls back to just saving the raw JSON.

**First real run**: if `extract_video_url()` comes up empty, open the
saved JSON, find the real field by hand, and send it back — that one
data point fixes the extraction logic for every run after it, instead of
guessing a second time.

## Cost

Talking-head generation is a metered, paid feature on Higgsfield (same
account/credits as the consumer app) — this script doesn't run anything
for free, it just automates the same paid call instead of clicking
through the web UI for it.
