#!/usr/bin/env python3
"""Search for secondary source verification of the gut bacteria aging study.
Uses DuckDuckGo HTML and extracts result links."""
import subprocess, re, sys

query = sys.argv[1]
ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", ua, url], capture_output=True)
html = p.stdout.decode("utf-32", errors="replace") if False else p.stdout.decode("utf-8", errors="replace")
# Extract result links and snippets
results = re.findall(r'class="result__a"[^>]*href="(.*?)"[^>]*>(.*?)</a>', html, re.DOTALL)
snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</span>', html, re.DOTALL)
print(f"Query: {query}")
print(f"URL: {url}")
print(f"Results found: {len(results)}")
print(f"Snippets found: {len(snippets)}")
for i, (link, title) in enumerate(results[:8]):
    clean_title = re.sub(r"<[^>]+>", "", title).strip()
    snippet = ""
    if i < len(snippets):
        snippet = re.sub(r"<[^>]+>", "", snippets[i]).strip()[:200]
    print(f"\n--- Result {i+1} ---")
    print(f"Link: {link}")
    print(f"Title: {clean_title}")
    print(f"Snippet: {snippet}")
