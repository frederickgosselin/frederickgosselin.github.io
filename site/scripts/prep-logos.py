"""Resize the brand logos from ../logos to web-sized PNGs in public/logos."""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "logos")
DST = os.path.join(HERE, "..", "public", "logos")
os.makedirs(DST, exist_ok=True)

# (source file, output name, target width px) - widths are about 2x the displayed size for retina screens
JOBS = [
    ("Logo_Alternatif_Polytechnique_Montreal_noir_rgb.png", "polymtl-alt.png", 640),
    ("Symbole_Polytechnique_Montreal_noir_rgb@4x.png", "polymtl-symbol.png", 256),
    ("Logo-LM2-E.png", "lm2-en.png", 480),
    ("Logo-LM2-F.png", "lm2-fr.png", 480),
    ("Logo-LM2-nowriting.png", "lm2-mark.png", 240),
]

for src, out, w in JOBS:
    im = Image.open(os.path.join(SRC, src)).convert("RGBA")
    bbox = im.getbbox()          # trim transparent margins
    if bbox:
        im = im.crop(bbox)
    h = round(im.height * w / im.width)
    im = im.resize((w, h), Image.LANCZOS)
    p = os.path.join(DST, out)
    im.save(p, optimize=True)
    print(out, im.size, os.path.getsize(p) // 1024, "kB")
