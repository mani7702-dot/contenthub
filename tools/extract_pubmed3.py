import re

with open('/tmp/pubmed_search.html', 'r') as f:
    html = f.read()

# Find article links and titles
links = re.findall(r'/pubmed/(\d+)', html)
print(f"PMIDs found: {links[:10]}")

# Find titles
titles = re.findall(r'<a href="/pubmed/\d+.*"[^>]*>([^<]+)</a>', html)
for t in titles[:10]:
    if 'sweet' in t.lower() or 'cognitive' in t.lower() or 'neurology' in t.lower():
        print(f"TITLE: {t.strip()}")

# Search for the DOI
dois = re.findall(r'10\.\d+/[^\s"<>]+', html)
print(f"\nDOIs: {dois[:10]}")

# Find PMID for sweetener study
for kw in ['sweetener', 'cognitive decline', 'Neurology']:
    idxs = [m.start() for m in re.finditer(kw, html, re.IGNORECASE)]
    for idx in idxs[:3]:
        context = re.sub(r'<[^>]+>', ' ', html[max(0,idx-100):idx+200])
        context = re.sub(r'\s+', ' ', context)
        print(f"\n--- '{kw}' at {idx} ---")
        print(context[:200])
