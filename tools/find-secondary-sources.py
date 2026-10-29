#!/usr/bin/env python3
"""Fetch a search-engine result page and extract article URLs/snippets."""
import subprocess, re, html as html_module, urllib.parse

queries = [
    ("Google News", "https://news.google.com/rss/search?q=excess+oxygen+magma+deep+earth+atmosphere"),
    ("phys.org search", "https://phys.org/search/?q=excess+oxygen+magma"),
]

for label, url in queries:
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, "--compressed", url], capture_output=True)
    raw = p.stdout.decode("utf-8", errors="replace")
    print(f"\n=== {label} ({url}) ===")
    print(f"Length: {len(raw)}")
    # Find all href links
    links = re.findall(r'href=["\']([^"\']+)["\']', raw)
    for l in links:
        low = l.lower()
        if any(k in low for k in ["phys.org", "scitechdaily", "newsbytesapp", "msn.com", "science", "oxygen"]) and "bing.com" not in low and "google.com" not in low:
            print(f"  LINK: {l[:200]}")
