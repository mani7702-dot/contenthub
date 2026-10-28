#!/usr/bin/env python3
"""Find the Nature Immunology paper on T cell stiffness via crossref API."""
import subprocess, re, json

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Use Crossref API to search for the paper
crossref_url = "https://api.crossref.org/works?query.bibliographic=t+cell+stiffness+tissue+memory+mandl&query.container-title=Nature+Immunology&rows=5"
print(f"Crossref URL: {crossref_url}")
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, crossref_url], capture_output=True)
text = p.stdout.decode("utf-8", errors="replace")
print(f"Response length: {len(text)} chars")

try:
    data = json.loads(text)
    items = data.get("message", {}).get("items", [])
    print(f"Found {len(items)} items")
    for item in items:
        title = item.get("title", [""])[0] if item.get("title") else ""
        doi = item.get("DOI", "")
        authors = item.get("author", [])
        author_str = ", ".join(f"{a.get('given', '')} {a.get('family', '')}" for a in authors)
        print(f"\n  Title: {title[:200]}")
        print(f"  DOI: {doi}")
        print(f"  Authors: {author_str[:200]}")
        print(f"  URL: {item.get('URL', '')}")
        print(f"  Published: {item.get('published', {}).get('date-parts', [['?']])[0]}")
        
        # Get abstract if available
        abstract = item.get("abstract", "")
        if abstract:
            abstract = re.sub(r'<[^>]+>', ' ', abstract)
            abstract = re.sub(r'\s+', ' ', abstract).strip()
            print(f"  Abstract: {abstract[:600]}")
except Exception as e:
    print(f"Error parsing JSON: {e}")
    print(text[:1000])
