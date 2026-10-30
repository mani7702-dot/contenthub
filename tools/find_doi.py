#!/usr/bin/env python3
"""Find and verify the Nature Scientific Reports article via DOI resolver and direct search."""
import subprocess, re, urllib.parse

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# The study was published in Scientific Reports (Nature portfolio)
# Authors: Alika K. Maunakea, Braden P. Kunihiro, Ruben Juarez - University of Hawaii
# Key facts to verify:
# 1. Bifidobacterium adolescentis -> slower aging
# 2. Succinivibrio dextrinosolvens -> faster aging
# 3. DunedinPACE biomarker used
# 4. ~15% of variation in biological aging rates
# 5. Blood + stool samples from 123 adults
# 6. Published in Scientific Reports (Nature portfolio)

# Try DOI resolver
print("=== Trying DOI resolver ===")
# We need to find the actual DOI. Let's try common patterns
# Scientific Reports 2026, likely DOI 10.1038/s41598-026-XXXXX-X
for doi_suffix in range(27000, 28400):
    doi = f"10.1038/s41598-026-{doi_suffix}"
    url = f"https://www.nature.com/articles/s41598-026-{doi_suffix}"
    p = subprocess.run(["curl", "-sL", "--max-time", "10", "-A", ua, "-o", "/dev/null", "-w", "%{http_code}", url], capture_output=True)
    status = p.stdout.decode().strip()
    if status == "200":
        print(f"  FOUND: {doi} -> {url} (status: {status})")
        # Fetch the actual page content
        p2 = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, url], capture_output=True)
        html = p2.stdout.decode("utf-8", errors="replace")
        title = re.search(r'<meta name="dc.title" content="(.*?)"', html)
        if not title:
            title = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
        if title:
            print(f"  Title: {title.group(1)[:200]}")
        description = re.search(r'<meta name="description" content="(.*?)"', html)
        if description:
            print(f"  Description: {description.group(1)[:200]}")
        # Check for key terms
        for term in ["Bifidobacterium", "Succinivibrio", "DunedinPACE", "123", "15%"]:
            if term.lower() in html.lower():
                print(f"  Found term: {term}")
        break
    # Print progress occasionally
    if doi_suffix % 50 == 0:
        print(f"  Checked up to {doi}...")

print("\n=== Trying Nature search API ===")
# Try the Nature articles API
api_url = "https://www.nature.com/nature/articlesapi/search?query=gut+microbiome+biological+aging+Maunakea&order=relevance&per_page=5"
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, api_url], capture_output=True)
print(f"API response: {p.stdout.decode()[:500]}")
