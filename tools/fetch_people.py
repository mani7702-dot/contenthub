#!/usr/bin/env python3
"""Fetch People.com article for cross-check details."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://people.com/three-tuscan-friends-cross-seas-to-return-wedding-ring-lost-in-a-river-12173081"
r = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
html = r.stdout
print(f"Fetched {len(html)} bytes")

# Extract title
title_match = re.search(r'<title>(.*?)</title>', html)
if title_match:
    print(f"Title: {title_match.group(1).strip()}")

# Extract meta description
meta = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
if meta:
    print(f"Description: {meta.group(1).strip()}")

# Look for article body
# People.com uses <p> tags within article
paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
print(f"\n=== Paragraphs ({len(paras)}) ===")
for p in paras:
    text = re.sub(r"<[^>]+>", "", p).strip()
    if len(text) > 30:
        print(text[:500])
        print("---")
