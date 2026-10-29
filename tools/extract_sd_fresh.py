#!/usr/bin/env python3
"""Extract full text from a ScienceDaily article URL."""
import sys, urllib.request, re, html

url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.sciencedaily.com/releases/2026/10/261027231021.htm'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
data = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')

# Extract main article text
m = re.search(r'<div[^>]*id=["\']text["\'][^>]*>(.*?)</div>', data, re.S)
if m:
    txt = re.sub(r'<[^>]+>', ' ', m.group(1))
else:
    m2 = re.search(r'<article[^>]*>(.*?)</article>', data, re.S)
    txt = re.sub(r'<[^>]+>', ' ', m2.group(1)) if m2 else data
txt = html.unescape(re.sub(r'\s+', ' ', txt)).strip()

# Print key context windows
keywords = ['sauna', 'immune', 'T cell', 'lymphocyte', 'natural killer', 'CD8', 'cytokine', 'white blood', 'Finnish', 'University', 'study', ' Published', 'journal']
seen = set()
for kw in keywords:
    low = txt.lower()
    start = 0
    while True:
        idx = low.find(kw.lower(), start)
        if idx < 0:
            break
        ctx = f"...{txt[max(0,idx-80):idx+300].strip()}..."
        if ctx not in seen:
            seen.add(ctx)
            print(f"\n=== [{kw}] ===")
            print(ctx)
        start = idx + len(kw)

print(f"\n\n=== FULL LENGTH: {len(txt)} chars ===")
