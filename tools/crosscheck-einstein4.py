#!/usr/bin/env python3
"""Find and fetch the specific corroborating articles."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Earth.com search
search_urls = [
    ("Earth.com search", "https://www.earth.com/?s=dark+energy+einstein"),
    ("Sci.News search", "https://scinews.com/?s=dark+energy+einstein"),
    ("Universe Today search", "https://www.universetoday.com/?s=dark+energy+einstein"),
]

for name, url in search_urls:
    print(f"=== {name} ===")
    p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, url],
                       capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    # Find article links and titles
    links = re.findall(r'href="(https?://[^"]*)"[^>]*>([^<]*(?:dark|energy|einstein|Friedmann|Blake|Temple)[^<]*)', html, re.IGNORECASE)
    if links:
        for link, title in links[:10]:
            print(f"  LINK: {link}")
            print(f"  TITLE: {title.strip()[:100]}")
            print()
    else:
        print("  No matching links found")
    print()
