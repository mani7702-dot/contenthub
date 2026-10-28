#!/usr/bin/env python3
"""Find the Nature Immunology paper for the T-cell stiffness study."""
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
# Try PubMed search
queries = [
    "https://pubmed.ncbi.nlm.nih.gov/?term=t+cell+tissue+stiffness+microbiome+aging+mandl",
    "https://pubmed.ncbi.nlm.nih.gov/?term=t+cell+sense+stiffness+tissue+memory+nature+immunology+2026",
]
for url in queries:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True)
    text = p.stdout.decode("utf-8", errors="replace")
    import re
    # Extract article titles and links
    links = re.findall(r'<a[^>]*href="(/pubmed/\d+)"[^>]*>(.*?)</a>', text, re.S)
    for href, title in links[:15]:
        title = re.sub(r'<[^>]+>', '', title).strip()
        title = re.sub(r'\s+', ' ', title)
        if len(title) > 10:
            print(f"  https://pubmed.ncbi.nlm.nih.gov{href} - {title[:100]}")
