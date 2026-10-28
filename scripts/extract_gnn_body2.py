import urllib.request
import re

url = 'https://www.goodnewsnetwork.org/family-thats-fostered-500-children-saved-from-housefire-thanks-to-strangers-wrong-turn/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')

# Find all paragraph text
paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
for i, p in enumerate(paragraphs):
    text = re.sub(r'<[^>]+>', '', p).strip()
    if len(text) > 30:
        print(f"P{i}: {text}")
        print("---")
