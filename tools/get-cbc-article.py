#!/usr/bin/env python3
"""Fetch the CBC video page for the baseball story."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

link = "https://www.cbc.ca/player/play/video/9.7384073"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, link], capture_output=True)
cbc_html = r.stdout.decode("utf-8", errors="replace")

print(f"CBC page length: {len(cbc_html)}")

# Extract title
title_match = re.search(r"<title>(.*?)</title>", cbc_html, re.DOTALL)
if title_match:
    print(f"\nTITLE: {html.unescape(title_match.group(1).strip())}")

# Extract meta description
meta_desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', cbc_html)
if meta_desc:
    print(f"\nMETA DESC: {html.unescape(meta_desc.group(1))}")

# Extract paragraphs
paras = re.findall(r"<p[^>]*>(.*?)</p>", cbc_html, re.DOTALL)
print(f"\n=== Found {len(paras)} paragraphs ===")
for p in paras:
    text_para = re.sub(r"<[^>]+>", "", p).strip()
    text_para = html.unescape(text_para)
    if len(text_para) > 30:
        print(text_para[:500])
        print("---")

# Also try to find JSON data in the page
json_matches = re.findall(r'"description"\s*:\s*"([^"]{50,300})"', cbc_html)
if json_matches:
    print("\n=== JSON descriptions ===")
    for j in json_matches[:5]:
        print(html.unescape(j[:300]))
        print("---")
