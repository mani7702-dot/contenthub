import urllib.request
import re

# Try Bing news search for the story
url = 'https://www.bing.com/news/search?q=fostered+500+children+house+fire+Georgia+Burke+rescue'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')

# Find article links from search results
links = re.findall(r'href="(https?://[^"]+)"', html)
seen = set()
for link in links:
    if any(x in link for x in ['bing.com', 'microsoft.com', 'go.microsoft', 'msn.com']):
        continue
    if link.startswith('https://') and len(link) < 200 and link not in seen:
        seen.add(link)
        print(link)
