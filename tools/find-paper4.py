#!/usr/bin/env python3
"""Find the McGill press release for the T-cell stiffness study."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try McGill news search
urls = [
    "https://www.mcgill.ca/news/science",
    "https://www.google.com/search?q=mcgill+university+judith+mandl+t+cell+stiffness+tissue+memory+nature+immunology",
]

for url in urls:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    p = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, url], capture_output=True)
    text = p.stdout.decode("utf-8", errors="replace")
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    print(f"Length: {len(text)} chars")
    
    # Look for relevant content
    for kw in ["stiffness", "T cell", "McGill", "Mandl", "tissue", "collagen"]:
        idx = clean.lower().find(kw.lower())
        if idx > 0:
            print(f"--- Found \"{kw}\" at pos {idx} ---")
            print(clean[max(0, idx-100):idx+400])
            print()

# Also try to find the DOI from the ScienceDaily article
# The article mentioned "published in Nature Immunology"
# Let's try to find the actual paper DOI
print("\n=== Trying to find paper via semantic scholar ===")
ss_url = "https://api.semanticscholar.org/graph/v1/paper/search?query=T+cell+tissue+stiffness+memory+Mandl&limit=5&fields=title,externalIds,url"
p2 = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, ss_url], capture_output=True)
text2 = p2.stdout.decode("utf-8", errors="replace")
print(f"Semantic Scholar response: {text2[:2000]}")
