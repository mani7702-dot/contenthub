#!/usr/bin/env python3
"""Fetch the cranberry tooth decay ScienceDaily article and extract full content."""
import subprocess, re

url = "https://www.sciencedaily.com/releases/2026/10/261028232701.htm"
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
html = result.stdout

print(f"HTML length: {len(html)}")

# Extract title
title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
if title_match:
    print("Title:", title_match.group(1).strip())

# Extract description paragraph (lead-in)
# ScienceDaily articles have the main content in <p> tags
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
# Extract just paragraph text
paras = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
for i, p in enumerate(paras[:20]):
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(clean) > 20:
        print(f"\n--- Para {i+1} ---")
        print(clean[:600])

# Extract meta description
desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
if desc_match:
    print("\n\nMeta Description:")
    print(desc_match.group(1).strip()[:500])

# Look for institution/source info
inst_match = re.search(r'<meta[^>]*name=["\']author["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
if inst_match:
    print("\nAuthor:", inst_match.group(1).strip())

# Look for journal reference
journal_text = re.findall(r'(?:published in|journal|Nature|Science|DOI)[^<]{0,200}', html, re.IGNORECASE)
for j in journal_text[:5]:
    print(f"\nJournal ref: {j}")
