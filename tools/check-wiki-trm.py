#!/usr/bin/env python3
"""Fetch Wikipedia page on tissue-resident memory T cells and extract key info."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://en.wikipedia.org/wiki/Tissue-resident_memory_T_cell"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Extract text content
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()

# Find relevant sections
for keyword in ['tissue-resident', 'resident memory T', 'mechanoreceptor', 'stiffness', 'mechanical', 'TRM', 'sentinel']:
    idx = text.lower().find(keyword.lower())
    if idx > 0:
        print(f"--- Around \"{keyword}\" ---")
        print(text[max(0, idx-50):idx+500])
        print()
        break
