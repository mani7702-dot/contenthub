#!/usr/bin/env python3
"""Search for the lightning proposal story across multiple sources."""
import subprocess, re, urllib.parse

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

# Try Action News 5 with different URL patterns
urls = [
    "https://www.actionnews5.com/search?q=lightning+proposal+Broderick+Wisconsin",
    "https://www.actionnews5.com/article/news/local/lightning-strike-proposal-wisconsin-kettle-moraine/539-video/",
    "https://www.actionnews5.com/article/news/local/wisconsin-lightning-strike-hiking-couple-proposal/539-video/",
]

for url in urls:
    data = fetch(url)
    text = strip_html(data)
    # Look for relevant content
    if "lightning" in text.lower() and "proposal" in text.lower():
        print(f"FOUND at: {url}")
        print(text[:3000])
        print("---")
    elif len(text) > 500:
        print(f"GOT {len(text)} chars from {url} (may have content)")
        # Print snippets containing relevant keywords
        for kw in ["lightning", "Broderick", "proposal", "Kettle Moraine"]:
            idx = text.lower().find(kw.lower())
            if idx >= 0:
                print(f"  [{kw}]: ...{text[max(0,idx-50):idx+200]}...")
    else:
        print(f"Empty/small response from {url}")

# Also try Bing search
print("\n=== Bing Search ===")
bing_url = "https://www.bing.com/search?q=" + urllib.parse.quote("lightning strike Wisconsin hiking couple proposal hospital Broderick")
data = fetch(bing_url)
text = strip_html(data)
# Extract result links
links = re.findall(r'href="(https?://[^"]+)"', text)
for l in links:
    if "actionnews5" in l or "goodnewsnetwork" in l or "wisconsin" in l.lower() or "lightning" in l.lower():
        if "bing.com" not in l and "microsoft.com" not in l:
            print(f"  {l}")
