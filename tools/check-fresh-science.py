#!/usr/bin/env python3
"""Fetch full ScienceDaily top feed and list items NOT already covered."""
import subprocess, xml.etree.ElementTree as ET, gzip, os, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.sciencedaily.com/rss/top.xml"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)

# Strip trailing comments after </rss>
data_str = data.decode("utf-8", errors="replace")
idx = data_str.rfind("</rss>")
if idx != -1:
    data_str = data_str[:idx + len("</rss>")]

root = ET.fromstring(data_str.encode())

# Gather all existing content
existing = []
for board in ["news", "blog", "trending"]:
    d = f"/home/ubuntu/contenthub/content/{board}/"
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                existing.append(f.lower())

rows = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    if not t or len(t) < 25:
        continue
    link = (it.findtext("link") or "").strip()
    desc = (it.findtext("description") or "").strip()[:300]
    rows.append({"title": t, "link": link, "desc": desc})

print(f"Total ScienceDaily top items: {len(rows)}")
print()

fresh = []
for r in rows:
    t = r["title"].lower()
    slug = re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:90]
    matched = False
    for ex in existing:
        if slug in ex or t[:40] in ex:
            matched = True
            break
    if not matched:
        fresh.append(r)

print(f"Fresh (not yet covered): {len(fresh)}")
print()
for r in fresh[:15]:
    print(f"  Title: {r['title']}")
    print(f"  Link:  {r['link']}")
    print(f"  Desc:  {r['desc'][:150]}...")
    print()
