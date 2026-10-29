#!/usr/bin/env python3
"""Search for a story across multiple news sources using DuckDuckGo."""
import subprocess, sys, re, urllib.parse

query = sys.argv[1]
encoded = urllib.parse.quote(query)
url = f"https://html.duckduckgo.com/html/?q={encoded}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Extract result links and snippets
results = re.findall(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</span>', html, re.DOTALL)

for i, (link, title) in enumerate(results[:10]):
    clean_title = re.sub(r'<[^>]+>', '', title).strip()
    clean_link = link.strip()
    snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ""
    print(f"Title: {clean_title}")
    print(f"URL: {clean_link}")
    print(f"Snippet: {snippet[:200]}")
    print()
