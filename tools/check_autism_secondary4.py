#!/usr/bin/env python3
"""Find and fetch secondary sources via Bing News."""
import requests
import re

headers = {"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"}

# Bing News search
bing_url = "https://www.bing.com/news/search?q=autism+face+processing+brain+yale+nature+mental+health"
try:
    r = requests.get(bing_url, headers=headers, timeout=15)
    print(f"Bing News Status: {r.status_code}")
    # Extract article snippets and links
    # Bing News cards
    links = re.findall(r'href="(https?://[^"]+)"', r.text)
    scitech_links = [l for l in links if 'scitechdaily' in l.lower()]
    yale_links = [l for l in links if 'yale' in l.lower() and 'edu' in l.lower()]
    medical_links = [l for l in links if 'medicaldaily' in l.lower()]
    print(f"  SciTech links: {scitech_links[:3]}")
    print(f"  Yale links: {yale_links[:3]}")
    print(f"  MedicalDaily links: {medical_links[:3]}")

    # Extract snippets
    snippets = re.findall(r'<p[^>]*>(.*?)</p>', r.text, re.DOTALL)
    for s in snippets:
        text = re.sub(r'<[^>]+>', '', s).strip()
        text = re.sub(r'\s+', ' ', text)
        if 'autism' in text.lower() and 'face' in text.lower() and len(text) > 50:
            print(f"  Snippet: {text[:300]}")
except Exception as e:
    print(f"Bing error: {e}")

# Try fetching the ScienceDaily article for the related story about the N170
try:
    r = requests.get("https://www.sciencedaily.com/releases/2026/10/261027063824.htm", headers=headers, timeout=20)
    # Extract the "RELATED STORIES" section
    related = re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r.text, re.DOTALL)
    for href, title in related:
        if 'releases' in href and ('autism' in title.lower() or 'face' in title.lower() or 'brain' in title.lower()):
            text = re.sub(r'<[^>]+>', '', title).strip()
            print(f"Related story: {text[:150]} -> {href}")
except Exception as e:
    print(f"Related stories error: {e}")
