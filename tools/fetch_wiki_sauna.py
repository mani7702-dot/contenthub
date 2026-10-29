#!/usr/bin/env python3
"""Fetch Wikipedia article about sauna and health for cross-checking."""
import urllib.request, re, html

# Fetch Wikipedia sauna article
url = 'https://en.wikipedia.org/wiki/Sauna'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
data = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')

# Extract text content
txt = re.sub(r'<[^>]+>', ' ', data)
txt = html.unescape(re.sub(r'\s+', ' ', txt)).strip()

# Search for immune-related content
for kw in ['immune', 'white blood', 'neutrophil', 'lymphocyte', 'inflammation', 'cardiovascular', 'Finnish']:
    idx = txt.lower().find(kw.lower())
    if idx >= 0:
        print(f"\n=== [{kw}] ===")
        print(f"...{txt[max(0,idx-100):idx+300].strip()}...")
