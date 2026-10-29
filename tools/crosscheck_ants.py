#!/usr/bin/env python3
"""Fetch Wikipedia article on ants for secondary verification."""
import re
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Fetch Wikipedia on ants - evolution and diversity
urls = [
    "https://en.wikipedia.org/wiki/Ant",
    "https://en.wikipedia.org/wiki/Transposable_element",
    "https://en.wikipedia.org/wiki/Cretaceous%E2%80%93Paleogene_extinction_event",
]

for url in urls:
    print(f"\n=== {url} ===")
    result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
    html = result.stdout.decode('utf-8', errors='replace')
    
    # Get first few paragraphs of body content
    # Wikipedia uses <p> tags in the main content
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    count = 0
    for p in paras:
        clean = re.sub(r'<[^>]+>', ' ', p)
        clean = re.sub(r'&#039;', "'", clean)
        clean = re.sub(r'&amp;', '&', clean)
        clean = re.sub(r'&[a-z]+;', ' ', clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        if len(clean) > 60 and not clean.startswith('You') and not clean.startswith('This'):
            print(f"  {clean[:400]}\n")
            count += 1
            if count >= 3:
                break
