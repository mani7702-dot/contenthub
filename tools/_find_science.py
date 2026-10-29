#!/usr/bin/env python3
"""Try to find the ScienceDaily article about the SDF Phase III trial."""
import urllib.request
import re

# Try different possible URLs
urls = [
    "https://www.sciencedaily.com/news/matter_energy/health_meds/dental_health/",
    "https://www.sciencedaily.com/releases/2026/10/261026000000.htm",
    "https://www.sciencedaily.com/search/?query=silver+diamine+fluoride+children",
    "https://www.sciencedaily.com/search/?query=SDF+cavity+trial+children",
    "https://www.sciencedaily.com/search/?query=University+Michigan+dental+caries+trial",
]

for url in urls:
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8', errors='replace')
        print(f"=== {url} ({len(html)} chars) ===")
        if 'search' in url:
            # Extract search results
            text = re.sub(r'<[^>]+>', '\n', html)
            text = re.sub(r'\n+', '\n', text)
            lines = [l.strip() for l in text.split('\n') if 'sdf' in l.lower() or 'silver' in l.lower() or 'diamine' in l.lower() or 'cavity' in l.lower()]
            for line in lines[:10]:
                print(f"  {line[:200]}")
        else:
            text = re.sub(r'<[^>]+>', '\n', html)
            text = re.sub(r'\n+', '\n', text)
            lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 40]
            for line in lines[5:20]:
                print(f"  {line[:200]}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    print()
