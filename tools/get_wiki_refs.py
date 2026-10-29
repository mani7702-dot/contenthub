import re, urllib.request

url = 'https://en.wikipedia.org/wiki/Gangaichthys'
req = urllib.request.Request(url, headers={'User-Agent': 'ContentHub (research; contact andugulamani722@gmail.com)'})
html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='ignore')
links = re.findall(r'href="(https?://[^"]+)"', html)
for l in links:
    print(l)
