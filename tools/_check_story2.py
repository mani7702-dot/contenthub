#!/usr/bin/env python3
"""Fetch article page and extract text content."""
import urllib.request
import re
import sys

url = "https://listverse.com/2026/10/08/10-animals-discovered-in-the-most-unexpected-places/"
# Actually let me just get the description from the RSS feed again
# The fetch-news already gave us the description

url = "https://listverse.com/2026/10/28/10-animals-discovered-in-the-most-unexpected-places/"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
try:
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode('utf-8', errors='replace')
    print(f"Page length: {len(html)} chars")
    
    # Remove script/style tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    
    # Find all text between tags
    text = re.sub(r'<[^>]+>', '\n', html)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Print lines that look like article content (longer than 30 chars)
    lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 30]
    
    # Find where the article starts
    start_idx = 0
    for i, line in enumerate(lines):
        if 'unexpected' in line.lower() or 'animals' in line.lower():
            start_idx = i
            break
    
    for line in lines[start_idx:start_idx+50]:
        print(line[:200])
except Exception as e:
    print(f"Error: {e}")
