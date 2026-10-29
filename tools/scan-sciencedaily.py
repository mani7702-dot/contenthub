#!/usr/bin/env python3
import subprocess, xml.etree.ElementTree as ET, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.sciencedaily.com/rss/top.xml"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
# Strip trailing comment
idx = data.rfind(b"</rss>")
if idx >= 0:
    data = data[:idx+6]
root = ET.fromstring(data)
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    if not t or len(t) < 25:
        continue
    print(t)