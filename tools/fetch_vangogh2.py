#!/usr/bin/env python3
"""Fallback: get all paragraph text from the Van Gogh star clusters GNN article."""
import subprocess, re, sys

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.goodnewsnetwork.org/star-clusters-in-van-goghs-starry-night-matches-taurus-sky-from-july-1889-shows-study/"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Get all <p> tags
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
out = []
for raw in paras:
    text = re.sub(r'<[^>]+>', ' ', raw)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&#8217;|&#8216;', "'", text)
    text = re.sub(r'&#8220;|&#8221;', '"', text)
    text = re.sub(r'&#39;', "'", text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > 40:
        out.append(text)
print("---ARTICLE TEXT---")
print("\n".join(out[:40]))
