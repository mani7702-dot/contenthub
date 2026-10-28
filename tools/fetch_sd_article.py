#!/usr/bin/env python3
"""Fetch and extract text from a ScienceDaily article page."""
import requests
import re
import sys

url = sys.argv[1]
headers = {"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"}
r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()
html = r.text

# Remove script/style
html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)

# Extract text
text = re.sub(r"<[^>]+>", " ", html)
text = re.sub(r"&[a-z]+;", " ", text)
text = re.sub(r"\s+", " ", text)

# Find the main article section
# ScienceDaily articles have <div id="text"> or similar
match = re.search(r"<div[^>]*id=[\"']text[\"'][^>]*>(.*?)</div>\s*</div>", html, flags=re.DOTALL | re.IGNORECASE)
if match:
    article_html = match.group(1)
    article_text = re.sub(r"<[^>]+>", " ", article_html)
    article_text = re.sub(r"\s+", " ", article_text).strip()
    print(f"ARTICLE ({len(article_text)} chars):")
    print(article_text[:3000])
else:
    print(text[:3000])
