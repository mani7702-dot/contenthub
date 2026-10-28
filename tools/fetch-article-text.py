#!/usr/bin/env python3
"""Fetch the full text of a GNN article for cross-checking."""
import subprocess, re, sys

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.goodnewsnetwork.org/one-teachers-idea-for-daily-positivity-practice-sweeps-through-his-elementary-school/"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Try article tag
match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
if match:
    raw = match.group(1)
else:
    # Try common content divs
    for cls in ["article-content", "td-post-content", "entry-content", "post-content"]:
        match = re.search(rf'class="{cls}"[^>]*>(.*?)</div>', html, re.DOTALL)
        if match:
            raw = match.group(1)
            break
    else:
        print("Could not extract article content. Page length:", len(html))
        sys.exit(1)

# Strip HTML tags
text = re.sub(r'<[^>]+>', ' ', raw)
text = re.sub(r'&amp;', '&', text)
text = re.sub(r'&nbsp;', ' ', text)
text = re.sub(r'&#8217;|&#8216;', "'", text)
text = re.sub(r'&#8220;|&#8221;', '"', text)
text = re.sub(r'&#8222;', '"', text)
text = re.sub(r'&#39;', "'", text)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:6000])
