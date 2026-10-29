#!/usr/bin/env python3
"""Fetch GNN article about Van Gogh Starry Night - extract full content."""
import re
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.goodnewsnetwork.org/stars-in-van-gogh-starry-night-matches-sky-in-july-1889/"
result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
html = result.stdout.decode('utf-8', errors='replace')

# Extract meta description
desc_match = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html, re.IGNORECASE)
if desc_match:
    print("META DESC:", desc_match.group(1)[:500])

# Extract article content - GNN uses <article> or .entry-content
article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
if article_match:
    content = article_match.group(1)
else:
    content = re.search(r'class="entry-content[^"]*"[^>]*>(.*?)</div>\s*</div>', html, re.DOTALL | re.IGNORECASE)
    content = content.group(1) if content else html

# Get paragraphs
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
