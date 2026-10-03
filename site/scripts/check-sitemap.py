"""Validate dist/sitemap.xml: well-formed, every URL and hreflang alternate exists in dist/, alternates are reciprocal.

Usage (after `npm run build`):  python scripts/check-sitemap.py
"""
import os, sys, urllib.parse
import xml.etree.ElementTree as ET

DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dist")
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}

root = ET.parse(os.path.join(DIST, "sitemap.xml")).getroot()
urls = {}
for u in root.findall("s:url", NS):
    loc = u.find("s:loc", NS).text
    alts = {a.get("hreflang"): a.get("href") for a in u.findall("x:link", NS)}
    urls[loc] = {"lastmod": (u.find("s:lastmod", NS).text if u.find("s:lastmod", NS) is not None else None), "alts": alts}
print("urls in sitemap:", len(urls))

problems = []


def exists(url):
    p = urllib.parse.urlparse(url).path
    return os.path.exists(os.path.join(DIST, *p.strip("/").split("/"), "index.html"))


for loc, d in urls.items():
    if not exists(loc):
        problems.append(f"missing page: {loc}")
    for lang, href in d["alts"].items():
        if not exists(href):
            problems.append(f"{loc}: alternate {lang} points to missing {href}")
        elif href != loc and urls.get(href, {}).get("alts", {}).get(urllib.parse.urlparse(loc).path.split("/")[1]) != loc:
            problems.append(f"{loc}: alternate {href} does not link back")

# every built page except the root redirect must be listed
built = []
for dp, dn, fn in os.walk(DIST):
    if "index.html" in fn:
        rel = os.path.relpath(dp, DIST).replace(os.sep, "/")
        if rel != ".":
            built.append("https://www.fgosselin.com/" + rel + "/")
unlisted = sorted(set(built) - set(urls))
if unlisted:
    problems.append(f"built pages not in sitemap: {unlisted[:5]} ... ({len(unlisted)})")
with_alt = sum(1 for d in urls.values() if len(d["alts"]) > 1)
print("urls with EN/FR alternates:", with_alt, "| without (no translation):", len(urls) - with_alt)
print("lastmod range:", min(d["lastmod"] for d in urls.values() if d["lastmod"]), "->", max(d["lastmod"] for d in urls.values() if d["lastmod"]))
print("PROBLEMS:" if problems else "OK: no problems")
for p in problems[:20]:
    print("  ", p)
sys.exit(1 if problems else 0)
