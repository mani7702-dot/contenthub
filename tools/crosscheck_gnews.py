import urllib.request, re, html
from urllib.parse import quote

# Try Google News RSS
print("=== Google News RSS ===")
queries = [
    'Pat Palinkas documentary Panther Pat',
    'Panther Pat Slamdance documentary',
]
for q in queries:
    url = f'https://news.google.com/rss/search?q={quote(q)}'
    print(f"\n--- Query: {q} ---")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub)'})
        resp = urllib.request.urlopen(req, timeout=15)
        ghtml = resp.read().decode('utf-8', errors='ignore')
        items = re.findall(r'<item>(.*?)</item>', ghtml, re.DOTALL)
        for item in items[:3]:
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
