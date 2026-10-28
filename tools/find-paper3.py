#!/usr/bin/env python3
"""Find the Nature Immunology paper by searching for Judith Mandl + stiffness."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try Nature Immunology October 2026 issue (volume 27)
for vol_issue in ["https://www.nature.com/ni/volumes/27/issues/10", "https://www.nature.com/ni/volumes/27/issues/11"]:
    print(f"\n{'='*60}")
    print(f"URL: {vol_issue}")
    print(f"{'='*60}")
    p = subprocess.run(["curl", "-s", "-L", "--max-time", "--max-time", "25", "-A", UA, vol_issue], capture_output=True)
    text = p.stdout.decode("utf-8", errors="replace")
    
    # Extract all article links
    for m in re.finditer(r'href="(/articles/s41590-[^"]+)"', text):
        link = m.group(1)
        # Get the title text near this link
        start = max(0, m.start() - 200)
        end = min(len(text), m.end() + 200)
        nearby = re.sub(r'<[^>]+>', ' ', text[start:end])
        nearby = re.sub(r'\s+', ' ', nearby).strip()
        print(f"  https://www.nature.com{link}")
        print(f"    Context: {nearby[:200]}")

# Try Nature search with author name
search_url = "https://www.nature.com/search?query=Judith+Mandl+tissue+stiffness"
print(f"\n{'='*60}")
print(f"Searching: {search_url}")
print(f"{'='*60}")
p = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, search_url], capture_output=True)
text = p.stdout.decode("utf-8", errors="replace")
clean = re.sub(r'<[^>]+>', '\n', text)
lines = [l.strip() for l in clean.split('\n') if l.strip() and len(l.strip()) > 20]
for line in lines:
    if 'mandl' in line.lower() or 'stiff' in line.lower() or 'tissue' in line.lower() or 't cell' in line.lower():
        print(f"  {line[:200]}")
