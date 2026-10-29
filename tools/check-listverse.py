#!/usr/bin/env python3
"""Check Listverse feed for fresh stories not yet covered in ContentHub."""
import subprocess, xml.etree.ElementTree as ET, gzip
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

def items(url):
    p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
    try:
        data = p.stdout
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
        root = ET.fromstring(data)
    except Exception:
        return []
    out = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        if not t or len(t) < 25:
            continue
        out.append({"title": t, "link": (it.findtext("link") or "").strip(),
                    "desc": (it.findtext("description") or "").strip()[:200]})
    return out

rows = items("https://listverse.com/feed/")
print(f"Total Listverse items: {len(rows)}")
for r in rows:
    print(f"  - {r['title']}")
    if r["desc"]:
        print(f"    desc: {r['desc'][:150]}")
    if r["link"]:
        print(f"    url: {r['link']}")
