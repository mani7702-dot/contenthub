#!/usr/bin/env python3
"""Fetch GNN articles - deforestation halt and school bus rescue."""
import re
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

urls = [
    "https://www.goodnewsnetwork.org/indonesia-calls-an-early-halt-to-worlds-largest-deforestation-project-saving-potentially/",
    "https://www.goodnewsnetwork.org/st-paul-man-jumps-onto-runaway-school-bus-saves-18-children/",
    "https://www.goodnewsnetwork.org/towering-figure-of-tolerance-from-2500-years-ago-finds-new-home-in-atlanta/",
]

for url in urls:
    print(f"\n=== {url.split('/')[-2] if url.split('/')[-2] else url.split('/')[-1]} ===")
    result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
    html = result.stdout.decode('utf-8', errors='replace')
    
    if len(html) < 500:
        print(f"  (HTTP returned small response - possibly blocked)")
        continue
    
    desc_match = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html, re.IGNORECASE)
    if desc_match:
        print("DESC:", desc_match.group(1)[:300])
    
    article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
    content = article_match.group(1) if article_match else html
    paras = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    for p in paras[:5]:
        clean = re.sub(r'<[^>]+>', ' ', p)
        clean = re.sub(r'&[a-z]+;', ' ', clean)
        clean = re.sub(r'&amp;', '&', clean)
        clean = re.sub(r'&#039;', "'", clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        if len(clean) > 40:
            print(f"  - {clean[:400]}")
