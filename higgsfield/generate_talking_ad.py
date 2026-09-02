#!/usr/bin/env python3
"""Generate a talking-head ad clip via Higgsfield's Speak v2 API.

Credentials come from HF_API_KEY / HF_SECRET, loaded from higgsfield/.env
(never committed — see .env.example). Get a key pair at
https://cloud.higgsfield.ai/api-keys.

Endpoint, auth header shape, and the submit-response shape ({"id", "type",
"jobs"}) come from Higgsfield's own open-source MCP integration
(github.com/QalaLabs/claude-higgsfield-mcp) — the closest thing to a public
reference implementation available, since the official docs site isn't
scrapable. What is NOT confirmed from any source: the exact field path to
the finished video URL inside a completed job-set response. This script
tries a few plausible paths and always saves the full raw response either
way — if none of them hit, open the saved JSON and send it back so the
extraction logic gets fixed against a real response instead of guessed at
twice.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

BASE_URL = "https://platform.higgsfield.ai"


def _headers():
    key = os.environ.get("HF_API_KEY")
    secret = os.environ.get("HF_SECRET")
    if not key or not secret:
        sys.exit(
            "Missing HF_API_KEY / HF_SECRET.\n"
            "Copy higgsfield/.env.example to higgsfield/.env and fill them in."
        )
    return {
        "Authorization": f"Key {key}:{secret}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def submit_talking_head(image_url, audio_url, prompt, quality="high", duration=5, seed=42):
    body = {
        "params": {
            "image_url": image_url,
            "audio_url": audio_url,
            "prompt": prompt,
            "quality": quality,
            "duration": duration,
            "seed": seed,
        }
    }
    r = requests.post(f"{BASE_URL}/v1/speak/higgsfield", headers=_headers(), json=body, timeout=30)
    r.raise_for_status()
    return r.json()


def poll_job_set(job_set_id, interval=5, timeout=600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(f"{BASE_URL}/v1/job-sets/{job_set_id}", headers=_headers(), timeout=30)
        r.raise_for_status()
        data = r.json()
        status = data.get("status") or data.get("state")
        print(f"  status: {status}")
        if status in ("completed", "succeeded", "done"):
            return data
        if status in ("failed", "error"):
            raise RuntimeError(f"Job failed:\n{json.dumps(data, indent=2)}")
        time.sleep(interval)
    raise TimeoutError("Timed out waiting for the job to finish.")


def extract_video_url(result):
    """Best-effort only — see module docstring."""
    candidates = [
        lambda d: d["jobs"][0]["results"]["raw"]["url"],
        lambda d: d["jobs"][0]["result"]["url"],
        lambda d: d["jobs"][0]["output"]["video_url"],
        lambda d: d["result"]["video_url"],
        lambda d: d["output_url"],
    ]
    for get in candidates:
        try:
            return get(result)
        except (KeyError, IndexError, TypeError):
            continue
    return None


def main():
    p = argparse.ArgumentParser(description="Generate a Higgsfield talking-head ad clip.")
    p.add_argument("--image-url", required=True, help="Public URL of the portrait/avatar image.")
    p.add_argument("--audio-url", required=True, help="Public URL of the narration audio (wav/mp3).")
    p.add_argument("--prompt", required=True, help="Scene/style description for the shot.")
    p.add_argument("--quality", default="high", choices=["high", "mid"])
    p.add_argument("--duration", type=int, default=5, choices=[5, 10, 15])
    p.add_argument("--out", default="result.json", help="Where to save the raw final job JSON.")
    args = p.parse_args()

    print("Submitting job...")
    submitted = submit_talking_head(
        args.image_url, args.audio_url, args.prompt, args.quality, args.duration
    )
    job_set_id = submitted.get("id")
    if not job_set_id:
        sys.exit(f"No job id in submit response:\n{json.dumps(submitted, indent=2)}")
    print(f"Job set id: {job_set_id}")

    print("Waiting for it to finish (polling every 5s)...")
    result = poll_job_set(job_set_id)

    Path(args.out).write_text(json.dumps(result, indent=2))
    print(f"Full response saved to {args.out}")

    video_url = extract_video_url(result)
    if video_url:
        print(f"\nVideo URL: {video_url}")
    else:
        print("\nCouldn't find the video URL automatically in the response.")
        print(f"Open {args.out}, find it by hand, and send it back to fix the extraction logic.")


if __name__ == "__main__":
    main()
