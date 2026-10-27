#!/usr/bin/env python3
"""Fetch Rainforest Trust page for the 70 million acres milestone."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try to find the Rainforest Trust article about 70 million acres
urls = [
    "https://www.rainforesttrust.org/70-million-acres/",
    "https://www.rainforesttrust.org/stories/70-million-acres-amazon/",
    "https://www.rainforesttrust.org/press/",
]

for url in urls:
    try:
        p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True)
        html = p.stdout.decode("utf-8", errors="replace")
        if len(html) < 500:
            print(f"=== {url} === (too short: {len(html)} bytes)")
            continue
        html2 = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        html2 = re.sub(r"<style[^>]*>.*?</style>", "", html2, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", html2)
        text = re.sub(r"\s+", " ", text)
        
        idx = text.lower().find("70 million")
        if idx < 0:
            idx = text.lower().find("70-million")
        if idx < 0:
            idx = text.lower().find("rainforest trust")
        
        print(f"=== {url} ===")
        if idx > 0:
            print(text[max(0,idx-200):idx+2000])
        else:
            print(text[:2000])
        print()
    except Exception as e:
        print(f"=== {url} === ERROR: {e}")
