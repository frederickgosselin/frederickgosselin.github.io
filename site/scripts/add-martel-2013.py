"""One-off: add Martel et al. (2013, IJRR), present in publications.md but missing from both pages."""
import os, re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "content", "pages")
NEW = ("Martel, S., Mohammadi, M., Felfoul, O., Lu, Z., Gosselin, F.P. "
       "“[Medical micro-robotics propelled and guided by magnetic resonance imaging (MRI) systems]"
       "(https://doi.org/10.1177/0278364913491470)” "
       "*International Journal of Robotics Research*, 2013, 32(9), 1010-1022.")

for lang in ("en", "fr"):
    path = os.path.join(BASE, lang, "publications.md")
    lines = open(path, encoding="utf-8").read().split("\n")
    idx = next(i for i, l in enumerate(lines) if re.match(r"^56\.\s+Guo, S\.-Z\.", l))
    assert "doi.org/10.1177/0278364913491470" not in "\n".join(lines)
    # renumber the entries after the insertion point (HTML numbering is automatic; keep the source tidy)
    for j in range(idx + 1, len(lines)):
        m = re.match(r"^(\d+)\.(\s+)", lines[j])
        if m:
            lines[j] = f"{int(m.group(1)) + 1}.{m.group(2)}" + lines[j][m.end():]
    lines.insert(idx + 1, f"57.  {NEW}")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(lang, "inserted after line", idx + 1)
