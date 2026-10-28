#!/usr/bin/env python3
"""Fetch the Nature paper abstract and key details."""
import subprocess, re, json

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Fetch the Nature article
urls = [
    "https://api.crossref.org/works/10.1038/s41590-026-02581-9",
    "https://www.nature.com/articles/s41590-026-02581-9",
]

for url in urls:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    p = subprocess.run(["curl", "-s", "-L", "--max-time", "--max-time", "25", "-A", UA, url], capture_output=True)
    text = p.stdout.decode("utf-8", errors="replace")
    print(f"Length: {len(text)} chars")
    
    # Check if it's JSON (crossref) or HTML (nature)
    if url.startswith("https://api.crossref"):
        try:
            data = json.loads(text)
            item = data.get("message", {})
            print(f"Title: {item.get('title', [''])[0]}")
            print(f"DOI: {item.get('DOI', '')}")
            authors = item.get("author", [])
            for a in authors:
                print(f"  Author: {a.get('given', '')} {a.get('family', '')}")
            print(f"Container: {item.get('container-title', [''])[0]}")
            print(f"Published: {item.get('published', {}).get('date-parts', [['?']])[0]}")
            abstract = item.get("abstract", "")
            if abstract:
                abstract = re.sub(r'<[^>]+>', ' ', abstract)
                abstract = re.sub(r'\s+', ' ', abstract).strip()
                print(f"Abstract: {abstract[:2000]}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        clean = re.sub(r'<[^>]+>', ' ', text)
        clean = re.sub(r'\s+', ' ', clean).strip()
        # Look for abstract
        for kw in ["abstract", "stiff", "mechanosens", "tissue-resident", "collagen"]:
            idx = clean.lower().find(kw.lower())
            if idx > 0:
                print(f"\n--- Around \"{kw}\" ---")
                print(clean[max(0, idx-50):idx+1000])
                print()
