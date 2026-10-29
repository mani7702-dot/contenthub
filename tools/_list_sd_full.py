#!/usr/bin/env python3
"""List all ScienceDaily top items with title + URL."""
import subprocess, xml.etree.ElementTree as ET, gzip

url = "https://www.sciencedaily.com/rss/top.xml"
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
idx = data.rfind(b"</rss>")
if idx >= 0:
    data = data[:idx+6]
root = ET.fromstring(data)
rows = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    if t and len(t) > 25:
        rows.append((t, l))
for i, (t, l) in enumerate(rows, 1):
    print(f"{i}. {t}")
    print(f"   {l}")
print(f"\nTotal: {len(rows)}")
