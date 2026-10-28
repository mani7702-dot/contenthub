#!/usr/bin/env python3
"""Check dedup status for candidate stories."""
import subprocess

terms = [
    "128000",
    "128,000",
    "atm",
    "every dollar",
    "texas man",
    "hobbits",
    "precious",
    "wedding ring",
    "italian",
    "microplastic",
    "wastewater",
    "princeton",
    "nature-inspired",
]

# Search in content files
for term in terms:
    result = subprocess.run(
        ["grep", "-ril", term, "content/news/", "content/blog/", "content/trending/"],
        capture_output=True, text=True, cwd="/home/ubuntu/contenthub"
    )
    matches = result.stdout.strip()
    if matches:
        print(f"FOUND '{term}': {matches}")
    else:
        print(f"CLEAN '{term}': no matches")
