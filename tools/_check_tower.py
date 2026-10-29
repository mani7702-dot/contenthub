#!/usr/bin/env python3
"""Fetch Tower of London article to check kid-safety."""
import urllib.request
import re

url = "https://listverse.com/2026/10/29/10-true-tales-from-the-tower-of-londons-1000-year-history/"

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
    
    lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 40]
    
    # Find article content
    start_idx = 0
    for i, line in enumerate(lines):
        if 'true tale' in line.lower() or 'tower of london' in line.lower():
            start_idx = i
            break
    
    for line in lines[start_idx:start_idx+60]:
        print(line[:250])
        
except Exception as e:
    print(f"Error: {e}")
