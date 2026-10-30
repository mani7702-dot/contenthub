import urllib.request, xml.etree.ElementTree as ET, sys

url = 'https://www.sciencedaily.com/rss/top.xml'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
raw = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'ignore')
raw = raw.split('</rss>')[0] + '</rss>'
root = ET.fromstring(raw)
items = root.findall('.//item')
print(f'TOTAL items: {len(items)}')
for i, it in enumerate(items[:25]):
    t = it.findtext('title') or ''
    link = it.findtext('link') or ''
    print(f'{i}: {t}')
    print(f'   {link}')
