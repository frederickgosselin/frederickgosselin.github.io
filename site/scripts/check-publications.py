"""Cross-check the EN and FR publication pages against ~/.claude/publications.md.

Usage:  python scripts/check-publications.py
Exit code 1 when something is missing or the two language pages disagree.
Matching is by DOI/preprint URL first, then by normalised title.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "..", "src", "content", "pages")
MASTER = os.path.join(os.path.expanduser("~"), ".claude", "publications.md")


def norm(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)              # markdown links -> text
    s = s.replace("–", "-").replace("—", "-")
    s = re.sub(r"[^a-z0-9]+", "", s.lower())
    return s


def urls(s):
    out = set()
    for u in re.findall(r"https?://[^\s)\]>]+", s):
        u = re.sub(r"^https?://(dx\.)?", "", u.lower()).rstrip(".,;*")
        u = re.sub(r"^doi\.org/doi:", "doi.org/", u)
        if u.startswith("doi.org/") or u.startswith("arxiv.org/abs/") or u.startswith("papers.ssrn") or "ssrn" in u:
            out.add(u)
    return out


def site_entries(lang):
    text = open(os.path.join(PAGES, lang, "publications.md"), encoding="utf-8").read()
    body = text.split("\n---\n", 1)[1]
    entries, cur = [], None
    for line in body.split("\n"):
        if re.match(r"^\d+\.\s", line):
            cur = [line]
            entries.append(cur)
        elif cur is not None and line.startswith("     ") and line.strip():
            cur.append(line)
        else:
            cur = None
    return [" ".join(e) for e in entries]


def master_entries():
    txt = open(MASTER, encoding="utf-8").read()
    sec = txt.split("## 3.", 1)[1].split("\n## 4.", 1)[0]
    out = []
    for line in sec.split("\n"):
        if not line.startswith("- "):
            continue
        m = re.match(r"- (.*?)\((\d{4})\)\.\s+(.*?)\.\s+([A-Z*_].*)", line)
        title = m.group(3) if m else line[2:80]
        out.append({"line": line, "year": m.group(2) if m else "?", "title": title, "urls": urls(line.split("[[PDF]]")[0])})
    return out


en, fr, master = site_entries("en"), site_entries("fr"), master_entries()
print(f"entries: EN {len(en)} | FR {len(fr)} | publications.md section 3: {len(master)}")

problems = 0


def covered(entries_norm, entries_urls, m):
    if any(u in eu for eu in entries_urls for u in m["urls"]):
        return True
    t = norm(m["title"])
    return len(t) > 15 and any(t in en_ for en_ in entries_norm)


for name, ents in (("EN", en), ("FR", fr)):
    ns, us = [norm(e) for e in ents], [urls(e) for e in ents]
    miss = [m for m in master if not covered(ns, us, m)]
    print(f"\n[{name}] in publications.md but NOT on the page: {len(miss)}")
    for m in miss:
        print("   ", m["year"], "|", m["title"][:100])
    problems += len(miss)

    mt = [norm(m["title"]) for m in master]
    mu = [m["urls"] for m in master]
    extra = []
    for e, n_, u_ in zip(ents, ns, us):
        if not any(t in n_ for t in mt if len(t) > 15) and not any(u in u_ for mm in mu for u in mm):
            extra.append(e)
    print(f"[{name}] on the page but NOT in publications.md: {len(extra)}")
    for e in extra:
        print("   ", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", e)[:150])
    problems += len(extra)

# author lists: compare "Surname, I." pairs for entries written surname-first (older entries are written "F. Gosselin")
AUTH = re.compile(r"([A-ZÀ-Ý][\wÀ-ÿ'’\-]+(?: [A-ZÀ-Ý][\wÀ-ÿ'’\-]+)*),\s*((?:[A-Z]\.\s?-?)+)")


def authors(s, upto):
    head = s[:upto]
    return {(re.sub(r"\W", "", a.lower()), re.sub(r"[^A-Z]", "", i)) for a, i in AUTH.findall(head)}


print("\n[authors] 'Surname, I.' differences between page (EN) and publications.md:")
adiff = 0
for m in master:
    t = norm(m["title"])
    for e in en:
        if len(t) > 15 and t in norm(e):
            # author block of the page entry = text before the first opening quote/link
            cut = re.search(r"[“\"\[]", e[4:])
            pa = authors(re.sub(r"^\d+\.\s+", "", e), (cut.start() if cut else 120))
            ma = authors(m["line"][2:], m["line"].find("(" + m["year"] + ")"))
            if pa and ma and pa != ma:
                adiff += 1
                print(f"   {m['year']} {m['title'][:60]}...\n      only on page: {sorted(pa - ma)}\n      only in publications.md: {sorted(ma - pa)}")
            break
print("   none" if not adiff else f"   {adiff} entr{'y' if adiff == 1 else 'ies'} to review")

# the two language pages must list the same papers, in the same order
print("\n[EN vs FR] entry-by-entry comparison (titles/journals must be identical):")
diff = 0
for i, (a, b) in enumerate(zip(en, fr), 1):
    if norm(a) != norm(b):
        diff += 1
        print(f"   #{i} differs:\n      EN {a[:140]}\n      FR {b[:140]}")
if len(en) != len(fr):
    diff += 1
    print("   different number of entries")
print("   identical" if not diff else f"   {diff} difference(s)")
problems += diff
sys.exit(1 if problems else 0)
