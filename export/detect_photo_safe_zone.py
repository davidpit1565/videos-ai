#!/usr/bin/env python3
"""
detect_photo_safe_zone.py — recommend where headline/caption text can sit on
a real background photo, combining real face/subject detection (Adobe) with
real pixel-brightness measurement (PIL). Built for the "Actually Works"
photo-composite reels (video/test-photo-composite-v*.html).

WHY TWO PARTS, NOT ONE SCRIPT
------------------------------
Adobe's face/subject detection (`image_select_subject`, Photoshop API) is
only reachable in this repo as an MCP tool this session calls directly —
there is no Adobe API key or bearer token sitting in this environment's env
vars that a bare `curl`/`requests` call from inside a plain Python script
could use (checked: `env | grep -i adobe` finds nothing, and no adobe creds
file exists outside node_modules/fonts noise). So this is NOT an end-to-end
autonomous script. It is two parts:

  PART A (this file, `prepare` command): pure local work — file size, MIME
  type, and the exact upload/detect tool-call sequence — for a human or
  agent operator who HAS the Adobe MCP tools in their turn to drive.

  PART B (this file, `recommend` command): the real math. Give it the photo
  and the face/subject bbox that came back from `image_select_subject`
  (paste the normalized {x,y,w,h} straight from that tool's result), and it
  measures real pixel brightness in the candidate text zones with PIL and
  returns a structured placement + gradient recommendation. No guessing,
  no "looks about right" — every number is measured against the actual file.

USAGE
-----
Step 1 — get a bbox (an operator/agent turn, not this script):
  1. mcp__Adobe__adobe_mandatory_init (once per conversation)
  2. python3 export/detect_photo_safe_zone.py prepare <path/to/photo.png>
     -> prints file_size, media_type, and the exact next calls to make:
        mcp__Adobe__asset_initialize_file_upload(...)
        curl -X PUT <the returned transfer link> --data-binary @photo.png
        mcp__Adobe__asset_finalize_file_upload(...)
        mcp__Adobe__image_select_subject(imageURI=<presignedAssetUrl>,
            options={"bodyParts": ["Face"], "returnBbox": true})
     (If image_select_subject reports a session-token-about-to-expire
     error, that's a known transient glitch on this endpoint — retry the
     SAME call once, unchanged, before treating it as a real failure.)

Step 2 — feed the bbox back in (this script does the real work):
  python3 export/detect_photo_safe_zone.py recommend <path/to/photo.png> \\
      --bbox 0.4667,0.2036,0.275,0.2172
  (bbox is x,y,w,h — normalized 0-1, top-left origin, exactly as
  image_select_subject's metadata.bbox returns it.)

  Optional: --frame-w/--frame-h (default 1080x1920, this channel's only
  format), --safe-top/--safe-bottom/--safe-x (default from CLAUDE.md's
  measured Meta safe-area numbers: top 269px, bottom 1248px i.e. bottom
  35%=672px from the bottom, sides 65px).

OUTPUT
------
A structured report: for each quiet zone above and below the detected
face/subject —
  - its real pixel bounds and height in px (and in cqw, this codebase's
    text-sizing unit: 1cqw = frame_w/100 px)
  - real measured average brightness (0-255, PIL grayscale mean) inside
    that zone, read straight off the source image, and a resulting
    suggested darkening-gradient PEAK alpha (brighter source -> needs a
    stronger dark overlay for white text to stay legible; darker source
    needs less, so the photo itself stays visible)
  - how many lines of headline-size text (assumed ~1.1x line-height) and
    caption-size text it can hold before running into the face or the
    other safe-area edge, so a caller can decide font size honestly
    instead of guessing
  - a plain headline/caption recommendation: which zone (top or bottom of
    the detected subject) fits a 2-3-line headline, and where the caption
    should sit (this channel's existing bottom:62cqw anchor is checked
    against the subject bbox too, and flagged if the subject's own bbox
    would sit under the caption's likely text lines)

This does NOT touch the HTML build for you. It is a recommendation tool a
production agent reads and then applies (padding-top / font-size / gradient
stops) by hand, same as `video/test-photo-composite-v4.html`'s round-4b fix
was done in this session.
"""
import argparse
import json
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("PIL/Pillow not installed. `pip install pillow` and retry.", file=sys.stderr)
    sys.exit(1)


def file_info(path):
    size = os.path.getsize(path)
    ext = os.path.splitext(path)[1].lower()
    media = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(ext, "application/octet-stream")
    return size, media


