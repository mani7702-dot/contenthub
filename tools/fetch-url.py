#!/usr/bin/env python3
"""Fetch a URL and extract title + paragraphs using subprocess (Tirith-safe)."""
import subprocess, re, sys

url = sys.argv[1] if len(sys.argv) > 1 else ""
if not url:
    print("Usage: fetch-url.py <url>")
    sys.exit(1)

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
result = subprocess.run(
    ["curl", "-s", "--max-time", "25", "-A", UA, url],
    capture_output=True, text=True
)
html = result.stdout

# Extract title
title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
if title_match:
    print("Title:", title_match.group(1).strip())

# Extract paragraph text
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
for i, p in enumerate(paras[:30]):
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(clean) > 30:
        print(f"\n--- Para {i+1} ---")
        print(clean[:500])

# Also look for description meta tag
desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
if desc_match:
    print("\n\nMeta Description:", desc_match.group(1).strip()[:500])
