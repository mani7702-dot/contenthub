#!/usr/bin/env python3
"""Find the research paper and corroborating articles."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Try to find the PRL/Proc Roy Soc A paper
# Also try fetching the Earth.com article directly by searching
urls = [
    ("Google News - Blake Temple", "https://news.google.com/rss/search?q=Blake+Temple+dark+energy+UC+Davis&hl=en-US&gl=US&ceid=US:en"),
    ("Google News - Friedmann unstable", "https://news.google.com/rss/search?q=Friedmann+unstable+dark+energy+Einstein&hl=en-US&gl=US&ceid=US:en"),
    ("Google News - dark energy challenge", "https://news.google.com/rss/search?q=dark+energy+challenge+cosmology+Einstein+equations&hl=en-US&gl=US&ceid=US:en"),
]

for name, url in urls:
    print(f"=== {name} ===")
    p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, url],
                       capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    items = re.findall(r"<item>(.*?)</item>", html, re.DOTALL)
    for item in items:
        title_match = re.search(r"<title>(.*?)</title>", item, re.DOTALL)
        link_match = re.search(r"<link>(.*?)</link>", item, re.DOTALL)
        if title_match:
            title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip()
            print(f"  TITLE: {title[:120]}")
        if link_match:
            link = link_match.group(1).strip()
            print(f"  LINK: {link[:150]}")
        print()
    print()
