#!/usr/bin/env python3
"""Search for stories using DuckDuckGo HTML and parse results."""
import subprocess, sys, re, urllib.parse

query = sys.argv[1]
encoded = urllib.parse.quote(query)
url = f"https://html.duckduckgo.com/html/?q={encoded}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, "--compressed", url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Extract result snippets
results = re.findall(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet">(.*?)</span>', html, re.DOTALL | re.IGNORECASE)

if not results:
    # Try alternative parsing
    results = re.findall(r'href="(https?://[^"]+)"[^>]*>(.*?)</a>.*?result__snippet.*?>(.*?)</span>', html, re.DOTALL | re.IGNORECASE)

for link, title, snippet in results[:8]:
    clean_title = re.sub(r'<[^>]+>', '', title).strip()
    clean_snippet = re.sub(r'<[^>]+>', '', snippet).strip()
    # Skip DDG redirect links
    if "duckduckgo.com" in link:
        continue
    print(f"Title: {clean_title}")
    print(f"URL: {link}")
    print(f"Snippet: {clean_snippet[:200]}")
    print()

if not results:
    print("No results found from DDG")
    # Print a snippet of the HTML to debug
    print("HTML preview:", html[:500])
