#!/usr/bin/env python3
"""Fetch paper details from CrossRef and Semantic Scholar."""
import subprocess, re, json, time

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Crossref - use the works endpoint differently
crossref_url = "https://api.crossref.org/works/10.1038/s41590-026-02581-9"
print(f"Crossref URL: {crossref_url}")
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, crossref_url], capture_output=True)
text = p.stdout.decode("utf-8", errors="replace")
print(f"Length: {len(text)} chars")
if text:
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
            print(f"Abstract: {abstract[:2500]}")
    except Exception as e:
        print(f"Error: {e}")
        print(text[:500])

# Also try Semantic Scholar with the DOI
print("\n\n=== Semantic Scholar ===")
time.sleep(3)  # avoid rate limit
ss_url = "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/s41590-026-02581-9?fields=title,authors,year,abstract,externalIds,url,journal"
p2 = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, ss_url], capture_output=True)
text2 = p2.stdout.decode("utf-8", errors="replace")
print(f"SS Response length: {len(text2)} chars")
if text2:
    try:
        data2 = json.loads(text2)
        print(f"Title: {data2.get('title', '')}")
        print(f"Year: {data2.get('year', '')}")
        print(f"Journal: {data2.get('journal', {}).get('name', '')}")
        authors = data2.get("authors", [])
        for a in authors:
            print(f"  Author: {a.get('name', '')}")
        print(f"URL: {data2.get('url', '')}")
        abstract = data2.get("abstract", "")
        if abstract:
            print(f"Abstract: {abstract[:2500]}")
    except Exception as e:
        print(f"Error: {e}")
        print(text2[:500])
