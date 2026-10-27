#!/usr/bin/env python3
"""Fetch full text and print a specific range."""
import sys
import re
import urllib.request

def fetch_text(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=timeout)
    html = resp.read().decode('utf-8', errors='replace')
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

url = 'https://www.sciencedaily.com/releases/2026/10/261023003214.htm'
text = fetch_text(url)

# Print from "magma that is now present" onwards
idx = text.find('magma that is now present')
if idx > 0:
    print(text[idx:idx+3000])
else:
    # Just print the tail
    print(text[-3000:])
