#!/usr/bin/env python3
"""Cross-check: search for the Antiquity paper about Lismore excavations."""
import subprocess, re, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Bing search for the specific paper
url = "https://www.bing.com/search?q=Antiquity+journal+Lismore+monastery+excavation+Argyll+Archaeology+Clare+Ellis+2024"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True)
text = r.stdout.decode("utf-8", errors="replace")

results = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
for p in results[:15]:
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(clean) > 60 and ("antiquity" in clean.lower() or "lismore" in clean.lower() or "ellis" in clean.lower()):
        print(f"  {clean[:300]}")
        print("---")

# Also try Cambridge Journals search
print("\n=== Cambridge search ===")
url2 = "https://www.bing.com/search?q=cambridge+core+antiquity+lismore+scotland+monastery+precious+metal"
r2 = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url2], capture_output=True)
text2 = r2.stdout.decode("utf-8", errors="replace")
results2 = re.findall(r'<p[^>]*>(.*?)</p>', text2, re.DOTALL)
for p in results2[:15]:
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(clean) > 60 and ("antiquity" in clean.lower() or "lismore" in clean.lower() or "precious" in clean.lower()):
        print(f"  {clean[:300]}")
        print("---")
