"""Move papers from "under review" to the top of the published list as "Accepted for publication in <journal>".

Edit ACCEPTED below for the next batch (order = order in the published list, newest first).
Both language pages are changed in one go, entries are renumbered. See CLAUDE.md for the publication rule.
Run python scripts/check-publications.py afterwards.
"""
import os, re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "content", "pages")

# (distinctive start of the title as it appears on the page, journal, optional preprint markdown to append)
ACCEPTED = [
    ("Two-Dimensional Cellular Material Optimization", "Materials & Design", True),
    ("Large-Scale Extrusion-Based Additive Manufacturing", "Additive Manufacturing", False),
]
HEAD_REVIEW = {"en": "**Papers under review**", "fr": "**Articles soumis à journaux à comité de lecture**"}
HEAD_PUBLISHED = {"en": "**Peer Reviewed Papers**", "fr": "**Articles publiés dans journaux à comité de lecture**"}


def renumber(lines, start, end):
    n = 1
    for j in range(start, end):
        m = re.match(r"^(\d+)\.(\s+)", lines[j])
        if m:
            lines[j] = f"{n}.{m.group(2)}" + lines[j][m.end():]
            n += 1


for lang in ("en", "fr"):
    path = os.path.join(BASE, lang, "publications.md")
    lines = open(path, encoding="utf-8").read().split("\n")
    moved = []
    for key, journal, keep_link in ACCEPTED:
        i = next(k for k, l in enumerate(lines) if re.match(r"^\d+\.\s", l) and key in l)
        entry = re.sub(r"^\d+\.\s+", "", lines.pop(i))
        # status: "under review" -> "Accepted for publication in *Journal*."
        assert re.search(r"under review\s*\.?\s*(\*\*\[Preprint\]\([^)]*\)\*\*)?\s*$", entry, flags=re.I), entry
        link = re.search(r"(\*\*\[Preprint\]\([^)]*\)\*\*)\s*$", entry)
        entry = re.sub(r"\s*under review\s*\.?\s*(\*\*\[Preprint\]\([^)]*\)\*\*)?\s*$", "", entry, flags=re.I)
        entry += f" Accepted for publication in *{journal}*."
        if link and keep_link:
            entry += " " + link.group(1)
        moved.append(entry)
    # renumber the remaining "under review" list
    h = lines.index(HEAD_REVIEW[lang])
    p = lines.index(HEAD_PUBLISHED[lang])
    renumber(lines, h + 1, p)
    # insert at the top of the published list
    first = next(k for k in range(p + 1, len(lines)) if re.match(r"^\d+\.\s", lines[k]))
    for off, entry in enumerate(moved):
        lines.insert(first + off, f"0.  {entry}")
    end = next((k for k in range(first, len(lines)) if lines[k].strip() == "" and not re.match(r"^\d+\.", lines[k + 1] if k + 1 < len(lines) else "")), len(lines))
    renumber(lines, p + 1, end)
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(lang, "ok | under review now:", sum(1 for l in lines[h + 1:p] if re.match(r"^\d+\.", l)))
