"""Add a newly submitted paper at the top of the "under review" list of both publication pages (EN + FR).

Usage: python scripts/add-submitted-paper.py
The new entry is placed first (newest first, like the published list); the existing entries are renumbered.
Edit AUTHORS and TITLE below for the next paper.  See CLAUDE.md for the publication rule.
"""
import os, re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "content", "pages")
AUTHORS = "Moazen, S., Wong, J.C.H., Gosselin, F.P., Tabiai, I., Dubé, M."
TITLE = "Enhancing Mechanical Performance of FFF-printed LDPE/Regolith Composites via Discrete In-situ Consolidation"
ENTRY = f"{AUTHORS} “{TITLE}” under review"

HEADINGS = {"en": "**Papers under review**", "fr": "**Articles soumis à journaux à comité de lecture**"}

for lang in ("en", "fr"):
    path = os.path.join(BASE, lang, "publications.md")
    lines = open(path, encoding="utf-8").read().split("\n")
    assert TITLE not in "\n".join(lines), f"{lang}: already present"
    h = lines.index(HEADINGS[lang])
    # first numbered entry after the heading, then renumber until the next heading
    first = next(i for i in range(h + 1, len(lines)) if re.match(r"^\d+\.\s", lines[i]))
    end = next(i for i in range(first, len(lines)) if lines[i].startswith("**"))
    for j in range(first, end):
        m = re.match(r"^(\d+)\.(\s+)", lines[j])
        if m:
            lines[j] = f"{int(m.group(1)) + 1}.{m.group(2)}" + lines[j][m.end():]
    lines.insert(first, f"1.  {ENTRY}")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(lang, "inserted at line", first + 1, "| under-review entries now:", end - first + 1 - sum(1 for k in range(first, end + 1) if not re.match(r"^\d+\.", lines[k])))
