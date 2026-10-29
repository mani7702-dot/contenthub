#!/usr/bin/env python3
"""Fetch GNN articles - microplastics and cheetah den."""
import re
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

urls = [
    "https://www.goodnewsnetwork.org/nature-inspired-tech-prevents-microplastics-entering-atlantic-ocean-through-wastewater/",
    "https://www.goodnewsnetwork.org/live-webcam-brings-you-inside-cheetah-den-with-5-tiny-cubs-tended-by-mom/",
]

for url in urls:
    print(f"\n=== {url} ===")
    result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
    html = result.stdout.decode('utf-8', errors='replace')
    
    desc_match = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html, re.IGNORECASE)
    if desc_match:
        print("DESC:", desc_match.group(1)[:300])
    
    # Get article paragraphs
    article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
    content = article_match.group(1) if article_match else html
    paras = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    for p in paras[:6]:
        clean = re.sub(r'<[^>]+>', ' ', p)
        clean = re.sub(r'&[a-z]+;', ' ', clean)
        clean = re.sub(r'&amp;', '&', clean)
        clean = re.sub(r'&#039;', "'", clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        if len(clean) > 40:
            print(f"  - {clean[:400]}")
