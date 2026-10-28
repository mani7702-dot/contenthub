#!/usr/bin/env python3
"""Fetch the full text of the Van Gogh Starry Night GNN article."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.goodnewsnetwork.org/stars-in-van-gogh-starry-night-matches-sky-in-july-1889-shows-study/"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "-L", url], capture_output=True, text=True)
html_content = p.stdout
print(f"Page length: {len(html_content)}")

# Try article tag then content divs
for pattern in [r'<article[^>]*>(.*?)</article>', 
                r'class="article-content"[^>]*>(.*?)</div>',
                r'class="td-post-content"[^>]*>(.*?)</div>', 
                r'class="entry-content"[^>]*>(.*?)</div>',
                r'class="post-content"[^>]*>(.*?)</div>']:
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        raw = match.group(1)
        text = re.sub(r'<[^>]+>', ' ', raw)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"Found with pattern: {pattern[:40]}")
        print(text[:6000])
        break
else:
    print("No article content found")
    # Print page title
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.DOTALL)
    if title_match:
        print(f"Title: {title_match.group(1).strip()}")
