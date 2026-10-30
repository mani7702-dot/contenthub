#!/usr/bin/env python3
"""Fetch article text plus title from a URL via curl + regex."""
import subprocess, re, sys

url = sys.argv[1]
ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", ua, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Extract title
title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
title = title_match.group(1).strip() if title_match else "NO TITLE"
print(f"TITLE: {title}")
print("=" * 60)

# Strip script/style
html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL | re.IGNORECASE)
for p_text in paras:
    clean = re.sub(r"<[^>]+>", "", p_text).strip()
    if len(clean) > 30:
        print(clean)
