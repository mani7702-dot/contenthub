#!/usr/bin/env python3
"""Fetch full ScienceDaily top RSS and extract complete item details for fresh stories."""
import subprocess, xml.etree.ElementTree as ET, gzip, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.sciencedaily.com/rss/top.xml"

result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
data = result.stdout

# Strip trailing comments
idx = data.rfind("</rss>")
if idx != -1:
    data = data[:idx + len("</rss>")]

root = ET.fromstring(data)

items = []
for it in root.iter("item"):
    title = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    desc = re.sub(r'<[^>]+>', '', it.findtext("description") or "").strip()[:300]
    guid = (it.findtext("guid") or "").strip()
    if not title or len(title) < 25:
        continue
    items.append({"title": title, "link": link, "guid": guid, "desc": desc})

print(f"Total items: {len(items)}")
print()

# Try fetching each article to see which ones work
import time
fresh_stories = []
for i, item in enumerate(items[:20]):
    test_url = item["link"]
    if not test_url:
        continue
    r = subprocess.run(["curl", "-s", "--max-time", "10", "-o", "/dev/null", "-w", "%{http_code}", "-A", UA, test_url], capture_output=True, text=True)
    code = r.stdout
    print(f"  [{code}] {item['title'][:70]} -> {item['link'][:100]}")
    if code == "200":
        fresh_stories.append(item)
    time.sleep(0.5)

print(f"\n\nFresh stories with 200 status: {len(fresh_stories)}")
for s in fresh_stories[:10]:
    print(f"\n  Title: {s['title']}")
    print(f"  URL: {s['link']}")
    print(f"  Desc: {s['desc'][:200]}")
