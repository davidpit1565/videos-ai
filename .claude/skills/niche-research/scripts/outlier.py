#!/usr/bin/env python3
"""Rank short-form posts by how far they beat their author's follower count.

The "outlier ratio" is views / followers. A post with 3x its author's
followers is a candidate for a repeatable format; a post from a 5M-follower
account with 5M views teaches little (the account did the work, not the video).

Input, either of:
  * a saved Oriane instagram/posts-search response (raw Firecrawl JSON, or
    just the records list / {"results": [...]} from it)
  * a CSV you filled in by hand from links you found yourself, with columns:
    handle,views,followers,published,format,caption,url

Stdlib only. Usage:
  python3 outlier.py <file> [--min-views 20000] [--min-ratio 3] [--top 20]
                            [--format md|csv]

Thresholds are ASSUMPTIONS to tune on real data, not measured values.
"""
import argparse
import csv
import json
import re
import statistics
import sys

BAIT = re.compile(r"\bcomment\b|\bdm me\b|\blink in bio\b", re.IGNORECASE)


def find_records(obj):
    """Return the first list of dicts that looks like post records."""
    if isinstance(obj, list):
        if obj and isinstance(obj[0], dict) and (
            "viewsCount" in obj[0] or "views" in obj[0]
        ):
            return obj
        for item in obj:
            found = find_records(item)
            if found is not None:
                return found
    elif isinstance(obj, dict):
        for key in ("results", "records", "data", "alexandria"):
            if key in obj:
                found = find_records(obj[key])
                if found is not None:
                    return found
        for value in obj.values():
            found = find_records(value)
            if found is not None:
                return found
    return None


def to_int(value):
    try:
        return int(float(value or 0))
    except (TypeError, ValueError):
        return 0


def normalize_oriane(r):
    published = (r.get("publishedAt") or "")[:10]
    return {
        "handle": r.get("profileHandle") or "",
        "views": to_int(r.get("viewsCount")),
        "followers": to_int(r.get("profileFollowersCount")),
        "published": published,
        "format": r.get("format") or "",
        "caption": (r.get("caption") or "").replace("\n", " "),
        "url": r.get("postUrl") or r.get("profileUrl") or "",
    }


def load(path):
    if path.lower().endswith(".csv"):
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        return [
            {
                "handle": r.get("handle", ""),
                "views": to_int(r.get("views")),
                "followers": to_int(r.get("followers")),
                "published": r.get("published", ""),
                "format": r.get("format", ""),
                "caption": r.get("caption", ""),
                "url": r.get("url", ""),
            }
            for r in rows
        ]
    with open(path, encoding="utf-8") as f:
        obj = json.load(f)
    records = find_records(obj)
    if records is None:
        sys.exit("No post records found in " + path)
    return [normalize_oriane(r) for r in records]


def score(post):
    # Zero or missing follower counts must not divide by zero; treat as 1.
    return post["views"] / max(post["followers"], 1)


def rank(posts, min_views, min_ratio):
    kept = []
    for p in posts:
        ratio = score(p)
        if p["views"] < min_views or ratio < min_ratio:
            continue
        kept.append({**p, "ratio": ratio, "bait": bool(BAIT.search(p["caption"]))})
    kept.sort(key=lambda p: p["ratio"], reverse=True)
    return kept


def render_md(kept, top):
    lines = [
        "| # | views÷followers | views | followers | date | handle | format | bait | caption |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, p in enumerate(kept[:top], 1):
        cap = p["caption"][:70].replace("|", "/")
        lines.append(
            f"| {i} | {p['ratio']:.1f}x | {p['views']:,} | {p['followers']:,} | "
            f"{p['published']} | {p['handle']} | {p['format']} | "
            f"{'yes' if p['bait'] else ''} | {cap} |"
        )
    return "\n".join(lines)


def render_csv(kept, top):
    out = ["ratio,views,followers,published,handle,format,bait,url,caption"]
    for p in kept[:top]:
        cap = p["caption"].replace('"', "'")
        out.append(
            f"{p['ratio']:.2f},{p['views']},{p['followers']},{p['published']},"
            f"{p['handle']},{p['format']},{int(p['bait'])},{p['url']},\"{cap}\""
        )
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("file")
    ap.add_argument("--min-views", type=int, default=20000)
    ap.add_argument("--min-ratio", type=float, default=3.0)
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--format", choices=["md", "csv"], default="md")
    args = ap.parse_args()

    posts = load(args.file)
    kept = rank(posts, args.min_views, args.min_ratio)
    print(f"# {len(posts)} posts read, {len(kept)} pass "
          f"views>={args.min_views:,} and ratio>={args.min_ratio}x")
    if kept:
        ratios = [p["ratio"] for p in kept]
        print(f"# median ratio of kept: {statistics.median(ratios):.1f}x")
        formats = {}
        for p in kept:
            formats[p["format"] or "?"] = formats.get(p["format"] or "?", 0) + 1
        print("# formats among kept: " + ", ".join(
            f"{k}={v}" for k, v in sorted(formats.items(), key=lambda x: -x[1])))
    render = render_md if args.format == "md" else render_csv
    print(render(kept, args.top))


if __name__ == "__main__":
    main()
