#!/usr/bin/env python3
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try fetching the PNAS article abstract
url = "https://www.pnas.org/doi/10.1073/pnas.2618030123"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout.decode('utf-8', errors='replace')
full_text = re.sub(r'<[^>]+>', ' ', data)
full_text = re.sub(r'\s+', ' ', full_text).strip()

# Look for abstract, title, key facts
for kw in ["Abstract", "Portia", "REM", "sleep", "spider", "Bonn"]:
    idx = full_text.lower().find(kw.lower())
    if idx >= 0:
        snippet = full_text[max(0,idx-50):idx+300]
        print(f"Found '{kw}': ...{snippet}...")
        print("---")
        break  # Just get first match