#!/usr/bin/env python3
"""Fetch GNN articles that are likely fresh - check each candidate."""
import re
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

candidates = [
    "https://www.goodnewsnetwork.org/stargazers-flood-light-pollution-map-lets-them-see-which-constellations-are-visible/",
    "https://www.goodnewsnetwork.org/ancient-sundial-found-in-cairo-mosque-parking-lot/",
    "https://www.goodnewsnetwork.org/van-gogh-debuts-16-new-paintings-in-first-ever-ai-exhibition/",
]

# Check from the scan-all-lanes output - let me look at more GNN items
# Let me fetch the GNN feed directly and get ALL headlines
result = subprocess.run([
    "curl", "-s", "--max-time", "25", "-A", UA,
    "https://www.goodnewsnetwork.org/feed/"
], capture_output=True)
html = result.stdout.decode('utf-8', errors='replace')

# Extract titles
titles = re.findall(r'<title[^>]*>(.*?)</title>', html)
links = re.findall(r'<link[^>]*>(.*?)</link>', html)

# Filter for non-empty, non-RSS titles
print(f"Found {len(titles)} titles in GNN feed")
for i, (t, l) in enumerate(zip(titles, links)):
    t = re.sub(r'<[^>]+>', '', t).strip()
    l = l.strip()
    if len(t) > 30 and 'goodnewsnetwork' not in t.lower() and l.startswith('http'):
        print(f"{i}: {t[:100]} -> {l[:120]}")
