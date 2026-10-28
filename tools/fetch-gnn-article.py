#!/usr/bin/env python3
"""Fetch a GNN article's main text content for cross-checking."""
import subprocess, re, gzip, sys

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = sys.argv[1] if len(sys.argv) > 1 else "https://www.goodnewsnetwork.org/tiny-scottish-islands-little-historical-society-makes-massive-discovery/"
r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = r.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
text = data.decode("utf-8", errors="replace")

# Find title
title_match = re.search(r"<title>(.*?)</title>", text, re.DOTALL)
if title_match:
    print(f"TITLE: {title_match.group(1).strip()}")
    print()

# Extract article body content from the GNN article
# Look for the main content area
content_match = re.search(r'<article[^>]*>(.*?)</article>', text, re.DOTALL)
if content_match:
    body = content_match.group(1)
else:
    # Try finding paragraphs with substantial content
    body = text

paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', body, re.DOTALL)
for p in paragraphs:
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(clean) > 60:
        print(clean[:400])
        print("---")
