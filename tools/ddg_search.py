#!/usr/bin/env python3
"""Search DuckDuckGo for the wedding ring hobbits story."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://html.duckduckgo.com/html/?q=patrick+mohr+italian+hobbits+wedding+ring+ireland+glendalough"
r = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
html = r.stdout
print(f"Fetched {len(html)} bytes")

# Extract result links and snippets
# DDG HTML results have result links in <a class="result__a" href="...">
links = re.findall(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
snippets = re.findall(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)

print(f"\n=== {len(links)} results ===")
for i, (link, title) in enumerate(zip(links[:10], snippets[:10] if snippets else [""]*10)):
    title_clean = re.sub(r"<[^>]+>", "", title).strip()
    snippet_clean = re.sub(r"<[^>]+>", "", snippets[i]).strip() if i < len(snippets) else ""
    print(f"\n[{i+1}] {title_clean}")
    print(f"    URL: {link}")
    print(f"    Snippet: {snippet_clean[:300]}")
