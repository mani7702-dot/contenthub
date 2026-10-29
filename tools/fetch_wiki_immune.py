#!/usr/bin/env python3
"""Fetch Wikipedia articles for cross-checking immune cell facts."""
import urllib.request, re, html

for url_name, url in [
    ('white blood cell', 'https://en.wikipedia.org/wiki/White_blood_cell'),
    ('neutrophil', 'https://en.wikipedia.org/wiki/Neutrophil'),
    ('lymphocyte', 'https://en.wikipedia.org/wiki/Lymphocyte'),
]:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
    data = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
    
    # Extract paragraphs from the article body
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', data, re.S)
    print(f"\n{'='*60}")
    print(f"=== {url_name} ===")
    print(f"{'='*60}")
    for p in paragraphs[:8]:
        txt = re.sub(r'<[^>]+>', '', p)
        txt = html.unescape(re.sub(r'\s+', ' ', txt)).strip()
        if len(txt) > 50:
            print(txt[:300])
            print()
