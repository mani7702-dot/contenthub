#!/usr/bin/env python3
"""Get ALL ScienceDaily top items with titles, URLs, and descriptions."""
import subprocess, xml.etree.ElementTree as ET, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

def items(url):
    p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
    try:
        data = p.stdout
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
        root = ET.fromstring(data)
    except (ET.ParseError, TypeError, Exception):
        return []
    out = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        if not t or len(t) < 25:
            continue
        out.append({"title": t, "link": (it.findtext("link") or "").strip(),
                    "desc": (it.findtext("description") or "").strip()[:300]})
    return out

rows = items("https://www.sciencedaily.com/rss/top.xml")
print(f"Total ScienceDaily top items: {len(rows)}")
print()
for i, r in enumerate(rows):
    print(f"{i+1}. {r['title']}")
    print(f"   URL: {r['link']}")
    print(f"   DESC: {r['desc'][:250]}")
    print()
