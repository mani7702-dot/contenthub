#!/usr/bin/env python3
"""Cross-check the GNN NYC cleanup story with a secondary source."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Search for secondary coverage
queries = [
    "Joshua Service NYC dumping site cleanup CBS News",
    "NYC Crown Heights metro bridge trash cleanup viral",
]

for q in queries:
    url = f"https://www.google.com/search?q={q.replace(' ', '+')}"
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url],
                       capture_output=True, text=True)
    text = re.sub(r'<[^>]+>', ' ', r.stdout)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    # Find result URLs
    urls = re.findall(r'https?://[^\s"\'<>]+', r.stdout)
    news_urls = [u for u in urls if any(s in u for s in ['.com', '.org', '.co', '.news'])
                 and not any(b in u for b in ['google', 'gstatic', 'youtube', 'facebook', 'reddit'])]
    print(f"=== Search: {q} ===")
    print(f"Page size: {len(r.stdout)} bytes")
    print(f"News URLs found: {news_urls[:10]}")
    print()

# Try fetching the CBS News article directly (mentioned in GNN story)
cbs_url = "https://www.cbsnews.com/news/joshua-service-nyc-dumping-site-cleanup/"
print(f"=== Fetching CBS News URL: {cbs_url} ===")
r2 = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, cbs_url],
                     capture_output=True, text=True)
print(f"CBS News page size: {len(r2.stdout)} bytes")
if len(r2.stdout) > 100:
    text2 = re.sub(r'<script[^>]*>.*?</script>', '', r2.stdout, flags=re.S)
    text2 = re.sub(r'<style[^>]*>.*?</style>', '', text2, flags=re.S)
    text2 = re.sub(r'<[^>]+>', ' ', text2)
    text2 = html.unescape(text2)
    text2 = re.sub(r'\s+', ' ', text2).strip()
    # Find relevant sections
    idx = text2.find("Service")
    if idx > 0:
        print(text2[max(0,idx-100):idx+2000])
    else:
        print("Could not find 'Service' in CBS page")
        print(text2[:500])
else:
    print("CBS page too small or empty")
