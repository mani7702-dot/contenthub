#!/usr/bin/env python3
"""Try to find secondary sources for the knitted traffic cops story."""
import subprocess, re, urllib.parse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Try DuckDuckGo Lite search
url = "https://lite.duckduckgo.com/lite/?q=Fillongley+knitted+traffic+cops+slowing+speeding+drivers"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
print(f"DuckDuckGo length: {len(r.stdout)}")

# Extract result links from DDG
links = re.findall(r'res="[^"]*"[^>]*>(.*?)</a>', r.stdout, re.DOTALL)
for l in links[:10]:
    text = re.sub(r"<[^>]+>", "", l).strip()
    if text and "duckduckgo" not in text.lower():
        print(f"  Result: {text[:150]}")

# Also look for any URLs
all_urls = re.findall(r'https?://[^\s<>"\']+', r.stdout)
relevant = [u for u in all_urls if "duckduckgo" not in u.lower()]
print(f"\nAll relevant URLs ({len(relevant)}):")
for u in relevant[:10]:
    print(f"  -> {u[:150]}")

# Try Bing
print("\n=== Bing search ===")
url = "https://www.bing.com/search?q=Fillongley+knitted+traffic+cops+slowing+speeding+drivers"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
print(f"Bing length: {len(r.stdout)}")
# Extract visible text
text = re.sub(r"<script[^>]*>.*?</script>", "", r.stdout, flags=re.DOTALL)
text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
text = re.sub(r"<[^>]+>", " ", text)
text = re.sub(r"\s+", " ", text).strip()
# Find knitted mentions
idx = 0
while True:
    idx = text.lower().find("knitted", idx)
    if idx < 0:
        break
    print(f"  Context: ...{text[max(0,idx-80):idx+150]}...")
    idx += 1