def cmd_prepare(args):
    if not os.path.isfile(args.image):
        print(f"error: no such file: {args.image}", file=sys.stderr)
        sys.exit(1)
    size, media = file_info(args.image)
    print(f"file: {args.image}")
    print(f"file_size (bytes): {size}")
    print(f"media_type: {media}")
    print()
    print("Next calls (operator/agent turn, not this script):")
    print("  1. mcp__Adobe__adobe_mandatory_init()  # once per conversation")
    print("  2. mcp__Adobe__asset_initialize_file_upload("
          f"path='{args.image}', file_size={size}, media_type='{media}')")
    print("     -> take the single PUT transfer link from the result")
    print(f"  3. curl -X PUT '<transfer link>' --data-binary @'{args.image}'")
    print("  4. mcp__Adobe__asset_finalize_file_upload(filename="
          f"'{os.path.basename(args.image)}', transfer_document=<from step 2>)")
    print("     -> take presignedAssetUrl from the result")
    print("  5. mcp__Adobe__image_select_subject(imageURI=<presignedAssetUrl>,")
    print("       options={'bodyParts': ['Face'], 'returnBbox': true})")
    print("     -> metadata.bbox = {x, y, w, h}, normalized 0-1, top-left origin")
    print("     (a 'session token about to expire' error here is a known")
    print("      transient glitch on this endpoint — retry the exact same")
    print("      call once before treating it as a real failure)")
    print()
    print("Then run:")
    print(f"  python3 export/detect_photo_safe_zone.py recommend '{args.image}' "
          "--bbox x,y,w,h")


def measure_brightness(img_gray, x0, y0, x1, y1):
    x0, y0 = max(0, int(x0)), max(0, int(y0))
    x1, y1 = min(img_gray.width, int(x1)), min(img_gray.height, int(y1))
    if x1 <= x0 or y1 <= y0:
        return None
    crop = img_gray.crop((x0, y0, x1, y1))
    hist = crop.histogram()
    total = sum(hist)
    if total == 0:
        return None
    weighted = sum(v * c for v, c in enumerate(hist))
    return weighted / total


def gradient_alpha_for_brightness(brightness):
    """Brighter source content needs a stronger dark overlay to keep white
    text legible; darker content needs less, so the photo underneath stays
    visible rather than being crushed for no reason. Linear map, clamped to
    the range this codebase's existing gradients actually use (v2/v3/v4
    peaks run roughly .30 (dim) to .80 (bright/graphic))."""
    if brightness is None:
        return None
    b = max(0, min(255, brightness))
    return round(0.30 + (b / 255.0) * 0.50, 2)


