#!/usr/bin/env python3
"""Extract more of the GNN dentist article and cross-check."""
import subprocess, re, urllib.parse

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Fetch the Good News Network article
url = "https://www.goodnewsnetwork.org/fda-approval-for-drill-free-cavity-care-may-be-imminent-after-great-phase-3-treatment-trial/"
p = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Try to find article body
html2 = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html2 = re.sub(r"<style[^>]*>.*?</style>", "", html2, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r"<[^>]+>", " ", html2)
text = re.sub(r"\s+", " ", text)

# Find the main article content
idx = text.find("FDA approval")
if idx >= 0:
    print("=== GNN ARTICLE ===")
    print(text[idx:idx+5000])
else:
    # Try finding from the h1
    idx = text.find("drill-free cavity")
    print(text[max(0,idx-200):idx+5000])
