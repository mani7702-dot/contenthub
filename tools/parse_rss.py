import urllib.request, re

req = urllib.request.Request(
    'https://www.sciencedaily.com/rss/top.xml',
    headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'}
)
data = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
# ScienceDaily RSS has trailing comment after </rss> — strip it
data = data.split('</rss>')[0] + '</rss>'
items = re.findall(r'<item>(.*?)</item>', data, re.S)
print('items:', len(items))
for it in items[:60]:
    t = re.search(r'<title>(.*?)</title>', it, re.S)
    if t:
        print('-', t.group(1).strip()[:150])
