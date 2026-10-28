import urllib.request
import re

url = 'https://www.goodnewsnetwork.org/family-thats-fostered-500-children-saved-from-housefire-thanks-to-strangers-wrong-turn/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')

text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)

idx = text.find('fostered 500')
if idx > 0:
    print(text[max(0, idx-200):idx+5000])
else:
    idx = text.find('housefire')
    if idx > 0:
        print(text[max(0, idx-200):idx+5000])
    else:
        print(text[:3000])
