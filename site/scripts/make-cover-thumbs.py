"""Make grid thumbnails for the journal covers (full-size originals stay in public/uploads)."""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.join(HERE, "..", "public", "uploads")
OUT = os.path.join(UP, "covers")
os.makedirs(OUT, exist_ok=True)

COVERS = [
    "2015/04/JFMcoverbig.jpg",
    "2020/12/Passieux2015_AdvancedMaterials-Cover-cropped.jpg",
    "2020/12/Bodkhe2018-40-Back-cover-scaled.jpg",
    "2019/07/Bidhendi2019-CellReportCover-1.jpg",
    "2020/12/Zou2020-CRPS-Cover.jpg",
    "2021/04/Boudina2021-JFM-cover-scaled.jpg",
]
for rel in COVERS:
    im = Image.open(os.path.join(UP, *rel.split("/"))).convert("RGB")
    w0, h0 = im.size
    im.thumbnail((520, 520), Image.LANCZOS)
    name = os.path.basename(rel)
    im.save(os.path.join(OUT, name), quality=84, optimize=True, progressive=True)
    print(f"{name}: full {w0}x{h0} (ratio {w0/h0:.2f}) -> thumb {im.size}, {os.path.getsize(os.path.join(OUT, name))//1024} kB; full {os.path.getsize(os.path.join(UP, *rel.split('/')))//1024} kB")
