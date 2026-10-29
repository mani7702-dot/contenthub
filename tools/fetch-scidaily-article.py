#!/usr/bin/env python3
"""Fetch the ScienceDaily article page for the Einstein/dark-energy story and extract key facts."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
url = "https://www.sciencedaily.com/releases/2026/10/261028232719.htm"

p = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url],
                     capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Extract paragraphs
paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
for para in paras:
    # strip tags
    text = re.sub(r"<[^>]+>", "", para).strip()
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&nbsp;", " ", text)
    if len(text) > 50:
        print(text)
        print()

print("=== END PARAGRAPHS ===")
# Also try to find the actual journal / DOI
doi = re.findall(r"(10\.\d+/[^\s\"'<>&]+)", html)
if doi:
    print(f"DOIs found: {doi[:5]}")
