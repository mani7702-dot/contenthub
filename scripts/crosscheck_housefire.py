import urllib.request
import re

# Cross-check with Local News 3 or other Georgia news sources
urls_to_try = [
    'https://www.wbng.com/article/news/local/georgia-house-fire-foster-family-rescued-casey',
    'https://local3news.com/news/local/family-fostered-500-children-saved-from-house-fire-in-georgia-chattooga-county',
]

for url in urls_to_try:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8')
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        for i, p in enumerate(paragraphs[:10]):
            text = re.sub(r'<[^>]+>', '', p).strip()
            if len(text) > 50:
                print(f"[{url[:50]}] P{i}: {text[:200]}")
                print("---")
    except Exception as e:
        print(f"[{url}] Error: {e}")
