import urllib.request, re, html
from urllib.parse import quote

# Try Wikipedia API for disambiguation
api_url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=Pat+Palinkas+football&format=json&srlimit=5'
print("=== Wikipedia search: Pat Palinkas football ===")
try:
    req = urllib.request.Request(api_url, headers={'User-Agent': 'ContentHub fact-check bot'})
    resp = urllib.request.urlopen(req, timeout=15)
    data = resp.read().decode('utf-8', errors='ignore')
    import json
    j = json.loads(data)
    for r in j.get('query', {}).get('search', []):
        print(f"  Title: {r['title']}")
        snippet = re.sub(r'<[^>]+>', '', r.get('snippet', ''))
        print(f"  Snippet: {html.unescape(snippet)[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Try Bing News RSS
print("\n=== Bing News RSS ===")
bing_url = 'https://www.bing.com/news/rss/search?q=Pat+Palinkas+first+woman+football+documentary'
try:
    req = urllib.request.Request(bing_url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub)'})
    resp = urllib.request.urlopen(req, timeout=15)
    bing_html = resp.read().decode('utf-8', errors='ignore')
    items = re.findall(r'<item>(.*?)</item>', bing_html, re.DOTALL)
    for item in items[:5]:
        title = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
        link = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
        desc = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
        if title:
            print(f"  Title: {html.unescape(title.group(1).strip())[:200]}")
        if link:
            print(f"  URL: {link.group(1).strip()}")
        if desc:
            desc_clean = re.sub(r'<[^>]+>', '', desc.group(1))
            print(f"  Desc: {html.unescape(desc_clean.strip())[:200]}")
        print("---")
except Exception as e:
    print(f"Error: {e}")

# Also try searching for the documentary
print("\n=== Bing News RSS: Panther Pat documentary ===")
bing_url2 = 'https://www.bing.com/news/rss/search?q=Panther+Pat+documentary+Slamdance'
try:
    req = urllib.request.Request(bing_url2, headers={'User-Agent': 'Mozilla/5.0 (ContentHub)'})
    resp = urllib.request.urlopen(req, timeout=15)
    bing_html = resp.read().decode('utf-8', errors='ignore')
    items = re.findall(r'<item>(.*?)</item>', bing_html, re.DOTALL)
    for item in items[:5]:
        title = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
        link = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
        desc = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
        if title:
            print(f"  Title: {html.unescape(title.group(1).strip())[:200]}")
        if link:
            print(f"  URL: {link.group(1).strip()}")
        if desc:
            desc_clean = re.sub(r'<[^>]+>', '', desc.group(1))
            print(f"  Desc: {html.unescape(desc_clean.strip())[:200]}")
        print("---")
except Exception as e:
    print(f"Error: {e}")
