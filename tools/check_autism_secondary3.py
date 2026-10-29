#!/usr/bin/env python3
"""Fetch secondary sources for the autism face processing study."""
import requests
import re

headers = {"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"}

# Get the Google News RSS feed URLs for the Yale and SciTechDaily articles
rss_url = "https://news.google.com/rss/search?q=autism+face+processing+brain+yale"
r = requests.get(rss_url, headers=headers, timeout=15)
links = re.findall(r'<link>(.*?)</link>', r.text)
print("RSS Links:")
for link in links:
    if 'sciencedaily' in link or 'yale' in link or 'medicaldaily' in link or 'sci-tech' in link:
        print(f"  {link.strip()}")

# Fetch the Yale news article
yale_urls = [
    "https://news.yale.edu/how-autistic-brains-process-faces-differently",
    "https://news.yale.edu/2026/10/27/how-autistic-brains-process-faces-differently",
]
for yu in yale_urls:
    try:
        r = requests.get(yu, headers=headers, timeout=15, allow_redirects=True)
        print(f"\nYale URL: {yu}")
        print(f"  Status: {r.status_code}")
        print(f"  Final URL: {r.url}")
        title = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE|re.DOTALL)
        if title:
            print(f"  Title: {title.group(1).strip()[:200]}")
        body = re.sub(r'<[^>]+>', ' ', r.text)
        body = re.sub(r'\s+', ' ', body).strip()
        if 'autism' in body.lower() and 'face' in body.lower():
            idx = body.lower().find('autism')
            print(f"  Excerpt: {body[max(0,idx-50):idx+300]}...")
    except Exception as e:
        print(f"Yale error for {yu}: {e}")

# Fetch SciTechDaily
try:
    r = requests.get("https://scitechdaily.com/autistic-brains-process-faces-differently/", headers=headers, timeout=15)
    print(f"\nSciTechDaily Status: {r.status_code}")
    if r.status_code == 200:
        title = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE|re.DOTALL)
        if title:
            print(f"  Title: {title.group(1).strip()[:200]}")
        body = re.sub(r'<[^>]+>', ' ', r.text)
        body = re.sub(r'\s+', ' ', body).strip()
        idx = body.lower().find('autism')
        if idx > 0:
            print(f"  Excerpt: {body[max(0,idx-50):idx+400]}...")
except Exception as e:
    print(f"SciTechDaily error: {e}")
