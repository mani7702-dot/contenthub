#!/usr/bin/env python3
"""Check all GNN feed items for coverage in ContentHub."""
import subprocess, xml.etree.ElementTree as ET, gzip
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

BLOCK = ("war", "attack", "death toll", "killed", "murder", "court", "lawsuit",
         "covid", "pandemic", "election", "politic", "terror", "bomb", "shooting")

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
        blocked = any(b in t.lower() for b in BLOCK)
        out.append({"title": t, "link": (it.findtext("link") or "").strip(),
                    "desc": (it.findtext("description") or "").strip()[:200],
                    "blocked": blocked})
    return out

rows = items("https://www.goodnewsnetwork.org/feed/")
for i, r in enumerate(rows):
    tag = "BLOCKED" if r["blocked"] else "ok"
    print(f"[{i+1}/{tag}] {r['title'][:100]}")
    if r["desc"]:
        print(f"    desc: {r['desc'][:150]}")
