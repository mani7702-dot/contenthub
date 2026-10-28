#!/usr/bin/env python3
"""Fetch CBC article about Dartmouth Spartans baseball."""
import subprocess, re, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Try CBC search and also try fetching the CBC video directly
# First try the CBC player URL
cbc_urls = [
    "https://www.cbc.ca/player/play/video/9.7384073",
    "https://www.cbc.ca/news/canada/nova-scotia/dartmouth-high-baseball-never-won-game",
    "https://www.cbc.ca/news/canada/nova-scotia/dartmouth-spartans-baseball-vibes-1.7384073",
]

for url in cbc_urls:
    r = subprocess.run(["curl", "-sL", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
    print(f"\n=== URL: {url} ===")
    print(f"Page length: {len(r.stdout)}")
    
    title_match = re.search(r"<title>(.*?)</title>", r.stdout, re.DOTALL)
    if title_match:
        print(f"TITLE: {html.unescape(title_match.group(1).strip())}")
    
    meta_desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', r.stdout)
    if meta_desc:
        print(f"META DESC: {html.unescape(meta_desc.group(1))}")
    
    # Extract paragraphs
    paras = re.findall(r"<p[^>]*>(.*?)</p>", r.stdout, re.DOTALL)
    count = 0
    for p in paras:
        t = re.sub(r"<[^>]+>", "", p).strip()
        t = html.unescape(t)
        if len(t) > 50:
            print(f"  {t[:300]}")
            count += 1
            if count >= 10:
                break
