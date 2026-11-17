import os, sys
import numpy as np
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p7lib
sys.path.insert(0, p7lib.H)
import importlib.util
spec = importlib.util.spec_from_file_location("mk6", p7lib.H + "/mk_assets6.py")
# reuse halftone()/crop_to() without re-running the module body
src = open(p7lib.H + "/mk_assets6.py").read().split("PH = H")[0]
ns = {"__file__": p7lib.H + "/mk_assets6.py"}; exec(compile(src, "mk6head", "exec"), ns)
halftone, crop_to = ns["halftone"], ns["crop_to"]
OUT = p7lib.OUT
srcs = {  # name: (file, aspect, cx, cy, width)
    "cake": (p7lib.H + "/hf/assets/photos/cake.jpg", .8, .5, .5, 700), "beach": (p7lib.H + "/hf/assets/photos/beach.jpg", .8, .56, .55, 700), "desk": (p7lib.H + "/hf/assets/photos/desk.jpg", .8, .45, .5, 700),
    "cat": (p7lib.A7 + "/ph_cat.jpg", .8, .62, .5, 700), "bikes": (p7lib.A7 + "/ph_bikes.jpg", .8, .78, .5, 700), "dog": (p7lib.A7 + "/ph_dog.jpg", .8, .4, .5, 700),
    "paris": (p7lib.A7 + "/ph_paris.jpg", 1.2, .5, .5, 700), "sled": (p7lib.A7 + "/ph_sledders.jpg", 1.0, .72, .55, 700)}
srcs.update({"cake_w": (p7lib.H + "/hf/assets/photos/cake.jpg", 1.26, .5, .5, 780), "dog_w": (p7lib.A7 + "/ph_dog.jpg", 1.26, .35, .5, 780)})
for k, (f, asp, cx, cy, w) in srcs.items():
    im = Image.open(f).convert("RGB")
    c = crop_to(im, asp, cx, cy, w)
    halftone(c, cell=6, mix=.62).save(f"{OUT}/pht_{k}.jpg", quality=90)
    print(k, c.size)

from PIL import ImageFilter
bg = Image.open(p7lib.A6 + "/cardboard.jpg").convert("RGB")
bg = bg.resize((int(bg.width * 1920 / bg.height), 1920), Image.LANCZOS)
arr = np.asarray(bg, float); gr_ = arr.mean(axis=2, keepdims=True); arr = (gr_ * .55 + arr * .45) * np.array((.98, .84, .64)) * .92
Image.fromarray(np.clip(arr, 0, 255).astype("uint8")).save(f"{OUT}/bg_card.jpg", quality=86)
print("bg ok")
