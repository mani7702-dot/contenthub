#!/usr/bin/env python3
"""Fetch secondary source for Tanzania gas discovery - Tanzaniainvest."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
url = "https://www.tanzaniainvest.com/energy/mnazi-bay-gas-discovery-october-2026"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, "-L", url], capture_output=True, text=True)
html = r.stdout

for cls in ["article-content", "td-post-content", "entry-content", "post-content", "content-area", "col-md-9"]:
    match = re.search(rf'class="[^"]*{cls}[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)
    if match:
        raw = match.group(1)
        text = re.sub(r'<[^>]+>', ' ', raw)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"=== Found class {cls} ===")
        print(text[:5000])
        break

if not match:
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    print(f"Total <p> tags: {len(paras)}")
    for i, raw in enumerate(paras):
        text = re.sub(r'<[^>]+>', '', raw).strip()
        text = re.sub(r'\s+', ' ', text)
        if len(text) > 40:
            print(f"[{i}] {text[:300]}")

title_match = re.search(r"<title>(.*?)</title>", html)
if title_match:
    print(f"\n=== Title ===")
    print(title_match.group(1))
