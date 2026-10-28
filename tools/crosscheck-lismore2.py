#!/usr/bin/env python3
"""Cross-check: get more detail from the Antiquity project gallery and Wikipedia."""
import subprocess, re, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Wikipedia for Lismore and Iona context
urls = {
    "Lismore Wikipedia": "https://en.wikipedia.org/wiki/Lismore,_Scotland",
    "Iona Wikipedia": "https://en.wikipedia.org/wiki/Iona",
    "Hebrides Wikipedia": "https://en.wikipedia.org/wiki/Inner_Hebrides",
}

for label, url in urls.items():
    print(f"\n=== {label}: {url} ===")
    r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True)
    data = r.stdout
    text = data.decode("utf-8", errors="replace")
    # Extract paragraphs
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
    for p in paragraphs[:8]:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if len(clean) > 80 and "Lismore" in clean.lower():
            print(f"  {clean[:300]}")
