import urllib.request, re

# Fetch ScienceDaily top RSS and locate the "dinosaur teeth" bird article
req = urllib.request.Request(
    'https://www.sciencedaily.com/rss/top.xml',
    headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'}
)
data = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
data = data.split('</rss>')[0] + '</rss>'
items = re.findall(r'<item>(.*?)</item>', data, re.S)
for it in items:
    t = re.search(r'<title>(.*?)</title>', it, re.S)
    if t and 'dinosaur teeth' in t.group(1).lower():
        link = re.search(r'<link>(.*?)</link>', it, re.S)
        desc = re.search(r'<description>(.*?)</description>', it, re.S)
        print("TITLE:", t.group(1).strip())
        print("LINK:", link.group(1).strip() if link else "N/A")
        d = desc.group(1).strip() if desc else ""
        d = re.sub(r'<[^>]+>', '', d)
        print("DESC:", d[:600])
        print("---")
