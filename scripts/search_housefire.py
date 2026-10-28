import urllib.request
import re

# Try to find the Local News 3 story
url = 'https://www.google.com/search?q=%22fostered+500+children%22+%22house+fire%22+%22Georgia%22+%22Burke%22+rescue'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')

# Find article links
links = re.findall(r'href="(https?://[^"]+)"', html)
for link in links:
    if 'goodnewsnetwork' not in link and 'google' not in link and 'youtube' not in link and 'facebook' not in link and len(link) < 200:
        print(link)
