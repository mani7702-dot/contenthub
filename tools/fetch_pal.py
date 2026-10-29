import urllib.request, re, html

url = 'https://en.wikipedia.org/wiki/Patricia_Palinkas'
print(f"=== Fetching: {url} ===")
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'ContentHub fact-check bot'})
    resp = urllib.request.urlopen(req, timeout=15)
    htmltext = resp.read().decode('utf-8', errors='ignore')
    paras = re.findall(r'<p[^>]*>(.*?)</p>', htmltext, re.DOTALL)
    count = 0
    for p in paras:
        clean = re.sub(r'<[^>]+>', '', p)
        clean = html.unescape(clean).strip()
        if len(clean) > 30:
            print(clean[:400])
            print('---')
            count += 1
        if count >= 10:
            break
    if count == 0:
        print("No substantial paragraphs found")
except Exception as e:
    print(f"Error: {e}")
