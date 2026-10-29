#!/usr/bin/env python3
"""Fetch ScienceDaily article about asteroid and ants."""
import re
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.sciencedaily.com/releases/2026/10/261026225608.htm"
result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
html = result.stdout.decode('utf-8', errors='replace')

# Extract meta description
desc_match = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html, re.IGNORECASE)
if desc_match:
    print("DESC:", desc_match.group(1)[:400])

# Extract paragraphs
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
print(f"\nFound {len(paras)} paragraphs\n")
for i, p in enumerate(paras):
    clean = re.sub(r'<[^>]+>', ' ', p)
    clean = re.sub(r'&[a-z]+;', ' ', clean)
    clean = re.sub(r'&amp;', '&', clean)
    clean = re.sub(r'&#039;', "'", clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    if len(clean) > 30:
        print(f"[{i}] {clean[:500]}\n")

# Find links to original source
links = re.findall(r'href="(https?://[^"]+)"', html)
print("\n=== SOURCE LINKS ===")
for link in links:
    if not link.startswith('https://www.sciencedaily') and not link.startswith('https://www.facebook') and not link.startswith('https://twitter') and not link.startswith('https://g.co'):
        if 'doi' in link.lower() or 'amazon' in link.lower() or 'nature' in link.lower() or 'science' in link.lower() or 'academia' in link.lower() or 'edu' in link.lower() or 'wiley' in link.lower() or ' Springer' in link.lower() or 'pnas' in link.lower() or 'royalsocietypublishing' in link.lower() or 'biology' in link.lower() or 'zoology' in link.lower() or 'entomol' in link.lower() or 'insect' in link.lower() or 'army' in link.lower() or 'ant' in link.lower():
            print(f"  {link[:200]}")
