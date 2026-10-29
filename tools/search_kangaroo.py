#!/usr/bin/env python3
"""Search DuckDuckGo HTML for a second source on the kangaroo rescue."""
import re, urllib.parse, subprocess

query = urllib.parse.quote("kangaroo rescued sea diver Boston Bay South Australia")
url = f"https://html.duckduckgo.com/html/?q={query}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
p = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="ignore")

links = re.findall(r'result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
snippets = re.findall(r'result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)

print("=== DuckDuckGo Results ===")
for i, (link, title, snip) in enumerate(zip(links[:8], snippets[:8], snippets[:8])):
    clean_title = re.sub(r'<[^>]+>', '', title).strip()
    clean_snip = re.sub(r'<[^>]+>', '', snip).strip() if snip else ""
    print(f"  {i+1}. {clean_title}")
    print(f"     url: {link}")
    print(f"     snip: {clean_snip[:200]}")
