#!/usr/bin/env python3
"""Fetch and extract article body for cross-checking."""
import urllib.request
import re
import sys

url = sys.argv[1] if len(sys.argv) > 1 else "https://listverse.com/2026/10/28/10-animals-discovered-in-the-most-unexpected-places/"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='replace')

# Try to extract article body
article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
body = article_match.group(1) if article_match else html

# Extract list items
items = re.findall(r'<li>(.*?)</li>', body, re.DOTALL)
print(f"Found {len(items)} list items")
for i, item in enumerate(items[:20]):
    clean = re.sub(r'<[^>]+>', ' ', item).strip()
    clean = re.sub(r'\s+', ' ', clean)
    if len(clean) > 20:
        print(f"{i+1}. {clean[:300]}")
        print()

# Also try extracting paragraphs
paragraphs = re.findall(r'<p>(.*?)</p>', body, re.DOTALL)
print("\n=== Paragraphs ===")
for i, p in enumerate(paragraphs[:15]):
    clean = re.sub(r'<[^>]+>', ' ', p).strip()
    clean = re.sub(r'\s+', ' ', clean)
    if len(clean) > 20:
        print(f"P{i+1}. {clean[:300]}")
