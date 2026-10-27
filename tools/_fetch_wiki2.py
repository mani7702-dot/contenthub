#!/usr/bin/env python3
"""Fetch more context from Wikipedia Kikai caldera."""
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

url = 'https://en.wikipedia.org/wiki/Kikai_Caldera'
text = fetch_text(url)

# Print the 7300-year Akahoya eruption context
idx = text.find('7300')
if idx > 0:
    print("=== 7300 years context ===")
    print(text[max(0,idx-200):idx+1500])

# Find eruption scale info
idx = text.find('VEI')
if idx > 0:
    print(f"\n=== VEI context ===\n{text[max(0,idx-100):idx+500]}")
