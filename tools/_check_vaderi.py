#!/usr/bin/env python3
"""Check Bathynomus vaderi details on Wikipedia."""
import urllib.request
import re

url = "https://en.wikipedia.org/wiki/Bathynomus_vaderi"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
try:
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode('utf-8', errors='replace')
    
    # Look for the scientific description
    html2 = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html2 = re.sub(r'<style[^>]*>.*?</style>', '', html2, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', html2)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 40]
    
    for line in lines[:30]:
        print(line[:300])
except Exception as e:
    print(f"Error: {e}")
    # The page might not exist, try searching
    print("\nTrying to find info in main Bathynomus article...")
    url2 = "https://en.wikipedia.org/wiki/Giant_isopod"
    req2 = urllib.request.Request(url2, headers={
        'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
    })
    resp2 = urllib.request.urlopen(req2, timeout=15)
    html2 = resp2.read().decode('utf-8', errors='replace')
    html2 = re.sub(r'<script[^>]*>.*?</script>', '', html2, flags=re.DOTALL)
    html2 = re.sub(r'<style[^>]*>.*?</style>', '', html2, flags=re.DOTALL)
    text2 = re.sub(r'<[^>]+>', '\n', html2)
    text2 = re.sub(r'\n+', '\n', text2)
    text2 = re.sub(r'[ \t]+', ' ', text2)
    lines2 = [l.strip() for l in text2.split('\n') if len(l.strip()) > 40]
    
    for line in lines2:
        if 'vader' in line.lower() or 'viet' in line.lower() or 'darth' in line.lower() or 'new species' in line.lower():
            print(f"  {line[:300]}")
