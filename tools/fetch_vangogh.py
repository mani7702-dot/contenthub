#!/usr/bin/env python3
"""Fetch the full text of the Van Gogh star clusters GNN article for cross-checking."""
import subprocess, re, sys

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.goodnewsnetwork.org/star-clusters-in-van-goghs-starry-night-matches-taurus-sky-from-july-1889-shows-study/"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
if match:
    raw = match.group(1)
else:
    for cls in ["article-content", "td-post-content", "entry-content", "post-content"]:
        match = re.search(rf'class="{cls}"[^>]*>(.*?)</div>', html, re.DOTALL)
        if match:
            raw = match.group(1)
            break
    else:
        print("Could not extract article content. Page length:", len(html))
        sys.exit(1)

text = re.sub(r'<[^>]+>', ' ', raw)
text = re.sub(r'&amp;', '&', text)
text = re.sub(r'&nbsp;', ' ', text)
text = re.sub(r'&#8217;|&#8216;', "'", text)
text = re.sub(r'&#8220;|&#8221;', '"', text)
text = re.sub(r'&#39;', "'", text)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:6000])
