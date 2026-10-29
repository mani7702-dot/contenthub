#!/usr/bin/env python3
"""Search for a second source for the lightning proposal story."""
import subprocess, re, urllib.parse

# Search via DuckDuckGo HTML
query = urllib.parse.quote("Nick Broderick Eva lightning struck Kettle Moraine propose")
url = f"https://html.duckduckgo.com/html/?q={query}"
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="ignore")

# Extract result snippets
links = re.findall(r'result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
snippets = re.findall(r'result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)

print("=== DuckDuckGo Results ===")
for i, (link, title, snip) in enumerate(zip(links[:8], snippets[:8], snippets[:8])):
    clean_title = re.sub(r'<[^>]+>', '', title).strip()
    clean_snip = re.sub(r'<[^>]+>', '', snip).strip() if snip else ""
    print(f"  {i+1}. {clean_title}")
    print(f"     url: {link}")
    print(f"     snip: {clean_snip[:150]}")
