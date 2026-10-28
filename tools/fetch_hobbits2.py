#!/usr/bin/env python3
"""Fetch full GNN article content and search for second source."""
import subprocess, re

# Re-fetch the GNN article
url = "https://www.goodnewsnetwork.org/3-italian-hobbits-searched-for-irishmans-precious-wedding-ring-for-days-before-bringing-it-to-his-home/"
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
html = r.stdout

# Extract title
title_match = re.search(r'<title>(.*?)</title>', html)
if title_match:
    print(f"Article title: {title_match.group(1).strip()}")

# Extract meta description
meta_desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
if meta_desc:
    print(f"\nMeta description: {meta_desc.group(1).strip()}")

# Try to extract article body paragraphs more aggressively
print("\n=== All paragraph text ===")
paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
for p in paras:
    text = re.sub(r"<[^>]+>", "", p).strip()
    if len(text) > 30:
        print(text[:800])
        print("---")

# Also extract date from the article
date_match = re.search(r'"datePublished":"([^"]+)"', html)
if date_match:
    print(f"\nPublish date: {date_match.group(1)}")
date2 = re.search(r'class="td-post-date".*?>(.*?)<', html, re.DOTALL)
if date2:
    print(f"Date element: {date2.group(1).strip()}")
