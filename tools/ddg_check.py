import urllib.request, re, html, json
from urllib.parse import quote

# Search DuckDuckGo for Pat Palinkas / Panther Pat documentary
queries = [
    'Pat Palinkas first woman professional football Orlando Panthers',
    'Panther Pat documentary Slamdance 2026',
]

for q in queries:
    url = f'https://html.duckduckgo.com/html/?q={quote(q)}'
    print(f"\n=== Search: {q} ===")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub fact-check bot)'})
        resp = urllib.request.urlopen(req, timeout=15)
        htmltext = resp.read().decode('utf-8', errors='ignore')
        # Extract result titles and snippets
        results = re.findall(r'result__a[^>]*href="(.*?)"[^>]*>(.*?)</a>', htmltext, re.DOTALL)
        for href, title in results[:8]:
            title_clean = re.sub(r'<[^>]+>', '', title)
            title_clean = html.unescape(title_clean).strip()
            print(f"  Title: {title_clean}")
            print(f"  URL: {href}")
    except Exception as e:
        print(f"Error: {e}")
