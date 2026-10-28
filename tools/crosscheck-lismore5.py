#!/usr/bin/env python3
"""Cross-check: DuckDuckGo HTML search with better URL encoding."""
import subprocess, re, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://html.duckduckgo.com/html/?q=Lismore+archaeology+monastery+Saint+Moluag+precious+metal+crucible+cross+slab"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True)
text = r3 = r.stdout.decode("utf-8", errors="replace")

# Find all result links and snippets
links = re.findall(r'class="result__a"[^>]*href="(.*?)"[^>]*>(.*?)</a>', text, re.DOTALL)
snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', text, re.DOTALL)

print(f"Found {len(links)} results, {len(snippets)} snippets")
for i in range(min(len(links), 8)):
    href = links[i][0]
    title = re.sub(r'<[^>]+>', '', links[i][1]).strip()
    snip = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ""
    print(f"\n  Title: {title}")
    print(f"  URL: {href}")
    print(f"  Snippet: {snip[:300]}")
