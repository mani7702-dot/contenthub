#!/usr/bin/env python3
"""Fetch and display all GNN RSS items."""
import subprocess, re, gzip, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.goodnewsnetwork.org/feed/"
r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = r.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
text = data.decode("utf-8", errors="replace")

# Check if we got valid data
print(f"Data length: {len(text)}")
print(f"First 200 chars: {text[:200]}")

items = re.findall(r"<item>(.*?)</item>", text, re.DOTALL)
print(f"\nFound {len(items)} items")
for i, item in enumerate(items[:10]):
    title_match = re.search(r"<title>(.*?)</title>", item, re.DOTALL)
    link_match = re.search(r"<link>(.*?)</link>", item, re.DOTALL)
    title = html.unescape(title_match.group(1).strip()) if title_match else "N/A"
    link = link_match.group(1).strip() if link_match else "N/A"
    print(f"\n{i+1}. TITLE: {title}")
    print(f"   LINK: {link}")
