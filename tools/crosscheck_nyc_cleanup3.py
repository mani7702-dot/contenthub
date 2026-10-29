#!/usr/bin/env python3
"""Cross-check NYC cleanup story - try multiple search engines and sources."""
import subprocess, re, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Try DuckDuckGo HTML search
queries = [
    "Joshua Service NYC dumping site cleanup CBS News",
    "NYC Crown Heights trash cleanup under metro bridge viral",
    "Joshua Service Queens NYC 311 dumping cleanup",
]

for q in queries:
    url = f"https://html.duckduckgo.com/html/?q={q.replace(' ', '+')}"
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url],
                       capture_output=True, text=True)
    links = re.findall(r'href="(https?://[^"]+)"', r.stdout)
    real_links = [l for l in links if not any(b in l for b in ['duckduckgo', 'duck.com'])]
    print(f"=== Query: {q} ===")
    print(f"  Page size: {len(r.stdout)} bytes")
    for l in real_links[:10]:
        print(f"  {l}")
    print()

# Also try fetching the GNN article and extract any external links mentioned
print("=== Links in GNN article ===")
url_gnn = "https://www.goodnewsnetwork.org/man-named-service-cleans-up-nyc-dumping-site-on-his-own-initiative/"
r2 = subprocess.run(["curl", "-s", "--max-time", "25", "-A", "Mozilla/5.0", url_gnn],
                     capture_output=True, text=True)
all_links = re.findall(r'href="(https?://[^"]+)"', r2.stdout)
cbs_links = [l for l in all_links if 'cbs' in l.lower() or 'news' in l.lower()]
for l in cbs_links[:10]:
    print(l)
