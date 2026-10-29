#!/usr/bin/env python3
"""Search for the study in ScienceDaily using web search approach."""
import urllib.request
import re
import urllib.parse

# Try to find the article on ScienceDaily by searching their site
# The GNN article mentions: University of Michigan, Phase III trial, 830 children, 
# silver diamine fluoride (SDF), Advantage Arrest 38% SDF, Elevate Oral Care

# Let's try to find it through a Google-like search
urls = [
    "https://www.sciencedaily.com/search/?query=silver+diamine+fluoride+michigan+trial",
    "https://www.sciencedaily.com/search/?query=Advantage+Arrest+SDF+Phase+III",
    "https://www.sciencedaily.com/search/?query=diamond+tooth+decay+children+sdf",
]

for url in urls:
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8', errors='replace')
        # Look for result links
        results = re.findall(r'<a[^>]*href="(/releases/[^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)
        if results:
            for href, text in results[:10]:
                clean = re.sub(r'<[^>]+>', ' ', text).strip()
                if len(clean) > 20:
                    print(f"  https://www.sciencedaily.com{href}: {clean[:100]}")
        else:
            # Try broader link extraction
            all_links = re.findall(r'<a[^>]*href="([^"]*releases[^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)
            for href, text in all_links[:10]:
                clean = re.sub(r'<[^>]+>', ' ', text).strip()
                if len(clean) > 20:
                    print(f"  {href}: {clean[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    print()
