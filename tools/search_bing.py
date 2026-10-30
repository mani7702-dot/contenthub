#!/usr/bin/env python3
"""Search DuckDuckGo and print raw HTML for debugging."""
import subprocess, re, sys

query = sys.argv[1]
ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", ua, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
# Look for result links
links = re.findall(r'href="(https?://[^"]+)"', html)
print(f"Query: {query}")
print(f"Total chars: {len(html)}")
print(f"Links found: {len(links)}")
for l in links[:15]:
    print(f"  {l}")
# Also try Bing
print("\n--- Trying Bing ---")
url2 = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
p2 = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", ua, url2], capture_output=True)
html2 = p2.stdout.decode("utf-8", errors="replace")
links2 = re.findall(r'href="(https?://[^"]+)"', html2)
print(f"Bing total chars: {len(html2)}")
print(f"Bing links found: {len(links2)}")
for l in links2[:15]:
    print(f"  {l}")
