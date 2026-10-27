#!/usr/bin/env python3
"""Get full list of GNN feed items to find a new story."""
import subprocess, xml.etree.ElementTree as ET, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "https://www.goodnewsnetwork.org/feed/"], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
root = ET.fromstring(data)
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    d = (it.findtext("description") or "").strip()[:200]
    if t and len(t) > 25:
        print(f"TITLE: {t}")
        print(f"URL: {l}")
        print(f"DESC: {d}")
        print()
