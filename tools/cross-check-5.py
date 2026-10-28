#!/usr/bin/env python3
"""Cross-check: Verify Fillongley is a real village in Warwickshire and Knit and Natter groups exist."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Verify Fillongley is a real village in Warwickshire via Wikipedia
url = "https://en.wikipedia.org/wiki/Fillongley"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
stdout = r.stdout
print(f"Wikipedia Fillongley: {len(stdout)} bytes")
text = re.sub(r"<[^>]+>", " ", stdout)
text = re.sub(r"\s+", " ", text).strip()
# Look for key facts
for term in ["Warwickshire", "Nuneaton", "village", "population"]:
    if term.lower() in text.lower():
        idx = text.lower().find(term.lower())
        print(f"  '{term}': {text[max(0,idx-30):idx+100]}")
    else:
        print(f"  '{term}': NOT FOUND")

# Verify Knit and Natter groups are real
print("\n=== Knit and Natter groups ===")
url = "https://en.wikipedia.org/wiki/Knit_and_Natter"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
stdout = r.stdout
print(f"Wikipedia Knit and Natter: {len(stdout)} bytes")
if len(stdout) > 0:
    text = re.sub(r"<[^>]+>", " ", stdout)
    text = re.sub(r"\s+", " ", text).strip()
    for term in ["United Kingdom", "pub", "knitting", "social group"]:
        if term.lower() in text.lower():
            idx = text.lower().find(term.lower())
            print(f"  '{term}': {text[max(0,idx-30):idx+100]}")

# Verify 30 mph speed limit signs are standard in UK
print("\n=== UK 30 mph signs ===")
url = "https://en.wikipedia.org/wiki/Speed_limit_in_the_United_Kingdom"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
stdout = r.stdout
print(f"Wikipedia UK speed limits: {len(stdout)} bytes")
text = re.sub(r"<[^>]+>", " ", stdout)
text = re.sub(r"\s+", " ", text).strip()
for term in ["30 mph", "30 mph", "built-up"]:
    if term.lower() in text.lower():
        idx = text.lower().find(term.lower())
        print(f"  '{term}': {text[max(0,idx-30):idx+100]}")

# Try fetching the GNN article again to verify it's still accessible
print("\n=== GNN article verification ===")
url = "https://www.goodnewsnetwork.org/village-installs-knitted-traffic-cops-to-slow-speeding-drivers/"
r = subprocess.run(["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}|%{size_download}",
                    "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
print(f"GNN article HTTP status: {r.stdout}")
