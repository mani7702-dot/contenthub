#!/usr/bin/env python3
"""Fetch MedicalDaily article for cross-checking."""
import requests
import re

headers = {"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"}

url = "https://www.medicaldaily.com/autism-eeg-face-processing-brain-signals-yale-study-476856"
try:
    r = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
    print(f"Status: {r.status_code}")
    print(f"Final URL: {r.url}")
    title = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE|re.DOTALL)
    if title:
        print(f"Title: {title.group(1).strip()[:200]}")

    body = re.sub(r'<[^>]+>', ' ', r.text)
    body = re.sub(r'\s+', ' ', body).strip()

    # Find relevant content
    for keyword in ['autism', 'face', 'EEG', '128', 'McPartland', 'neuron', 'brain signal', 'N170']:
        idx = body.lower().find(keyword.lower())
        if idx > 0:
            print(f"\n  '{keyword}' context: ...{body[max(0,idx-80):idx+300]}...")
except Exception as e:
    print(f"Error: {e}")
