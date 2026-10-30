#!/usr/bin/env python3
"""Fetch and extract article text from a URL via curl + regex paragraph extraction.
Tirith-safe replacement for browser_navigate when it times out."""
import subprocess, re, sys

url = sys.argv[1]
ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", ua, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
# Strip script/style
html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
# Extract paragraphs
paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL | re.IGNORECASE)
out = []
for p_text in paras:
    clean = re.sub(r"<[^>]+>", "", p_text)
    clean = clean.strip()
    if len(clean) > 30:
        out.append(clean)
print("\n".join(out))
