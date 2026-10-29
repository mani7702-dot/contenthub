#!/usr/bin/env python3
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.sciencedaily.com/releases/2026/10/261026225555.htm"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout.decode('utf-8', errors='replace')

# Extract the main content - look for the article body
# ScienceDaily articles have the content in <div id="text-body"> or similar
import re

# Get all paragraph text
paras = re.findall(r'<p[^>]*>(.*?)</p>', data, re.DOTALL)
for para in paras:
    text = re.sub(r'<[^>]+>', '', para).strip()
    if len(text) > 30:
        print(text)
        print("---")