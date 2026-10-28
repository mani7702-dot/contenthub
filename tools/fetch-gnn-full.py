#!/usr/bin/env python3
import subprocess, xml.etree.ElementTree as ET
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.goodnewsnetwork.org/feed/"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
root = ET.fromstring(p.stdout)
items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    d = (it.findtext("description") or "").strip()[:300]
    items.append({"title": t, "link": l, "desc": d})
for i, r in enumerate(items[:30]):
    print(f'{i+1}. {r["title"]}')
    print(f'   {r["link"]}')
    print(f'   {r["desc"]}')
    print()
