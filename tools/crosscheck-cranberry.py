#!/usr/bin/env python3
"""Cross-check: Fetch the original journal article and UIC press page for cranberry research."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Search for the research on UIC website
urls_to_check = [
    "https://uicedu.com/news/2026/10/cranberry-juice-tooth-decay",
    "https://today.uic.edu/cranberry-juice-tooth-decay",
]

# Also try a web search via DuckDuckGo lite for cranberry juice tooth decay University of Illinois Chicago
search_url = "https://lite.duckduckgo.com/lite/?q=cranberry+juice+tooth+decay+University+Illinois+Chicago+Wu"
result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, search_url], capture_output=True, text=True)
html = result.stdout

# Extract links and text
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
# Get result snippets
snippets = re.findall(r'<td[^>]*class=["\'][^"\']*result-snippet[^"\']*["\'][^>]*>(.*?)</td>', text, re.DOTALL | re.IGNORECASE)
links = re.findall(r'<a[^>]*href="(https?://[^"]+)"[^>]*class=["\'][^"\']*result-link[^"\']*["\']', text, re.IGNORECASE)

print("DuckDuckGo search results for 'cranberry juice tooth decay University of Illinois Chicago Wu':")
print()
for i, s in enumerate(snippets[:15]):
    clean = re.sub(r'<[^>]+>', '', s).strip()
    if len(clean) > 20:
        print(f"  [{i+1}] {clean[:300]}")
        print()

print(f"\nResult links found: {len(links)}")
for l in links[:10]:
    print(f"  {l}")

# Also try searching for the journal publication
search_url2 = "https://lite.duckduckgo.com/lite/?q=%22cranberry+juice%22+%22tooth+decay%22+%22University+of+Illinois%22+journal"
result2 = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, search_url2], capture_output=True, text=True)
html2 = result2.stdout
text2 = re.sub(r'<script[^>]*>.*?</script>', '', html2, flags=re.DOTALL | re.IGNORECASE)
text2 = re.sub(r'<style[^>]*>.*?</style>', '', text2, flags=re.DOTALL | re.IGNORECASE)
snippets2 = re.findall(r'<td[^>]*class=["\'][^"\']*result-snippet[^"\']*["\'][^>]*>(.*?)</td>', text2, re.DOTALL | re.IGNORECASE)

print("\n\nDuckDuckGo search results for 'cranberry juice tooth decay University of Illinois journal':")
for i, s in enumerate(snippets2[:15]):
    clean = re.sub(r'<[^>]+>', '', s).strip()
    if len(clean) > 20:
        print(f"  [{i+1}] {clean[:300]}")
        print()
