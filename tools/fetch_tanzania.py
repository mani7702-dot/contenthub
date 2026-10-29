#!/usr/bin/env python3
"""Fetch full text of the Tanzania natural gas discovery story from BBC."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
url = "https://www.bbc.co.uk/news/articles/c5m2dry2xwwvo?at_medium=RSS&at_campaign=rss"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, "-L", url], capture_output=True, text=True)
html = r.stdout

paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
print(f"Total <p> tags: {len(paras)}")
for i, raw in enumerate(paras):
    text = re.sub(r'<[^>]+>', '', raw).strip()
    text = re.sub(r'\s+', ' ', text)
    if len(text) > 40 and not text.startswith('Skip') and not text.startswith('BBC'):
        print(f"[{i}] {text[:300]}")

meta_desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
if meta_desc:
    print(f"\n=== Meta description ===")
    print(meta_desc.group(1))

title_match = re.search(r"<title>(.*?)</title>", html)
if title_match:
    print(f"\n=== Title ===")
    print(title_match.group(1))
