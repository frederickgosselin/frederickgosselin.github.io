"""Make a small thumbnail for the first image of every news post (EN + FR).

Output: public/uploads/news-thumbs/<same path as the original>.jpg  (max 640 px wide)
Run again whenever a news post gets a new first image.
"""
import glob, os, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
NEWS = os.path.join(HERE, "..", "src", "content", "news")
UP = os.path.join(HERE, "..", "public", "uploads")
OUT = os.path.join(UP, "news-thumbs")

done = {}
for f in glob.glob(os.path.join(NEWS, "*", "*.md")):
    body = open(f, encoding="utf-8").read().split("\n---\n", 1)[1]
    m = re.search(r"!\[[^\]]*\]\(/uploads/([^)\s]+)", body)
    if not m:
        continue
    rel = m.group(1)
    if rel in done:
        continue
    src = os.path.join(UP, *rel.split("/"))
    if not os.path.exists(src):
        print("MISSING", rel)
        continue
    if rel.lower().endswith(".pdf"):
        continue
    im = Image.open(src)
    im = im.convert("RGBA")
    bg = Image.new("RGB", im.size, (255, 255, 255))    # flatten transparency on white
    bg.paste(im, mask=im.split()[3])
    bg.thumbnail((640, 640), Image.LANCZOS)
    dst = os.path.join(OUT, *os.path.splitext(rel)[0].split("/")) + ".jpg"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    bg.save(dst, quality=82, optimize=True, progressive=True)
    done[rel] = (im.size, bg.size, os.path.getsize(dst) // 1024)

for rel, (full, small, kb) in sorted(done.items()):
    print(f"{rel}: {full[0]}x{full[1]} -> {small[0]}x{small[1]} ({kb} kB)")
print(len(done), "thumbnails")
