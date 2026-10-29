#!/usr/bin/env python3
"""Fetch GNN article - school bus rescue - full content."""
import re
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.goodnewsnetwork.org/st-paul-man-jumps-onto-runaway-school-bus-saves-18-children/"
result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
html = result.stdout.decode('utf-8', errors='replace')

desc_match = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html, re.IGNORECASE)
if desc_match:
    print("DESC:", desc_match.group(1)[:300])

# Extract more paragraphs
article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
content = article_match.group(1) if article_match else html
paras = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
print(f"\nFound {len(paras)} paragraphs\n")
for i, p in enumerate(paras):
    clean = re.sub(r'<[^>]+>', ' ', p)
    clean = re.sub(r'&[a-z]+;', ' ', clean)
    clean = re.sub(r'&amp;', '&', clean)
    clean = re.sub(r'&#039;', "'", clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    if len(clean) > 30:
        print(f"[{i}] {clean[:500]}\n")

# Also extract source links
sources = re.findall(r'href="(https?://[^"]+)"', content)
print("\n=== LINKS ===")
for s in sources[:10]:
    if 'goodnewsnetwork' not in s:
        print(s)
