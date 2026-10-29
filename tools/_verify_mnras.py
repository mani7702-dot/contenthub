#!/usr/bin/env python3
"""Fetch Oxford Academic MNRAS page for the Lumina paper to verify."""
import subprocess, re

doi = "10.1093/mnras/stag1469"
url = f"https://academic.oup.com/mnras/article-lookup?doi={doi}"
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
print(f"HTML size: {len(html)} bytes")

# Check title
title = re.findall(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
print(f"Page title: {title}")

# Check if this resolves to the paper
if "stag1469" in html or "Lumina" in html:
    print("CONFIRMED: DOI resolves and Lumina mentioned")
elif "not found" in html.lower() or "404" in html:
    print("ERROR: page not found")
else:
    # Print first few paragraphs
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE)
    for para in paras[:5]:
        clean = re.sub(r'<[^>]+>', '', para).strip()
        clean = re.sub(r'\s+', ' ', clean)
        if len(clean) > 20:
            print(f"PARA: {clean[:200]}")
            print()
