#!/usr/bin/env python3
"""Fetch the ScienceDaily article about SDF cavity treatment."""
import urllib.request
import re

url = "https://www.sciencedaily.com/releases/2026/10/261026093000.htm"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
try:
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode('utf-8', errors='replace')
    print(f"Page length: {len(html)} chars")
    
    # Try to extract the abstract/p content
    # ScienceDaily uses specific div classes
    match = re.search(r'<div[^>]*class="[^"]*text-body[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
    if not match:
        match = re.search(r'<p>(.*?)</p>', html, re.DOTALL)
    
    if match:
        body = match.group(1) if isinstance(match, re.Match) else match
    else:
        body = html
    
    # Extract all paragraph text
    paragraphs = re.findall(r'<p>(.*?)</p>', body, re.DOTALL)
    for p in paragraphs:
        clean = re.sub(r'<[^>]+>', ' ', p).strip()
        clean = re.sub(r'\s+', ' ', clean)
        if len(clean) > 40:
            print(clean[:400])
            print()
    
    if not paragraphs:
        # Try broader extraction
        text = re.sub(r'<[^>]+>', '\n', html)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 40]
        start = False
        for line in lines:
            if 'SDF' in line or 'silver diamine' in line.lower() or 'cavity' in line.lower() or 'tooth' in line.lower():
                start = True
            if start:
                print(line[:300])
except Exception as e:
    print(f"Error: {e}")
