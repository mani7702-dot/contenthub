#!/usr/bin/env python3
"""Extract full text content from the GNN article."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

url = "https://www.goodnewsnetwork.org/village-installs-knitted-traffic-cops-to-slow-speeding-drivers/"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
stdout = r.stdout

# Extract article content from entry-content div
content_match = re.search(r'class="[^"]*td-post-content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', stdout, re.DOTALL)
if not content_match:
    content_match = re.search(r'class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', stdout, re.DOTALL)

if content_match:
    html = content_match.group(1)
    paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
    print(f"=== Article paragraphs ({len(paras)}) ===")
    for p in paras:
        text = re.sub(r"<[^>]+>", "", p).strip()
        if len(text) > 10:
            print(text[:500])
            print("---")
    
    # Also look for any embedded links
    links = re.findall(r'href="(https?://[^"]+)"', html)
    print(f"\n=== External links in article ({len(links)}) ===")
    for l in links:
        if "goodnewsnetwork" not in l:
            print(f"  -> {l}")
else:
    print("Could not find article content div")
    # Try all paragraphs
    paras = re.findall(r"<p[^>]*>(.*?)</p>", stdout, re.DOTALL)
    print(f"Total paragraphs: {len(paras)}")
    for p in paras:
        text = re.sub(r"<[^>]+>", "", p).strip()
        if len(text) > 30:
            print(f"  {text[:200]}")

# Also extract meta description
meta_desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', stdout)
if meta_desc:
    print(f"\n=== Meta description ===")
    print(meta_desc.group(1))

# Extract title
title_match = re.search(r"<title>(.*?)</title>", stdout)
if title_match:
    print(f"\n=== Title ===")
    print(title_match.group(1))
