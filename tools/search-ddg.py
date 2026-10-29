#!/usr/bin/env python3
"""Search for lightning proposal story on multiple platforms."""
import subprocess, re, urllib.parse

UA = "Mozilla/5.0 (ContentHub reader; contact andugulamani722@gmail.com)"

def fetch(url):
    p = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True)
    return p.stdout.decode("utf-8", errors="replace")

def strip_html(text):
    html = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'&[a-z#0-9]+;', ' ', html)
    html = re.sub(r'\s+', ' ', html).strip()
    return html

# Try DuckDuckGo for search
ddg_url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote("lightning strike proposal Wisconsin hiking Broderick Kettle Moraine")
html = fetch(ddg_url)
# Extract search results
results = re.findall(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
snippets = re.findall(r'class="result__snippet">(.*?)</a>', html, re.DOTALL)

print("=== DuckDuckGo Results ===")
for i, (url, title) in enumerate(results[:10]):
    title_text = re.sub(r'<[^>]+>', '', title).strip()
    snip = snippets[i] if i < len(snippets) else ""
    snip_text = re.sub(r'<[^>]+>', '', snip).strip()[:200]
    print(f"  [{i+1}] {title_text}")
    print(f"      URL: {url}")
    print(f"      Snippet: {snip_text}")
    print()

# Also try the Listverse nuclear testing URL to confirm
print("\n=== Listverse nuclear testing article ===")
lv_url = "https://listverse.com/2026/10/27/10-unexpected-things-still-carrying-the-fingerprints-of-nuclear/"
html2 = fetch(lv_url)
text2 = strip_html(html2)
# Find the main article content
idx = text2.find("Nuclear weapons tests")
if idx >= 0:
    print(text2[idx:idx+2000])
