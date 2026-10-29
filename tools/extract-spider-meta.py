#!/usr/bin/env python3
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.sciencedaily.com/releases/2026/10/261026225555.htm"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout.decode('utf-8', errors='replace')

# Look for journal name and DOI
# ScienceDaily typically has a "JournalReference" or similar
matches = re.findall(r'<[^>]*>(.*?)</[^>]*>', data, re.DOTALL)
full_text = re.sub(r'<[^>]+>', ' ', data)
# Collapse whitespace
full_text = re.sub(r'\s+', ' ', full_text).strip()

# Find journal/doi references
for kw in ["Nature", "Science", "Current Biology", "PNAS", "DOI", "journal", "Proceedings"]:
    idx = full_text.lower().find(kw.lower())
    if idx >= 0:
        snippet = full_text[max(0,idx-50):idx+200]
        print(f"Found '{kw}': ...{snippet}...")
        print("---")