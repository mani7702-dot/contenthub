#!/usr/bin/env python3
"""Parse a ScienceDaily RSS XML file and print titles."""
import xml.etree.ElementTree as ET
import gzip
import sys
import os

path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sd_top.xml"
data = open(path, "rb").read()
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
# Strip trailing HTML comments that break the XML parser
idx = data.rfind(b"</rss>")
if idx != -1:
    data = data[: idx + 6]
root = ET.fromstring(data)
count = 0
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    d = (it.findtext("description") or "").strip()[:150]
    if t and len(t) >= 25:
        count += 1
        print(f"[{count}] {t}")
        print(f"  url: {l}")
        print(f"  desc: {d}")
    if count >= 20:
        break
print(f"\nTotal items parsed: {count}")
