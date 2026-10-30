#!/usr/bin/env python3
"""Extract article about gut microbiome from UH October 2026 news page."""
import subprocess, re

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Fetch the October 2026 news page and find links related to gut/microbiome/aging
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "https://www.hawaii.edu/news/2026/10/"], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Find all article links
links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)
for href, text in links:
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    if len(clean_text) > 10 and ('gut' in href.lower() or 'gut' in clean_text.lower() or 'microbiome' in clean_text.lower() or 'aging' in clean_text.lower() or 'biome' in clean_text.lower() or 'bacteria' in clean_text.lower()):
        print(f"Link: {href}")
        print(f"Text: {clean_text[:150]}")
        print()

# Also, try fetching the specific Google News article which might redirect to the UH press release
# The Google News RSS gave a Google News article URL - let's try fetching it
gn_url = "https://news.google.com/rss/articles/CBMijwFBVV95cUxPYzFuQlNIcmRwSHNBa3YwYUZZQ1pGeW00c001WUZpZGFuNkNxYlVVdzR0S282aW1lYzRXcG5vcTZLZGoyX1prN1FHdjZhRVJpMnNVeGhJZ01DSnFXVFpJamZPVktBd2tvRzR3ZzViamZPZWd0VnBVM1V0MDFWdEFCSUQ3aEd2Njl3d3hJb25MNA?oc=5"
p2 = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "-H", "Accept: text/html", gn_url], capture_output=True)
html2 = p2.stdout.decode("utf-8", errors="replace")
print(f"\nGoogle News article chars: {len(html2)}")
# Look for the UH link or Nature link in the Google News page
uh_links = re.findall(r'https?://[^\s"\'<>]*hawaii\.edu[^\s"\'<>]*', html2)
nature_links = re.findall(r'https?://[^\s"\'<>]*nature\.com[^\s"\'<>]*', html2)
print(f"UH links in GN page: {len(uh_links)}")
for l in uh_links[:5]:
    print(f"  {l[:150]}")
print(f"Nature links in GN page: {len(nature_links)}")
for l in nature_links[:5]:
    print(f"  {l[:150]}")
