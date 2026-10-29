#!/usr/bin/env python3
"""Fetch FDA approval cavity care article from GNN."""
import urllib.request
import re

# Try the GNN article about cavities
url = "https://www.goodnewsnetwork.org/fda-approval-for-drill-free-cavity-care-may-be-imminent-after-great-phase-3-treatment-trial/"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
try:
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode('utf-8', errors='replace')
    print(f"Page length: {len(html)} chars")
    
    html2 = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html2 = re.sub(r'<style[^>]*>.*?</style>', '', html2, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', html2)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 40]
    
    for line in lines[5:50]:
        print(line[:300])
except Exception as e:
    print(f"Error: {e}")
