#!/usr/bin/env python3
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Get Wikipedia article on Portia fimbriata for cross-checking
url = "https://en.wikipedia.org/wiki/Portia_(spider)"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout.decode('utf-8', errors='replace')

# Extract text content
full_text = re.sub(r'<[^>]+>', ' ', data)
full_text = re.sub(r'\s+', ' ', full_text).strip()

# Look for sleep/REM references
for kw in ["sleep", "REM", "jumping", "cognitive", "hunt"]:
    idx = full_text.lower().find(kw.lower())
    if idx >= 0:
        snippet = full_text[max(0,idx-30):idx+300]
        print(f"Found '{kw}': ...{snippet}...")
        print("---")