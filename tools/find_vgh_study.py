#!/usr/bin/env python3
"""Fetch GNN article about Van Gogh Starry Night Taurus study."""
import sys
import re
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Search GNN for the Van Gogh Taurus story
search_urls = [
    "https://www.goodnewsnetwork.org/?s=van+gogh+starry+night+taurus",
    "https://www.goodnewsnetwork.org/?s=starry+night+constellation+study",
]

for url in search_urls:
    result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
    html = result.stdout.decode('utf-8', errors='replace')
    
    # Find article links
    links = re.findall(r'href="(https://www\.goodnewsnetwork\.org/.*?(?:van|gogh|starry|taurus|constellation).*?/)"', html, re.IGNORECASE)
    for link in links[:5]:
        print(f"Found: {link}")
    
    # Also look for any article links in search results
    all_links = re.findall(r'href="(https://www\.goodnewsnetwork\.org/[^"]+)"', html)
    article_links = [l for l in all_links if '/?p=' not in l and 'tag' not in l and len(l) > 50]
    for link in article_links[:10]:
        print(f"  Article: {link}")

# Also search for the study directly
print("\n=== Searching for study ===")
result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "https://www.goodnewsnetwork.org/?s=starry+night+matches+taurus"], capture_output=True)
html = result.stdout.decode('utf-8', errors='replace')
links = re.findall(r'href="(https://www\.goodnewsnetwork\.org/[^"]+)"', html)
for link in links[:20]:
    if '/?p=' not in link:
        print(link)
