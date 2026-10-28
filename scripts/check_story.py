import urllib.request
import re

url = 'https://www.bbc.co.uk/news/articles/cmwyv8ld22z1o'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')

text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)

idx = text.find('King acknowledges')
if idx > 0:
    print(text[max(0, idx-200):idx+2000])
else:
    idx = text.find('Caribbean')
    if idx > 0:
        print(text[max(0, idx-200):idx+2000])
    else:
        print(text[:2000])
