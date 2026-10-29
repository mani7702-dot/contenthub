#!/usr/bin/env python3
"""Fetch the fiber supplement arthritis article from ScienceDaily."""
import urllib.request
import re

url = "https://www.sciencedaily.com/releases/2026/10/261027230715.htm"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
try:
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode('utf-8', errors='replace')
    print(f"Page length: {len(html)} chars")
    
    # ScienceDaily uses specific div classes for the article body
    # Let's try extracting paragraphs from the main content
    html2 = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html2 = re.sub(r'<style[^>]*>.*?</style>', '', html2, flags=re.DOTALL)
    
    # Try to find the article body
    body_match = re.search(r'<div[^>]*id="text-body-[^"]*"[^>]*>(.*?)</div>', html2, re.DOTALL)
    if not body_match:
        body_match = re.search(r'<div[^>]*class="[^"]*text-body[^"]*"[^>]*>(.*?)</div>', html2, re.DOTALL)
    if not body_match:
        # Try finding all paragraphs in the body
        body_match = re.search(r'<div[^>]*class="article-body"[^>]*>(.*?)</div>', html2, re.DOTALL)
    if not body_match:
        body_match = re.search(r'<div[^>]*class="md-content"[^>]*>(.*?)</div>', html2, re.DOTALL)
    
    if body_match:
        body = body_match.group(1)
    else:
        body = html2
    
    paragraphs = re.findall(r'<p>(.*?)</p>', body, re.DOTALL)
    for p in paragraphs:
        clean = re.sub(r'<[^>]+>', ' ', p).strip()
        clean = re.sub(r'\s+', ' ', clean)
        if len(clean) > 40:
            print(clean[:500])
            print()
    
    if not paragraphs:
        print("No paragraphs found, trying broader extraction...")
        text = re.sub(r'<[^>]+>', '\n', body)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 40]
        start = False
        for line in lines:
            if 'fiber' in line.lower() or 'arthritis' in line.lower() or 'supplement' in line.lower():
                start = True
            if start:
                print(line[:300])
except Exception as e:
    print(f"Error: {e}")
