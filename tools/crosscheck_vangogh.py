#!/usr/bin/env python3
"""Cross-check the Van Gogh Starry Night astronomy study."""
import re
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Search for secondary sources confirming this study
urls = [
    "https://www.sllab.co.kr/en",  # SLLAB website
    "https://www.nature.com/articles/s41598-026-12345-w",  # Scientific Reports (placeholder)
]

# Search for the study via DuckDuckGo HTML
search_url = "https://html.duckduckgo.com/html/?q=van+gogh+starry+night+hyades+taurus+study+2026"
result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, search_url], capture_output=True)
html = result.stdout.decode('utf-8', errors='replace')

# Extract search results
results = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*class="result__a"[^>]*>(.*?)</a>', html, re.IGNORECASE)
if not results:
    results = re.findall(r'href="(https?://[^"]+)"[^>]*>(.*?)</a>', html)
    # Filter for relevant
    results = [(r[0], r[1]) for r in results if any(k in r[1].lower() for k in ['van gogh', 'starry', 'hyades', 'taurus', 'scientific'])]

for url, title in results[:10]:
    clean_title = re.sub(r'<[^>]+>', '', title).strip()
    print(f"  {clean_title[:100]}")
    print(f"  URL: {url[:150]}\n")

# Also try Wikipedia for Hyades/Taurus
result2 = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "https://en.wikipedia.org/wiki/Hyades_(star_cluster)"], capture_output=True)
wiki = result2.stdout.decode('utf-8', errors='replace')
# Extract first few paragraphs
text = re.sub(r'<[^>]+>', ' ', wiki)
text = re.sub(r'\s+', ' ', text)
# Find relevant content
match = re.search(r'(Hyades.*?(?:open cluster|nearest|constellation|Taurus).*?(?:\.|!|\?))', text[:3000])
if match:
    print("Wikipedia Hyades:", match.group(1)[:300])
