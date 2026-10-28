#!/usr/bin/env python3
"""Cross-check: get more Wikipedia details and Antiquity journal info."""
import subprocess, json, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Full Wikipedia page for Lismore via REST API
print("=== Lismore full extract ===")
url = "https://en.wikipedia.org/api/rest_v1/page/summary/Lismore,_Scotland"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-H", "Accept: application/json", url], capture_output=True)
try:
    data = json.loads(r.stdout.decode("utf-8", errors="replace"))
    print(data.get('extract', ''))
except:
    print(r.stdout[:200])

# Try the Antiquity journal page
print("\n=== Antiquity journal - search for Lismore ===")
url2 = "https://www.antiquity.ac.uk/projgall/ellis2401/"
r2 = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url2], capture_output=True)
text = r2.stdout.decode("utf-8", errors="replace")
# Extract paragraphs
import re
paras = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
for p in paras[:15]:
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(clean) > 40:
        print(f"  {clean[:300]}")

# Also try a DuckDuckGo search for "Lismore Antiquity archaeology monastery"
print("\n=== DuckDuckGo search ===")
url3 = "https://html.duckduckgo.com/html/?q=Lismore+Antiquity+archaeology+monastery+St+Saint+Moluag+precious+metal"
r3 = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url3], capture_output=True)
text3 = r3.stdout.decode("utf-8", errors="replace")
results = re.findall(r'class="result__a"[^>]*>(.*?)</a>', text3, re.DOTALL)
snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', text3, re.DOTALL)
for i in range(min(len(results), 5)):
    title = re.sub(r'<[^>]+>', '', results[i]).strip()
    snip = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ""
    print(f"  {title}")
    print(f"  {snip[:200]}")
