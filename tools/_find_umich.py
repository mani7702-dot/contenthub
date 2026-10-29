#!/usr/bin/env python3
"""Search for the University of Michigan SDF study press release."""
import urllib.request
import re

# Try the U-M press release search
urls = [
    "https://www.sciencedaily.com/news/matter_energy/health_meds/dental_health/",
]

for url in urls:
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8', errors='replace')
        # Look for SDF-related articles
        articles = re.findall(r'<a[^>]*href="([^"]*dental[^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)
        for href, text in articles[:20]:
            clean = re.sub(r'<[^>]+>', ' ', text).strip()
            if 'sdf' in clean.lower() or 'silver' in clean.lower() or 'cavity' in clean.lower() or 'fluoride' in clean.lower():
                print(f"  {href}: {clean[:100]}")
        
        # Also just search for SDF mentions
        if 'sdf' in html.lower() or 'silver diamine' in html.lower():
            # Find all links mentioning SDF
            all_links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)
            for href, text in all_links:
                clean = re.sub(r'<[^>]+>', ' ', text).strip()
                if 'sdf' in clean.lower() or 'silver' in clean.lower():
                    print(f"  {href}: {clean[:100]}")
    except Exception as e:
        print(f"Error: {e}")
