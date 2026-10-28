#!/usr/bin/env python3
"""Cross-check: find the McGill University press release for the T-cell stiffness study."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try McGill press release site and Google Scholar
urls = [
    "https://www.mcgill.ca/news/science/2026/10/26/how-immune-cells-feel-their-surroundings",
    "https://www.nature.com/articles/s41590-026-0255-9",
    "https://www.nature.com/articles/s41590-026-0255-0",
]
for url in urls:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    p = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, url], capture_output=True)
    text = p.stdout.decode("utf-8", errors="replace")
    print(f"Length: {len(text)} chars")
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    # Look for relevant text about T cells and stiffness
    for kw in ["stiff", "stiffness", "T cell", "memory T cell", "collagen gel", "McGill"]:
        idx = clean.lower().find(kw.lower())
        if idx > 0:
            print(f"--- Around \"{kw}\" (pos {idx}) ---")
            print(clean[max(0, idx-100):idx+500])
            print()
