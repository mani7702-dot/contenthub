#!/usr/bin/env python3
"""Fetch secondary source for Tanzania gas discovery - Africanews."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
url = "https://www.africanews.com/2026/10/28/tanzania-announces-first-major-gas-discovery-in-a-decade/"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, "-L", url], capture_output=True, text=True)
html = r.stdout

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
