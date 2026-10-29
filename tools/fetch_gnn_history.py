#!/usr/bin/env python3
"""Fetch the GNN article 'Good News in History, October 28'."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
url = "https://www.goodnewsnetwork.org/good-news-in-history-october-28/"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
html = r.stdout

content_match = re.search(r'class="[^"]*td-post-content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)
if not content_match:
    content_match = re.search(r'class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)

if content_match:
    raw = content_match.group(1)
    paras = re.findall(r"<p[^>]*>(.*?)</p>", raw, re.DOTALL)
    print(f"=== Article paragraphs ({len(paras)}) ===")
    for p in paras:
        text = re.sub(r"<[^>]+>", "", p).strip()
        if len(text) > 10:
            print(text[:500])
            print("---")
else:
    print("Could not find content div. Length:", len(html))
    title_match = re.search(r"<title>(.*?)</title>", html)
    if title_match:
        print("Title:", title_match.group(1))
