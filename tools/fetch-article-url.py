#!/usr/bin/env python3
"""Fetch GNN feed and find the cheetah article URL."""
import subprocess, re
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "https://www.goodnewsnetwork.org/feed/"], capture_output=True)
html = p.stdout.decode("utf-8", errors="ignore")
# Find cheetah URL
urls = re.findall(r"<link>(.*?)</link>", html, re.DOTALL)
for u in urls:
    if "cheetah" in u.lower():
        print(u.strip())
