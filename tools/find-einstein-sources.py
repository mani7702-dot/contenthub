#!/usr/bin/env python3
"""Search for corroborating sources on the Einstein/dark-energy study by Blake Temple, UC Davis, Proc Roy Soc A."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Try Google News RSS search for Blake Temple dark energy
urls = [
    "https://news.google.com/rss/search?q=Blake+Temple+dark+energy+Einstein&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=Einstein+equations+dark+energy+universe&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=UC+Davis+Friedmann+unstable+dark&hl=en-US&gl=US&ceid=US:en",
]

for url in urls:
    print(f"=== {url} ===")
    p = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url],
                       capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    items = re.findall(r"<item>(.*?)</item>", html, re.DOTALL)
    for item in items[:5]:
        title = re.search(r"<title>(.*?)</title>", item, re.DOTALL)
        link = re.search(r"<link>(.*?)</link>", item, re.DOTALL)
        desc = re.search(r"<description>(.*?)</description>", item, re.DOTALL)
        if title:
            print(f"TITLE: {re.sub(r'<[^>]+>', '', title.group(1)).strip()}")
        if link:
            ln = link.group(1).strip()
            if "google.com/url" in ln:
                m = re.search(r"url\?q=([^&]+)", ln)
                if m:
                    ln = m.group(1)
            print(f"LINK: {ln}")
        if desc:
            print(f"DESC: {re.sub(r'<[^>]+>', '', desc.group(1)).strip()[:200]}")
        print("---")
    print()
