#!/usr/bin/env python3
"""Inspect HTML structure of the Van Gogh GNN page to find article content."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.goodnewsnetwork.org/star-clusters-in-van-goghs-starry-night-matches-taurus-sky-from-july-1889-shows-study/"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Find divs with class containing content
for cls in ["td-post-content", "entry-content", "article-content", "post-content", "content-area", "theiaPostSlider"]:
    matches = re.findall(rf'class="[^"]*{cls}[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
    if matches:
        print(f"=== Found class {cls}: {len(matches)} matches ===")
        raw = matches[0]
        text = re.sub(r'<[^>]+>', ' ', raw)
        text = re.sub(r'\s+', ' ', text).strip()
        print(text[:4000])
        break
else:
    # Print a snippet around 'starclusters' or 'Study' or 'researchers'
    for kw in ["Star Clusters", "star clusters", "Taurus", "study", "researchers", "astronomy"]:
        idx = html.lower().find(kw.lower())
        if idx > 0:
            snippet = html[idx-200:idx+1500]
            text = re.sub(r'<[^>]+>', ' ', snippet)
            text = re.sub(r'\s+', ' ', text).strip()
            print(f"=== keyword '{kw}' at {idx} ===")
            print(text[:3000])
            break
    else:
        print("No article text found. Page length:", len(html))
        # print first 3000 chars of body
        body = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
        if body:
            text = re.sub(r'<[^>]+>', ' ', body.group(1)[:5000])
            print("\nBody snippet:", text[:3000])
