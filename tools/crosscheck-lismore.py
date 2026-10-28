#!/usr/bin/env python3
"""Cross-check: search for academic sources on the Lismore discovery."""
import subprocess, re, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Search for the academic paper
urls = [
    "https://www.cambridge.org/core/journals/antiquity/article/abs/lismore/0003598X",
    "https://www.antiquity.ac.uk/projgall/ellis2401/",
    "https://www.sciencedirect.com/science/article/pii/S0003598X2400001X",
]

for url in urls:
    print(f"\n=== Trying: {url} ===")
    try:
        r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True)
        data = r.stdout
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
        text = data.decode("utf-8", errors="replace")
        # Extract title
        title_match = re.search(r"<title>(.*?)</title>", text, re.DOTALL)
        if title_match:
            t = title_match.group(1).strip()
            print(f"Page title: {t}")
        # Look for key terms
        for term in ["Lismore", "Saint Mo Luóc", "650", "1040 CE", "precious metal", "cross slab", "Antiquity"]:
            if term.lower() in text.lower():
                print(f"  Found: '{term}'")
    except Exception as e:
        print(f"  Error: {e}")
