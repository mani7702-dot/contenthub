#!/usr/bin/env python3
"""Extract the GNN article 'Man Named Service Cleans Up NYC Dumping Site' - parse article body."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.goodnewsnetwork.org/man-named-service-cleans-up-nyc-dumping-site-on-his-own-initiative/"

r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url],
                   capture_output=True, text=True)
print(f"SIZE: {len(r.stdout)} bytes")

html_src = r.stdout

# Extract the <article> section
m = re.search(r'<article[^>]*>(.*?)</article>', html_src, re.S | re.I)
if m:
    article_html = m.group(1)
else:
    # fallback: find the entry-content div
    m = re.search(r'<div[^>]*class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>\s*</', html_src, re.S | re.I)
    if m:
        article_html = m.group(1)
    else:
        article_html = html_src

# strip tags
text = re.sub(r'<script[^>]*>.*?</script>', '', article_html, flags=re.S)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
text = re.sub(r'<[^>]+>', ' ', text)
text = html.unescape(text)
text = re.sub(r'\s+', ' ', text).strip()

print("=== ARTICLE TEXT ===")
print(text[:4000])
