#!/usr/bin/env python3
"""Fetch the cranberry ScienceDaily article and extract full content."""
import subprocess, re

url = "https://www.sciencedaily.com/releases/2026/10/261027232659.htm"
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
html = result.stdout

print(f"HTML length: {len(html)}")
print(f"Status check: {html[:200]}")

# Extract title
title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
if title_match:
    print("Title:", title_match.group(1).strip())

# Extract all text content
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()
print(f"\nText content (first 3000 chars):")
print(text[:3000])
