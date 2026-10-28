#!/usr/bin/env python3
"""Parse ScienceDaily RSS and print title/url/guid for each item."""
import xml.etree.ElementTree as ET
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sd_top2.xml"
data = open(path, "rb").read()
idx = data.rfind(b"</rss>")
if idx != -1:
    data = data[: idx + 6]
root = ET.fromstring(data)
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    g = (it.findtext("guid") or "").strip()
    print(t)
    print(f"  url: {l}")
    print(f"  guid: {g}")
    print()
