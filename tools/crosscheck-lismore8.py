#!/usr/bin/env python3
"""Cross-check: get the Antiquity journal project gallery page."""
import subprocess, re, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try several possible project gallery URLs
urls = [
    "https://www.antiquity.ac.uk/projgall/nebulous2401/",
    "https://www.antiquity.ac.uk/projgall/ellis2401/",
    "https://www.antiquity.ac.uk/projgall/grant2401/",
]

for url in urls:
    r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True)
    text = r.stdout.decode("utf-8", errors="replace")
    title_match = re.search(r"<title>(.*?)</title>", text, re.DOTALL)
    if title_match:
        t = title_match.group(1).strip()
        if "Page not found" not in t and "404" not in t and len(t) > 5:
            print(f"URL: {url}")
            print(f"Title: {t}")
            results = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
            for p in results[:10]:
                clean = re.sub(r'<[^>]+>', '', p).strip()
                if len(clean) > 60:
                    print(f"  {clean[:300]}")
            print("---")
