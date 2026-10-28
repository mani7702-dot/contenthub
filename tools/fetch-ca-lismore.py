#!/usr/bin/env python3
"""Fetch the Current Archaeology article about Lismore."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://archaeology.co.uk/articles/features/staffas-past-signatures.htm"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "-L", url], capture_output=True, text=True)
content = p.stdout
print(f"Page length: {len(content)}")
title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.DOTALL)
if title_match:
    print(f"Title: {title_match.group(1).strip()}")

# Try article tag then content
for pattern in [r'<article[^>]*>(.*?)</article>', 
                r'class="entry-content[^"]*"[^>]*>(.*?)</div>',
                r'class="article-body"[^>]*>(.*?)</div>',
                r'class="post-content[^"]*"[^>]*>(.*?)</div>']:
    match = re.search(pattern, content, re.DOTALL)
    if match:
        raw = match.group(1)
        text = re.sub(r'<[^>]+>', ' ', raw)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"\nFound with pattern: {pattern[:50]}")
        print(text[:8000])
        break
else:
    # Just extract all text
    text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = html.unescape(text)
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 40]
    for line in lines[:40]:
        print(line[:300])