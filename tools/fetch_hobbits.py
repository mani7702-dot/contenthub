#!/usr/bin/env python3
"""Fetch the GNN article about the Italian hobbits returning a wedding ring."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.goodnewsnetwork.org/3-italian-hobbits-searched-for-irishmans-precious-wedding-ring-for-days-before-bringing-it-to-his-home/"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
html = r.stdout
print(f"=== Fetched {len(html)} bytes ===\n")

# Extract article body
content_match = re.search(r'class="[^"]*td-post-content[^"]*"[^>]*>(.*?)<div class="td-post-navigation"', html, re.DOTALL)
if not content_match:
    content_match = re.search(r'class="[^"]*td-post-content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)
if content_match:
    body = content_match.group(1)
    paras = re.findall(r"<p[^>]*>(.*?)</p>", body, re.DOTALL)
    print(f"=== Article paragraphs ({len(paras)}) ===\n")
    for p in paras:
        text = re.sub(r"<[^>]+>", "", p).strip()
        if len(text) > 20:
            print(text[:600])
            print("---")
    links = re.findall(r'href="(https?://[^"]+)"', body)
    print("\n=== External links in article ===")
    for l in links:
        if "goodnewsnetwork" not in l:
            print(f"  -> {l}")
else:
    print("Could not find article content")
    # Try meta description
    meta_desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
    if meta_desc:
        print(f"Meta description: {meta_desc.group(1)}")
    title_match = re.search(r'<title>(.*?)</title>', html)
    if title_match:
        print(f"Title: {title_match.group(1)}")
