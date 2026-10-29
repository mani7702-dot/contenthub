import urllib.request, re, html

urls = [
    'https://en.wikipedia.org/wiki/Orlando_Panthers_(WFL)',
    'https://en.wikipedia.org/wiki/Pat_Palinkas',
]

for url in urls:
    print(f"\n=== {url} ===")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ContentHub fact-check bot'})
        resp = urllib.request.urlopen(req, timeout=15)
        htmltext = resp.read().decode('utf-8', errors='ignore')
        paras = re.findall(r'<p[^>]*>(.*?)</p>', htmltext, re.DOTALL)
        found = False
        for p in paras[:20]:
            clean = re.sub(r'<[^>]+>', '', p)
            clean = html.unescape(clean).strip()
            if len(clean) > 30:
                print(clean[:300])
                print('---')
                found = True
        if not found:
            print("No substantial paragraphs found")
    except Exception as e:
        print(f"Error: {e}")
