#!/usr/bin/env python3
"""Extract full article text from MedicalDaily."""
import requests
import re

headers = {"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"}

url = "https://www.medicaldaily.com/autism-eeg-face-processing-brain-signals-yale-study-476856"
r = requests.get(url, headers=headers, timeout=20)

# Extract article body
body = re.sub(r'<[^>]+>', ' ', r.text)
body = re.sub(r'\s+', ' ', body).strip()

# Find the main article content - look for the writer attribution
start = body.find("Yale Study Finds Face-Related Brain Signals")
if start > 0:
    # Get everything from the title onward
    content = body[start:start+3000]
    print(content)
