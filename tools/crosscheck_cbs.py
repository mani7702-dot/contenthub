#!/usr/bin/env python3
"""Fetch and extract CBS News article about Joshua Service NYC cleanup."""
import subprocess, re, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
url = "https://www.cbsnews.com/newyork/news/joshua-service-brooklyn-underpass-nyc-department-of-sanitation/"

r = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, "--compressed", url],
                   capture_output=True, text=True)
print(f"Page size: {len(r.stdout)} bytes")

html_src = r.stdout

# Try to extract article content
# First try <article> tag
m = re.search(r'<article[^>]*>(.*?)</article>', html_src, re.S | re.I)
if m:
    article = m.group(1)
else:
    # Try finding the main content area
    m = re.search(r'<div[^>]*class="[^"]*article-body[^"]*"[^>]*>(.*?)</div>', html_src, re.S | re.I)
    if m:
        article = m.group(1)
    else:
        article = html_src

text = re.sub(r'<script[^>]*>.*?</script>', '', article, flags=re.S)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
text = re.sub(r'<[^>]+>', ' ', text)
text = html.unescape(text)
text = re.sub(r'\s+', ' ', text).strip()

print("=== ARTICLE TEXT ===")
print(text[:5000])
