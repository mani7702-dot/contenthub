#!/usr/bin/env python3
"""Cross-check the lunch tab story - fetch GNN article and find another source."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Fetch the GNN article
url = "https://www.goodnewsnetwork.org/anonymously-pays-dinner-tab-for-27-disability-staff-in-south-korea/"
r = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True)
text = r.stdout.decode("utf-8", errors="replace")

# Extract OG meta tags
for field in ["og:title", "og:description", "og:image"]:
    match = re.search(rf'<meta property="{field}" content="(.*?)"', text)
    if match:
        print(f"{field}: {match.group(1)[:300]}")

# Try to find article content paragraphs
# GNN uses td-post-content
content_match = re.search(r'class="td-post-content">(.*?)</div>\s*</div>', text, re.DOTALL)
if not content_match:
    content_match = re.search(r'class="td-post-content">(.*?)(?:</div>\s*</div>|<div class=")', text, re.DOTALL)

if content_match:
    clean = re.sub(r'<[^>]+>', '\n', content_match.group(1))
    clean = re.sub(r'\n\s*\n', '\n', clean)
    clean = re.sub(r'\n{3,}', '\n\n', clean)
    print("\n=== Article Content ===")
    print(clean[:3000])
else:
    # Try finding paragraphs
    pars = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
    print(f"\nFound {len(pars)} paragraphs")
    for i, p in enumerate(pars):
        clean = re.sub(r'<[^>]+>', '', p).strip()
        clean = re.sub(r'\s+', ' ', clean)
        if len(clean) > 60 and not clean.startswith("Sign in") and not clean.startswith("Welcome") and not clean.startswith("Cookie"):
            print(f"\nP{i}: {clean[:500]}")
            if i > 20:
                break
