#!/usr/bin/env python3
"""Try Wayback Machine and other sources for the lunch tab story."""
import subprocess, json, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try Wayback Machine CDX API to find archived snapshots
url = "https://www.goodnewsnetwork.org/stranger-anonymously-pays-420-lunch-tab-for-27-disabled-residents-and-caregivers/"
api_url = f"https://web.archive.org/cdx/search/cdx?url={url}&output=json&limit=3"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, api_url], capture_output=True, text=True)
print("=== Wayback CDX ===")
print(r.stdout[:2000])

# Also check if there's a known article via web search
# Let's try fetching the article directly with content extraction
r2 = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True)
text = r2.stdout.decode("utf-8", errors="replace")
# Try to extract content between article tags or known divs
# Look for the actual story content
for pattern in [
    r'\$420.*?resident',
    r'27.*?disabled.*?caregiver',
    r'anonymously.*?pay',
    r'lunch tab.*?caregiver',
]:
    matches = re.findall(pattern, text, re.I | re.DOTALL)
    if matches:
        print(f"\n=== Match for {pattern[:30]}... ===")
        for m in matches[:1]:
            clean = re.sub(r'<[^>]+>', ' ', m)
            clean = re.sub(r'\s+', ' ', clean)
            print(clean[:1000])

# Also try to find the article in the JSON data in the page
json_match = re.search(r'td_data\\":\\"(.*?)\\",\\"td_block_id', text)
if json_match:
    print("\n=== From page JSON ===")
    print(json_match.group(0)[:500])

print(f"\nPage length: {len(text)}")
