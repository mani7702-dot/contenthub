#!/usr/bin/env python3
"""Search Bing News RSS for secondary sources."""
import subprocess, urllib.parse, xml.etree.ElementTree as ET

queries = [
    "magma oxygen deep earth atmosphere volcano",
    "excess oxygen magma National Science Review HPSTAR",
]
for q in queries:
    url = f"https://www.bing.com/news/search?q={urllib.parse.quote(q)}&format=RSS"
    p = subprocess.run(["curl", "-s", "--max-time", "15", "-A",
        "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)", url], capture_output=True)
    data = p.stdout
    try:
        root = ET.fromstring(data)
        print(f"\n=== Query: {q} ===")
        count = 0
        for item in root.iter("item"):
            t = (item.findtext("title") or "").strip()
            l = (item.findtext("link") or "").strip()
            d = (item.findtext("description") or "").strip()
            print(f"  Title: {t[:120]}")
            print(f"  URL: {l[:150]}")
            print(f"  Desc: {d[:200]}")
            print()
            count += 1
            if count >= 5:
                break
    except Exception as e:
        print(f"Error: {e}")
        print(f"Data: {data[:200]}")