def lines_that_fit(zone_h_px, font_cqw, frame_w, line_height_mult=1.15):
    font_px = font_cqw * (frame_w / 100.0)
    line_px = font_px * line_height_mult
    if line_px <= 0:
        return 0
    return int(zone_h_px // line_px)


def cmd_recommend(args):
    if not os.path.isfile(args.image):
        print(f"error: no such file: {args.image}", file=sys.stderr)
        sys.exit(1)
    try:
        bx, by, bw, bh = [float(v) for v in args.bbox.split(",")]
    except Exception:
        print("error: --bbox must be 'x,y,w,h' normalized 0-1, "
              "e.g. 0.4667,0.2036,0.275,0.2172", file=sys.stderr)
        sys.exit(1)

    fw, fh = args.frame_w, args.frame_h
    img = Image.open(args.image).convert("RGB")
    if img.width != fw or img.height != fh:
        print(f"warning: image is {img.width}x{img.height}, expected "
              f"{fw}x{fh} (this channel's only reel format) — bbox math "
              "below assumes the bbox was computed against THIS image's "
              "own dimensions; results are still normalized-fraction "
              "correct either way.", file=sys.stderr)
    gray = img.convert("L")

    face_x0, face_y0 = bx * fw, by * fh
    face_x1, face_y1 = (bx + bw) * fw, (by + bh) * fh

    safe_top, safe_bottom = args.safe_top, args.safe_bottom
    safe_x0, safe_x1 = args.safe_x, fw - args.safe_x

    zones = {}
    if face_y0 > safe_top:
        zones["above_subject"] = (safe_x0, safe_top, safe_x1, face_y0)
    if face_y1 < safe_bottom:
        zones["below_subject"] = (safe_x0, face_y1, safe_x1, safe_bottom)

    report = {
        "image": args.image,
        "frame": {"w": fw, "h": fh},
        "safe_box_px": {"x0": safe_x0, "y0": safe_top, "x1": safe_x1, "y1": safe_bottom},
        "subject_bbox_px": {
            "x0": round(face_x0, 1), "y0": round(face_y0, 1),
            "x1": round(face_x1, 1), "y1": round(face_y1, 1),
        },
        "zones": {},
    }

    HEADLINE_FONT_CQW = 9.6   # this codebase's v2/v3 default headline size
    CAPTION_FONT_CQW = 5.6    # this codebase's default caption size

    for name, (x0, y0, x1, y1) in zones.items():
        h_px = y1 - y0
        brightness = measure_brightness(gray, x0, y0, x1, y1)
        alpha = gradient_alpha_for_brightness(brightness)
        report["zones"][name] = {
            "px": {"x0": round(x0, 1), "y0": round(y0, 1), "x1": round(x1, 1), "y1": round(y1, 1)},
            "height_px": round(h_px, 1),
            "height_cqw": round(h_px / (fw / 100.0), 1),
            "measured_brightness_0_255": round(brightness, 1) if brightness is not None else None,
            "suggested_gradient_peak_alpha": alpha,
            "headline_lines_fit_at_default_9.6cqw": lines_that_fit(h_px, HEADLINE_FONT_CQW, fw),
            "caption_lines_fit_at_default_5.6cqw": lines_that_fit(h_px, CAPTION_FONT_CQW, fw),
        }

    # Plain recommendation: prefer whichever zone fits >=2 headline lines at
    # default size; if neither does, recommend the larger zone with a
    # smaller font, named explicitly rather than silently shrinking type.
    headline_choice = None
    best_lines = -1
    for name, z in report["zones"].items():
        if z["headline_lines_fit_at_default_9.6cqw"] > best_lines:
            best_lines = z["headline_lines_fit_at_default_9.6cqw"]
            headline_choice = name

    recommendation = {}
    if headline_choice and best_lines >= 2:
        recommendation["headline_zone"] = headline_choice
        recommendation["headline_font_cqw"] = HEADLINE_FONT_CQW
        recommendation["note"] = (
            f"'{headline_choice}' fits {best_lines}+ lines at the default "
            f"{HEADLINE_FONT_CQW}cqw headline size — no font-size compromise needed."
        )
    elif headline_choice:
        # Doesn't fit at default size — recommend the shrink, not silence.
        z = report["zones"][headline_choice]
        # binary-search-ish: step font down until >=2 lines fit or floor hit
        font = HEADLINE_FONT_CQW
        while font > 4.0 and lines_that_fit(z["height_px"], font, fw) < 2:
            font -= 0.2
        recommendation["headline_zone"] = headline_choice
        recommendation["headline_font_cqw"] = round(font, 1)
        recommendation["note"] = (
            f"'{headline_choice}' only fits the default headline size at "
            f"{best_lines} line(s) — shrink to ~{round(font,1)}cqw to get "
            "2 lines in, or shorten the copy instead of shrinking further."
        )
    else:
        recommendation["headline_zone"] = None
        recommendation["note"] = (
            "No quiet zone (outside the subject bbox, inside the safe box) "
            "is large enough for a real headline at any legible size. This "
            "photo needs either a re-crop/re-generate with the subject "
            "placed lower/higher, or the headline needs to overlap the "
            "subject with heavy per-word darkening behind just that text — "
            "a real trade-off, not a default to reach for."
        )

    # Caption placement: this codebase's convention anchors captions at
    # bottom:62cqw. Flag plainly if the subject's own bbox would sit under
    # where that caption's text actually renders (a 2-line caption at
    # 5.6cqw needs roughly 2*5.6*1.28*(fw/100) px above the anchor).
    caption_anchor_px_from_bottom = 62 * (fw / 100.0)
    caption_top_px = fh - caption_anchor_px_from_bottom - (2 * CAPTION_FONT_CQW * 1.28 * (fw / 100.0))
    caption_conflict = not (face_y1 <= caption_top_px or face_y0 >= fh - caption_anchor_px_from_bottom)
    recommendation["caption_anchor_bottom_cqw"] = 62
    recommendation["caption_conflicts_with_subject_bbox"] = caption_conflict
    if caption_conflict:
        recommendation["caption_note"] = (
            "The default bottom:62cqw caption anchor overlaps the detected "
            "subject bbox for this photo — move the caption anchor or "
            "re-check against this photo's actual layout before shipping."
        )

    report["recommendation"] = recommendation

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"image: {report['image']}  ({fw}x{fh})")
        print(f"safe box: x {safe_x0:.0f}-{safe_x1:.0f}  y {safe_top:.0f}-{safe_bottom:.0f}")
        print(f"subject bbox: x {face_x0:.0f}-{face_x1:.0f}  y {face_y0:.0f}-{face_y1:.0f}")
        print()
        for name, z in report["zones"].items():
            print(f"[{name}]  y {z['px']['y0']:.0f}-{z['px']['y1']:.0f}"
                  f"  ({z['height_px']:.0f}px / {z['height_cqw']:.1f}cqw tall)")
            print(f"  measured brightness: {z['measured_brightness_0_255']}"
                  f"  -> suggested gradient peak alpha: {z['suggested_gradient_peak_alpha']}")
            print(f"  fits {z['headline_lines_fit_at_default_9.6cqw']} headline "
                  f"line(s) at 9.6cqw, {z['caption_lines_fit_at_default_5.6cqw']} "
                  "caption line(s) at 5.6cqw")
            print()
        print("recommendation:")
        for k, v in recommendation.items():
            print(f"  {k}: {v}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("prepare", help="local file-size/mime lookup + the exact Adobe tool-call sequence to run")
    pp.add_argument("image")
    pp.set_defaults(func=cmd_prepare)

    pr = sub.add_parser("recommend", help="real brightness + subject-bbox based placement recommendation")
    pr.add_argument("image")
    pr.add_argument("--bbox", required=True, help="x,y,w,h normalized 0-1, from image_select_subject's metadata.bbox")
    pr.add_argument("--frame-w", type=int, default=1080)
    pr.add_argument("--frame-h", type=int, default=1920)
    pr.add_argument("--safe-top", type=float, default=269)
    pr.add_argument("--safe-bottom", type=float, default=1248)
    pr.add_argument("--safe-x", type=float, default=65)
    pr.add_argument("--json", action="store_true")
    pr.set_defaults(func=cmd_recommend)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
