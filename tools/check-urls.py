#!/usr/bin/env python3
"""Check HTTP status for the GNN article URL."""
import subprocess

urls = [
    "https://www.goodnewsnetwork.org/village-installs-knitted-traffic-cops-to-slow-speeding-drivers/",
    "https://www.goodnewsnetwork.org/village-installs-knitted-traffic-cops-to-slow-down-speeding-drivers/",
]

for url in urls:
    r = subprocess.run(["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}|%{url_effective}|%{size_download}",
                        "--max-time", "20", "-A",
                        "Mozilla/5.0 (ContentHub picker)", url], capture_output=True, text=True)
    print(f"URL: {url}")
    print(f"  Result: {r.stdout}")
    print()
