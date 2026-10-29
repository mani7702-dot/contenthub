#!/usr/bin/env python3
"""Fetch more GNN articles - remaining candidates."""
import re
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

urls = [
    ("stranger-lunch", "https://www.goodnewsnetwork.org/anonymously-pays-dinner-tab-for-27-disability-staff-in-south-korea/"),
    ("flood-tape", "https://www.goodnewsnetwork.org/tape-can-block-99-of-water-compared-to-expensive-sandbags/"),
    ("baseball-team", "https://www.goodnewsnetwork.org/high-school-baseball-team-has-all-the-vibes-of-success-but-never-won-a-game-kids-dont-mi/"),
    ("italian-hobbits", "https://www.goodnewsnetwork.org/3-italian-hobbits-searched-for-irishmans-precious-wedding-ring-for-days-before-bringing-/"),
]

for name, url in urls:
    print(f"\n=== {name} ===")
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
    for p in paras[:4]:
        clean = re.sub(r'<[^>]+>', ' ', p)
        clean = re.sub(r'&[a-z]+;', ' ', clean)
        clean = re.sub(r'&amp;', '&', clean)
        clean = re.sub(r'&#039;', "'", clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        if len(clean) > 40:
            print(f"  - {clean[:400]}")
