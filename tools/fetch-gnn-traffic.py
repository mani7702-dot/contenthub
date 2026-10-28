#!/usr/bin/env python3
"""Fetch and parse the GNN knitted traffic cops article."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.goodnewsnetwork.org/village-installs-knitted-traffic-cops-to-slow-speeding-drivers/"
r = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
stdout = r.stdout

# Extract the main article content - look for entry-content or article body
content_match = re.search(r'class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>', stdout, re.DOTALL)
if not content_match:
    content_match = re.search(r'<article[^>]*>(.*?)</article>', stdout, re.DOTALL)
if not content_match:
    content_match = re.search(r'<div[^>]*class="[^"]*post-content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', stdout, re.DOTALL)

if content_match:
    html = content_match.group(1)
    paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
    print(f"Found {len(paras)} paragraphs in article content\n")
    for i, p in enumerate(paras):
        text = re.sub(r"<[^>]+>", "", p).strip()
        if len(text) > 20:
            print(f"[{i}] {text[:500]}")
            print()
else:
    # Fallback: get all paragraphs
    paras = re.findall(r"<p[^>]*>(.*?)</p>", stdout, re.DOTALL)
    print(f"Found {len(paras)} paragraphs total\n")
    for i, p in enumerate(paras):
        text = re.sub(r"<[^>]+>", "", p).strip()
        if len(text) > 30:
            print(f"[{i}] {text[:300]}")
            print()
