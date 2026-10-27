#!/usr/bin/env python3
"""Fetch full text from a URL, return the complete article body."""
import re
import sys
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

if __name__ == '__main__':
    url = sys.argv[1]
    text = fetch_text(url)
    # Print from "FULL STORY" onwards or a good chunk
    idx = text.find('FULL STORY')
    if idx > 0:
        print(text[idx:idx+5000])
    else:
        print(text[:5000])
