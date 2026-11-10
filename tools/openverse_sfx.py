#!/usr/bin/env python3
"""Search Openverse for free sound effects, download one, convert to 48 kHz mono wav, log credits.

Only network hosts used: api.openverse.org and the file URL Openverse returns
(for Freesound that is cdn.freesound.org; the tool refuses any other host).
Anonymous API use, no key. Anonymous limits: 20 requests/min, 200/day.

Examples:
  python3 tools/openverse_sfx.py search "camera shutter"
  python3 tools/openverse_sfx.py search whoosh --max-seconds 2 --limit 10
  python3 tools/openverse_sfx.py get <id> --out tools/openverse_test --name whoosh_x \
        --credits tools/openverse_test/credits.md

Default licence filter is CC0 + PDM (public domain). Use --license to widen, e.g. "cc0,pdm,by"
(BY needs attribution: the credits row records it; don't use it unless you will credit).
"""
import argparse, json, os, subprocess, sys, urllib.parse, urllib.request

API = "https://api.openverse.org/v1/audio/"
UA = {"User-Agent": "sfx-search-tool/1.0"}
ALLOWED_FILE_HOSTS = {"cdn.freesound.org", "freesound.org", "upload.wikimedia.org",
                      "api.openverse.org", "audio.jamendo.com", "mp3d.jamendo.com", "prod-1.storage.jamendo.com"}


def get_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        left = r.headers.get("x-ratelimit-available-anon_sustained")
        if left is not None and int(left) < 20:
            print(f"warning: only {left} anonymous requests left today", file=sys.stderr)
        return json.load(r)


def search(q, lic, limit, max_s, min_s, source=None):
    p = {"q": q, "license": lic, "page_size": min(limit * 3, 20)}
    if source:
        p["source"] = source  # freesound | wikimedia_audio | jamendo
    d = get_json(API + "?" + urllib.parse.urlencode(p))
    out = []
    for r in d.get("results", []):
        s = (r.get("duration") or 0) / 1000
        if max_s and s > max_s or s < min_s:
            continue
        out.append(r)
    return out[:limit], d.get("result_count", 0)


def show(results):
    for r in results:
        print(f"{r['id']}  {(r.get('duration') or 0)/1000:5.2f}s  {r['license']:4}  "
              f"{r['title'][:45]!r}  by {r.get('creator')}  [{r['source']}]\n    {r['foreign_landing_url']}")


def download(r, out_dir, name, credits):
    url = r["url"]
    host = urllib.parse.urlparse(url).hostname
    if host not in ALLOWED_FILE_HOSTS:
        sys.exit(f"refusing download from unexpected host {host}")
    os.makedirs(out_dir, exist_ok=True)
    raw = os.path.join(out_dir, f"{name}.src.{r.get('filetype') or 'mp3'}")
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"download failed: HTTP {e.code} from {host} (host may be blocked by network policy)")
    with open(raw, "wb") as f:
        f.write(data)
    wav = os.path.join(out_dir, f"{name}.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-ar", "48000", "-ac", "1",
                    "-c:a", "pcm_s16le", wav], check=True)
    os.remove(raw)
    if credits:
        new = not os.path.exists(credits)
        with open(credits, "a") as f:
            if new:
                f.write("| file | title | creator | licence | source URL |\n|---|---|---|---|---|\n")
            f.write(f"| {name}.wav | {r['title']} | {r.get('creator')} | {r['license'].upper()} "
                    f"{r.get('license_version','')} ({r.get('license_url','')}) | {r['foreign_landing_url']} |\n")
    print("saved", wav)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("query")
    s.add_argument("--license", default="cc0,pdm"); s.add_argument("--limit", type=int, default=8)
    s.add_argument("--max-seconds", type=float, default=4.0); s.add_argument("--min-seconds", type=float, default=0.0)
    s.add_argument("--source", help="freesound | wikimedia_audio | jamendo")
    g = sub.add_parser("get"); g.add_argument("id")
    g.add_argument("--out", default="."); g.add_argument("--name"); g.add_argument("--credits")
    a = ap.parse_args()
    if a.cmd == "search":
        res, total = search(a.query, a.license, a.limit, a.max_seconds, a.min_seconds, a.source)
        print(f"{total} total matches for {a.query!r} ({a.license}); showing {len(res)} within duration filter")
        show(res)
    else:
        r = get_json(API + a.id + "/")
        download(r, a.out, a.name or a.id[:8], a.credits)


if __name__ == "__main__":
    main()
