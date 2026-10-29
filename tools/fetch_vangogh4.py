#!/usr/bin/env python3
"""Extract content from Van Gogh GNN page - broader search."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.goodnewsnetwork.org/star-clusters-in-van-goghs-starry-night-matches-taurus-sky-from-july-1889-shows-study/"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Find all text between <p> tags, collect them
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
print(f"Total <p> tags: {len(paras)}")
for i, raw in enumerate(paras):
    text = re.sub(r'<[^>]+>', ' ', raw)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&#8217;|&#8216;', "'", text)
    text = re.sub(r'&#8220;|&#8221;', '"', text)
    text = re.sub(r'&#39;', "'", text)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > 30 and not text.startswith('Share') and not text.startswith('Comments'):
        print(f"[{i}] {text[:200]}")
