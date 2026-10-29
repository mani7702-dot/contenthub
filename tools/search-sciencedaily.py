#!/usr/bin/env python3
"""Search ScienceDaily for cranberry tooth decay article."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Search ScienceDaily
url = "https://www.sciencedaily.com/search/?keyword=cranberry+tooth+decay"
result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
html = result.stdout

# Find article links
links = re.findall(r'href="(/releases/\d{4}/\d{2}/\d+[^"]+)"', html)
print("Release links found:")
for l in set(links):
    print(f"  https://www.sciencedaily.com{l}")

# Also search for cranberry
links2 = re.findall(r'href="([^"]*cranberry[^"]*)"', html, re.IGNORECASE)
print("\nCranberry links found:")
for l in set(links2):
    print(f"  {l}")

# Extract title
title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
if title_match:
    print("\nPage title:", title_match.group(1).strip())
