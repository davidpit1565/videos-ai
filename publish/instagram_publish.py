#!/usr/bin/env python3
"""Publish a Reel to Instagram via the Graph API.

Instagram will not accept a local file — it fetches the video from a public URL,
so the MP4 has to be reachable on the open internet first (see publish/SETUP.md).

  export IG_USER_ID=17841400000000000
  export IG_ACCESS_TOKEN=EAAG...
  python3 instagram_publish.py --video https://…/reel-01.mp4 --caption caption.txt

  --dry-run   validate everything and stop before anything is posted
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request

API = "https://graph.facebook.com/v21.0"


def call(method, path, **params):
    params = {k: v for k, v in params.items() if v is not None}
    url = f"{API}/{path}"
    if method == "GET":
        url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url)
    else:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(params).encode())
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            err = json.loads(body)["error"]
            sys.exit(f"Instagram rejected the request ({e.code}): {err.get('message')}\n"
                     f"  type={err.get('type')} code={err.get('code')} "
                     f"subcode={err.get('error_subcode')}")
        except (KeyError, ValueError):
            sys.exit(f"Instagram rejected the request ({e.code}): {body[:400]}")


def reachable(url):
    """Instagram's fetcher is not your browser — check the URL the way it will."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=30) as r:
            ctype = r.headers.get("Content-Type", "")
            size = int(r.headers.get("Content-Length") or 0)
            return r.status == 200, ctype, size
    except Exception as e:
        return False, str(e), 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--video", required=True, help="public https URL of the MP4")
    p.add_argument("--caption", required=True, help="path to a UTF-8 caption file")
    p.add_argument("--cover", help="optional public https URL of a cover image")
    p.add_argument("--no-feed", action="store_true", help="Reels tab only, keep it off the grid")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    user_id = os.environ.get("IG_USER_ID")
    token = os.environ.get("IG_ACCESS_TOKEN")
    if not user_id or not token:
        sys.exit("Set IG_USER_ID and IG_ACCESS_TOKEN first — see publish/SETUP.md")

    caption = open(a.caption, encoding="utf-8").read().strip()
    if len(caption) > 2200:
        sys.exit(f"Caption is {len(caption)} characters; Instagram's limit is 2200.")

    ok, ctype, size = reachable(a.video)
    if not ok:
        sys.exit(f"Instagram won't be able to fetch that URL: {ctype}\n"
                 "It must be public https, no login, no redirect to a viewer page.")
    if "video" not in ctype:
        print(f"  warning: Content-Type is '{ctype}', not video/mp4. "
              "Some hosts (Drive, Dropbox share links) serve an HTML page here and the "
              "upload will fail.", file=sys.stderr)
    print(f"  video reachable · {size/1e6:.1f} MB · {ctype}")

    me = call("GET", user_id, fields="username,followers_count", access_token=token)
    print(f"  publishing as @{me.get('username')} ({me.get('followers_count')} followers)")
    print(f"  caption: {len(caption)} chars, {caption.count('#')} hashtags")

    if a.dry_run:
        print("\ndry run — nothing was posted.")
        return

    print("\ncreating media container…")
    c = call("POST", f"{user_id}/media", media_type="REELS", video_url=a.video,
             caption=caption, cover_url=a.cover,
             share_to_feed="false" if a.no_feed else "true", access_token=token)
    cid = c["id"]

    # Instagram transcodes asynchronously; publishing before it finishes just errors
    print(f"container {cid} — waiting for Instagram to transcode", end="", flush=True)
    for attempt in range(60):
        time.sleep(5)
        st = call("GET", cid, fields="status_code,status", access_token=token)
        code = st.get("status_code")
        if code == "FINISHED":
            print(" done")
            break
        if code == "ERROR":
            sys.exit(f"\nInstagram failed to process the video: {st.get('status')}")
        print(".", end="", flush=True)
    else:
        sys.exit("\nStill processing after 5 minutes — check the container later, "
                 "the video may be too long or the wrong codec.")

    print("publishing…")
    r = call("POST", f"{user_id}/media_publish", creation_id=cid, access_token=token)
    print(f"\nPublished. Media id: {r['id']}")

    q = call("GET", f"{user_id}/content_publishing_limit",
             fields="quota_usage,config", access_token=token)
    used = q.get("data", [{}])[0].get("quota_usage")
    if used is not None:
        print(f"Posts used in the last 24h: {used} of 50.")


if __name__ == "__main__":
    main()
