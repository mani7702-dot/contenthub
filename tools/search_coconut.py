#!/usr/bin/env python3
"""Cross-check coconut oil jet fuel research via Bing News."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

search_url = "https://www.bing.com/news/search?q=coconut+oil+aviation+fuel+jet+engine+Osaka+Metropolitan+University"
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, search_url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

print(f"HTML length: {len(html)}")

# Extract result links
links = re.findall(r'href="(https?://[^"]+)"', html)
for link in links[:30]:
    if "bing.com" in link or "microsoft.com" in link:
        continue
    print(f"LINK: {link}")

# Extract text snippets
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)
for match in re.finditer(r'((?:coconut|Osaka)[^.]{0,200})', text, re.IGNORECASE):
    snippet = match.group(1).strip()
    if len(snippet) > 30:
        print(f"SNIPPET: {snippet[:200]}")
        print("---")
