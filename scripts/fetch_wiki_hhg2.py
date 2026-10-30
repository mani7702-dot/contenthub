import urllib.request, json, sys

url = "https://en.wikipedia.org/w/api.php?action=query&titles=High%20harmonic%20generation&prop=extracts&exsectionformat=plain&format=json&formatversion=2"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
data = json.loads(raw)
if 'query' in data:
    for page in data['query']['pages']:
        txt = page.get('extract', '')
        print(f"Title: {page.get('title')}")
        print(txt[:2000])
