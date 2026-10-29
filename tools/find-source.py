#!/usr/bin/env python3
"""Search for news sources and extract article text."""
import subprocess, re, sys, urllib.parse

UA = "Mozilla/5.0 (ContentHub reader; contact andugulamani722@gmail.com)"

def fetch(url):
    p = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True)
    return p.stdout

def strip_html(data):
    html = data.decode("utf-8", errors="replace")
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'&[a-z#0-9]+;', ' ', html)
    html = re.sub(r'\s+', ' ', html).strip()
    return html

# Try Action News 5 search
url = "https://www.actionnews5.com/search?q=" + urllib.parse.quote("lightning proposal Wisconsin hiking Broderick")
data = fetch(url)
text = strip_html(data)
# Look for relevant links
links = re.findall(r'href="(/[^\"]+)"', text[:10000])
for l in links[:20]:
    if "lightning" in l.lower() or "broderick" in l.lower() or "proposal" in l.lower():
        print(f"Link: https://www.actionnews5.com{l}")

# Also try a direct fetch
print("\n--- Searching for Action News 5 coverage ---")
url2 = "https://www.actionnews5.com/article/news/local/lightning-strike-survivor-proposes-hospital-wisconsin-kettle-moraine/539-101414813.html"
data2 = fetch(url2)
text2 = strip_html(data2)
print(text2[:3000])
