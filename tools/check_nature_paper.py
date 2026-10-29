#!/usr/bin/env python3
"""Cross-check the autism brain study by fetching Nature Mental Health paper."""
import requests
import re

url = "https://www.nature.com/articles/s44220-026-00672-y"
headers = {"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"}

try:
    r = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
    print(f"Status: {r.status_code}")
    title = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE|re.DOTALL)
    if title:
        print(f"Title: {title.group(1).strip()[:300]}")

    # Find abstract
    abs_match = re.search(r'<div[^>]*class="[^"]*abstract[^"]*"[^>]*>(.*?)</div>', r.text, re.DOTALL|re.IGNORECASE)
    if abs_match:
        text = re.sub(r'<[^>]+>', ' ', abs_match.group(1))
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"Abstract: {text[:800]}")
    else:
        meta_desc = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]+)"', r.text, re.IGNORECASE)
        if meta_desc:
            print(f"Description: {meta_desc.group(1)[:300]}")

    r2 = requests.get(url, headers=headers, timeout=20)
    body_text = re.sub(r'<[^>]+>', ' ', r2.text)
    body_text = re.sub(r'\s+', ' ', body_text)
    if 'face' in body_text.lower():
        idx = body_text.lower().find('face')
        print(f"Context around 'face': ...{body_text[max(0,idx-100):idx+200]}...")

except Exception as e:
    print(f"Error: {e}")
