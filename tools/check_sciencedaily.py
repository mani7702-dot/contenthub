#!/usr/bin/env python3
"""Fetch ScienceDaily top articles to find fresh stories."""
import re
import subprocess
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.sciencedaily.com/rss/top.xml"
result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = result.stdout
# Strip trailing comment
data = data.split(b'</rss>')[0] + b'</rss>'

root = ET.fromstring(data)
items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    desc = (it.findtext("description") or "").strip()
    items.append({"title": t, "link": link, "desc": desc[:300]})

print(f"Found {len(items)} ScienceDaily items\n")
for i, item in enumerate(items[:20]):
    print(f"{i}. {item['title'][:100]}")
    print(f"   {item['link'][:120]}")
    print(f"   {item['desc'][:150]}\n")
