#!/usr/bin/env python3
"""Extract article body from GNN lunch tab story."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andgu722@gmail.com)"
url = "https://www.goodnewsnetwork.org/stranger-anonymously-pays-420-lunch-tab-for-27-disabled-residents-and-caregivers/"
r = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True)
text = r.stdout.decode("utf-8", errors="replace")

# Look for the description from the RSS / Open Graph
for field in ["og:description", "og:title", "twitter:description"]:
    match = re.search(rf'<meta property="{field}" content="(.*?)"', text)
    if match:
        print(f"{field}: {match.group(1)[:300]}")

# Try to find the article entry-content
# Look between common article content markers
content_match = re.search(r'<div class="td-post-content">(.*?)</div>', text, re.DOTALL)
if content_match:
    clean = re.sub(r'<[^>]+>', ' ', content_match.group(1))
    clean = re.sub(r'\s+', ' ', clean)
    print("\n=== Article Content ===")
    print(clean[:3000])
else:
    # Try entry-content class
    content_match = re.search(r'class="entry-content"(.*?)</div>', text, re.DOTALL)
    if content_match:
        clean = re.sub(r'<[^>]+>', ' ', content_match.group(1))
        clean = re.sub(r'\s+', ' ', clean)
        print("\n=== Article Content (entry-content) ===")
        print(clean[:3000])
    else:
        print("\nNo article content div found")
        # Try to find paragraphs with specific text
        pars = re.findall(r'<p>(.*?)</p>', text, re.DOTALL)
        for p in pars:
            clean = re.sub(r'<[^>]+>', '', p).strip()
            if len(clean) > 50 and not clean.startswith("Sign in") and not clean.startswith("Welcome"):
                print(f"\n  Para: {clean[:500]}")
