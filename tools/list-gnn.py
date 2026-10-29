#!/usr/bin/env python3
"""List all GNN headlines without keyword filtering."""
import subprocess, xml.etree.ElementTree as ET, gzip
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "https://www.goodnewsnetwork.org/feed/"], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
root = ET.fromstring(data)
count = 0
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    if len(t) < 25:
        continue
    link = (it.findtext("link") or "").strip()
    desc = (it.findtext("description") or "").strip()[:300]
    print(f"--- {t}")
    print(f"  URL: {link}")
    print(f"  DESC: {desc}")
    count += 1
print(f"\nTotal: {count} items")
