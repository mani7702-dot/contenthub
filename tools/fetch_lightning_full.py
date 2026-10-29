#!/usr/bin/env python3
"""Fetch the full text of the lightning proposal GNN article."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
url = "https://www.goodnewsnetwork.org/man-proposes-to-his-girlfriend-after-they-were-struck-by-lightning-she-restarted-his-heart-twice/"
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
    links = re.findall(r'href="(https?://[^"]+)"', raw)
    print(f"\n=== External links in article ({len(links)}) ===")
    for l in links:
        if "goodnewsnetwork" not in l:
            print(f"  -> {l}")
else:
    print("Could not find content div. Length:", len(html))

meta_desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
if meta_desc:
    print(f"\n=== Meta description ===")
    print(meta_desc.group(1))

title_match = re.search(r"<title>(.*?)</title>", html)
if title_match:
    print(f"\n=== Title ===")
    print(title_match.group(1))
