#!/usr/bin/env python3
"""Cross-check the FDA drill-free cavity care story."""
import subprocess, urllib.parse

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Fetch the Good News Network article
url = "https://www.goodnewsnetwork.org/fda-approval-for-drill-free-cavity-care-may-be-imminent-after-great-phase-3-treatment-trial/"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
# Extract text content from paragraphs
import re
# Remove scripts and styles
html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
# Remove HTML tags
text = re.sub(r"<[^>]+>", " ", html)
text = re.sub(r"\s+", " ", text)
# Find the main content
idx = text.lower().find("drill-free")
if idx > 0:
    print(text[max(0,idx-200):idx+3000])
else:
    print(text[:3000])
