#!/usr/bin/env python3
"""Fetch and extract the full text of a GNN article for cross-checking."""
import subprocess, re
UA = "Mozilla/5.0 (ContentHub picker; contact anduguhamani722@gmail.com)"

url = "https://www.goodnewsnetwork.org/man-proposes-to-his-girlfriend-after-they-were-struck-by-lightning-she-restarted-his-heart-twice/"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="ignore")

# Extract all text content
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'&amp;', '&', text)
text = re.sub(r'&lt;', '<', text)
text = re.sub(r'&gt;', '>', text)
text = re.sub(r'&quot;', '"', text)
text = re.sub(r'&#039;', "'", text)
text = re.sub(r'&nbsp;', ' ', text)
text = re.sub(r'\s+', ' ', text)

# Find the main content
print("=== FULL ARTICLE TEXT ===")
print(text[:5000])
