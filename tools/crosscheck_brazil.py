#!/usr/bin/env python3
"""Cross-check Brazil 6-day workweek constitutional amendment story."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
urls = [
    "https://www.goodnewsnetwork.org/brazil-ends-long-tradition-of-6-day-workweek-via-constitutional-amendment/",
]

# First, fetch the GNN article to find the original source links
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, urls[0]], capture_output=True, text=True)
html = r.stdout

# Extract article body paragraphs
content_match = re.search(r'class="[^"]*td-post-content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)
if content_match:
    body = content_match.group(1)
    paras = re.findall(r"<p[^>]*>(.*?)</p>", body, re.DOTALL)
    print(f"=== GNN article paragraphs ({len(paras)}) ===")
    for p in paras:
        text = re.sub(r"<[^>]+>", "", p).strip()
        if len(text) > 20:
            print(text[:500])
            print("---")
    # Find all links in the article
    links = re.findall(r'href="(https?://[^"]+)"', body)
    print("\n=== External links in article ===")
    for l in links:
        if "goodnewsnetwork" not in l:
            print(f"  -> {l}")
else:
    # Try all paragraphs
    paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
    print(f"Total paragraphs: {len(paras)}")
    for p in paras:
        text = re.sub(r"<[^>]+>", "", p).strip()
        if len(text) > 40:
            print(f"  {text[:300]}")
