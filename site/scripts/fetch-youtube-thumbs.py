"""Download the poster image of every YouTube video embedded in a news post (EN + FR).

Source: https://i.ytimg.com/vi/<id>/maxresdefault.jpg (falls back to hqdefault, with its letterbox bars cropped).
Output: public/uploads/news-thumbs/yt-<id>.jpg, 640 px wide, 16:9.
Files are committed, so visitors never contact YouTube just to see the news cards.
"""
import glob, io, os, re, sys, urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
NEWS = os.path.join(HERE, "..", "src", "content", "news")
OUT = os.path.join(HERE, "..", "public", "uploads", "news-thumbs")
os.makedirs(OUT, exist_ok=True)

ids = {}
for f in sorted(glob.glob(os.path.join(NEWS, "*", "*.md"))):
    body = open(f, encoding="utf-8").read().split("\n---\n", 1)[1]
    for vid in re.findall(r"youtube(?:-nocookie)?\.com/embed/([\w-]{6,})", body):
        ids.setdefault(vid, os.path.basename(f))
print(len(ids), "distinct YouTube videos")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


ok = 0
for vid, src in ids.items():
    dst = os.path.join(OUT, f"yt-{vid}.jpg")
    img = None
    for name in ("maxresdefault", "hqdefault"):
        try:
            data = fetch(f"https://i.ytimg.com/vi/{vid}/{name}.jpg")
            im = Image.open(io.BytesIO(data)).convert("RGB")
            if im.width < 200:                    # YouTube serves a tiny placeholder for missing sizes
                continue
            if name == "hqdefault":               # 4:3 with black bars above/below the 16:9 picture: crop them
                h = round(im.width * 9 / 16)
                top = (im.height - h) // 2
                im = im.crop((0, top, im.width, top + h))
            img = im
            break
        except Exception as e:
            print("  ", vid, name, "failed:", e)
    if img is None:
        print("NO THUMBNAIL", vid, src)
        continue
    img.thumbnail((640, 640), Image.LANCZOS)
    img.save(dst, quality=82, optimize=True, progressive=True)
    ok += 1
    print(f"yt-{vid}.jpg  {img.size}  {os.path.getsize(dst)//1024} kB   ({src[:50]})")
print(ok, "of", len(ids), "saved")
sys.exit(0 if ok == len(ids) else 1)
