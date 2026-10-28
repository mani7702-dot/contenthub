#!/usr/bin/env python3
"""Fetch and parse the GNN RSS feed, looking for the knitted traffic cops item."""
import subprocess, re, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.goodnewsnetwork.org/feed/"
r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = r.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
text = data.decode("utf-8", errors="replace")

items = re.findall(r"<item>(.*?)</item>", text, re.DOTALL)
for item in items:
    if "knitted" in item.lower():
        title = re.search(r"<title>(.*?)</title>", item)
        link = re.search(r"<link>(.*?)</link>", item)
        desc = re.search(r"<description>(.*?)</description>", item, re.DOTALL)
        print("Title:", title.group(1) if title else "N/A")
        print("Link:", link.group(1) if link else "N/A")
        print("Desc:", desc.group(1)[:500] if desc else "N/A")
        print()

# Also print all titles for recent items
print("\n=== All recent GNN titles ===")
for item in items[:20]:
    title = re.search(r"<title>(.*?)</title>", item)
    if title:
        print(f"  - {title.group(1)[:90]}")
