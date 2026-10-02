"""One-off repair of the converted publication pages (EN + FR).

- moves the six journal-cover <img> lines into front matter (`covers:`), rendered as a click-to-enlarge grid
- repairs the arXiv link of entry 39 that the converter split over two lines
- repairs the malformed thesis link and the escaped underscore in the final link
- FR: translates only the thesis captions (headings were already translated); titles/journals stay as they are
"""
import re, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "content", "pages")

COVERS = [
    ("/uploads/2015/04/JFMcoverbig.jpg", "JFMcoverbig.jpg",
     "Cover of the Journal of Fluid Mechanics (Gosselin, de Langre & Machado-Almeida, 2010)",
     "Couverture du Journal of Fluid Mechanics (Gosselin, de Langre & Machado-Almeida, 2010)"),
    ("/uploads/2020/12/Passieux2015_AdvancedMaterials-Cover-cropped.jpg", "Passieux2015_AdvancedMaterials-Cover-cropped.jpg",
     "Cover of Advanced Materials (Passieux et al., 2015)",
     "Couverture d'Advanced Materials (Passieux et al., 2015)"),
    ("/uploads/2020/12/Bodkhe2018-40-Back-cover-scaled.jpg", "Bodkhe2018-40-Back-cover-scaled.jpg",
     "Cover of Advanced Engineering Materials (Bodkhe et al., 2018)",
     "Quatrième de couverture (Bodkhe et al., 2018)"),
    ("/uploads/2019/07/Bidhendi2019-CellReportCover-1.jpg", "Bidhendi2019-CellReportCover-1.jpg",
     "Cover of Cell Reports (Bidhendi et al., 2019)",
     "Couverture de Cell Reports (Bidhendi et al., 2019)"),
    ("/uploads/2020/12/Zou2020-CRPS-Cover.jpg", "Zou2020-CRPS-Cover.jpg",
     "Cover of Cell Reports Physical Science (Zou et al., 2020)",
     "Couverture de Cell Reports Physical Science (Zou et al., 2020)"),
    ("/uploads/2021/04/Boudina2021-JFM-cover-scaled.jpg", "Boudina2021-JFM-cover-scaled.jpg",
     "Cover of the Journal of Fluid Mechanics (Boudina, Gosselin & Étienne, 2021)",
     "Couverture du Journal of Fluid Mechanics (Boudina, Gosselin & Étienne, 2021)"),
]

THESIS_URL = "https://publications.polymtl.ca/view/advisor/Gosselin,_Frederick.html"

for lang in ("en", "fr"):
    path = os.path.join(BASE, lang, "publications.md")
    s = open(path, encoding="utf-8").read()

    # 1. cover images out of the body
    n_before = len(re.findall(r"^!\[\]\(/uploads/.*\)\s*$", s, flags=re.M))
    s = re.sub(r"^!\[\]\(/uploads/[^)\n]*\)\s*\n\n", "", s, flags=re.M)
    assert n_before == 6, n_before

    # 2. covers into front matter
    yaml = "covers:\n"
    for full, thumb, alt_en, alt_fr in COVERS:
        alt = alt_en if lang == "en" else alt_fr
        yaml += f'  - src: "{full}"\n    thumb: "/uploads/covers/{thumb}"\n    alt: "{alt}"\n'
    s = re.sub(r"(\norder: \d+\n)", r"\1" + yaml.replace("\\", "\\\\"), s, count=1)

    # 3. broken arXiv link of entry 39 (split over two lines)
    s, k = re.subn(r"\(\s*\n\s+(http://arxiv\.org/abs/1905\.08055\))", r"(\1", s)
    assert k == 1, ("arxiv", k)

    # 4. thesis link with stray angle brackets/space
    s, k = re.subn(r"\(<\s*(https://hal\.archives-ouvertes\.fr/tel-01765524)>\)", r"(\1)", s)
    assert k == 1, ("hal", k)

    # 5. final link: escaped underscore
    s = s.replace("Gosselin,\\_Frederick.html", "Gosselin,_Frederick.html")

    # 6. captions
    if lang == "fr":
        s, k = re.subn(r"^Thèse de doctorat\s*$", "Ma thèse de doctorat (en français)  ", s, flags=re.M)
        assert k == 1, ("thesis caption", k)
        if THESIS_URL not in s:
            s = s.rstrip("\n") + "\n\nThèses de doctorat et de maîtrise des étudiants que j’ai supervisés ou co-supervisés au fil des ans :  \n" \
                f"[{THESIS_URL}]({THESIS_URL})\n"
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    print(lang, "ok; numbered entries:", len(re.findall(r"^\d+\.\s", s, flags=re.M)))
