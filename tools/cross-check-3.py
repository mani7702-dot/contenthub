#!/usr/bin/env python3
"""Extract actual search result links from Bing for the knitted traffic cops story."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

url = "https://www.bing.com/search?q=%22Fillongley%22+%22knitted%22+traffic+cops"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
stdout = r.stdout

# Extract all links from Bing results
# Bing uses <a href="URL" in the results
links = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>', stdout)
# Filter out bing/microsoft links
relevant = [l for l in links if "bing" not in l.lower() and "microsoft" not in l.lower() 
            and "msn" not in l.lower() and "w3.org" not in l.lower() and "microsoft.com" not in l.lower()]
print(f"Found {len(relevant)} relevant links")
for l in relevant[:10]:
    print(f"  -> {l[:200]}")

# Also search for the GNN article URL in the results
if any("goodnewsnetwork" in l for l in relevant):
    print("\nGNN article found in search results!")
else:
    print("\nNo GNN article found in search results")

# Try another search with different terms
print("\n=== Alternative search ===")
url2 = "https://www.bing.com/search?q=Fillongley+village+knitted+speed+camera+warwickshire"
r2 = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url2], capture_output=True, text=True)
links2 = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>', r2.stdout)
relevant2 = [l for l in links2 if "bing" not in l.lower() and "microsoft" not in l.lower() 
              and "msn" not in l.lower() and "w3.org" not in l.lower()]
print(f"Found {len(relevant2)} relevant links")
for l in relevant2[:10]:
    print(f"  -> {l[:200]}")
