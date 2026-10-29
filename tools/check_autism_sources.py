#!/usr/bin/env python3
"""Fetch the Yale press release for the autism brain study."""
import requests
import re

# The ScienceDaily article mentions the paper is at DOI 10.1038/s44220-026-00672-y
# Let's check the University of Houston press office for Jason Griffin
urls = [
    "https://www.sciencedaily.com/releases/2026/10/261027063824.htm",
    "https://hubresearch.com/news/2026/10/20/how-autistic-brains-process-faces-differently",  # try UH
]

headers = {"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"}

# Try to find a Yale news story
import urllib.parse
search_urls = [
    "https://news.yale.edu/search?keywords=autism+faces+brain",
    "https://news.yale.edu/search?keywords=face+processing+autism",
]

for su in search_urls:
    try:
        r = requests.get(su, headers=headers, timeout=15)
        links = re.findall(r'href="(/news/\d+/[^"]*)"', r.text)
        for link in links[:20]:
            print(f"Found link: {link}")
    except Exception as e:
        print(f"Error fetching {su}: {e}")

# Try the Nature article via DOI redirect
try:
    r = requests.get("https://doi.org/10.1038/s44220-026-00672-y", headers=headers, timeout=15, allow_redirects=True)
    print(f"\nNature DOI Status: {r.status_code}")
    print(f"Final URL: {r.url}")
    title = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE|re.DOTALL)
    if title:
        print(f"Title: {title.group(1).strip()[:200]}")
except Exception as e:
    print(f"Nature DOI Error: {e}")

# Try pubmed
try:
    r = requests.get("https://pubmed.ncbi.nlm.nih.gov/?term=autism+face+processing+EEG+McPartland", headers=headers, timeout=15)
    print(f"\nPubMed Status: {r.status_code}")
    titles = re.findall(r'<a[^>]*class="docsum-title"[^>]*>(.*?)</a>', r.text, re.DOTALL)
    for t in titles[:5]:
        text = re.sub(r'<[^>]+>', '', t).strip()
        text = re.sub(r'\s+', ' ', text)
        print(f"  PubMed: {text[:200]}")
except Exception as e:
    print(f"PubMed Error: {e}")
