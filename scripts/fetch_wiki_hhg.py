import urllib.request, re, json, sys

url = "https://en.wikipedia.org/w/api.php?action=query&titles=High-harmonic_generation&prop=extracts&exsectionformat=plain&format=json&formatversion=2"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
data = json.loads(raw)
if 'query' in data:
    for page in data['query']['pages']:
        txt = page.get('extract', '')
        if not txt:
            print("EMPTY EXTRACT - page title:", page.get('title', '?'))
            # Try searching instead
            search_url = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=high-harmonic+generation&format=json"
            sreq = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
            sraw = urllib.request.urlopen(sreq, timeout=25).read().decode('utf-8','ignore')
            sdata = json.loads(sraw)
            titles = [r['title'] for r in sdata.get('query',{}).get('search',[])[:3]]
            print(f"Search results: {titles}")
        else:
            print(txt[:1500])
else:
    print(f"ERROR: {raw[:500]}")
