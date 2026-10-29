#!/usr/bin/env python3
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Fetch the ScienceDaily article and look for the full journal reference and story source
url = "https://www.sciencedaily.com/releases/2026/10/261026225555.htm"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout.decode('utf-8', errors='replace')
full_text = re.sub(r'<[^>]+>', ' ', data)
full_text = re.sub(r'\s+', ' ', full_text).strip()

# Find "Journal Reference"
idx = full_text.find("Journal Reference")
if idx >= 0:
    print(full_text[idx:idx+500])
print("\n=== Story Source ===")
idx = full_text.find("Story Source")
if idx >= 0:
    print(full_text[idx:idx+300])

print("\n=== Full Citation ===")
# Find the full citation info
idx = full_text.find("PNAS")
if idx >= 0:
    print(full_text[max(0,idx-200):idx+400])