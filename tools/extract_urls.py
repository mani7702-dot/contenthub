import re, urllib.parse

with open('/tmp/gsearch.html', 'r') as f:
    html = f.read()

links = re.findall(r'uddg=([^"&]+)', html)
for l in links[:20]:
    decoded = urllib.parse.unquote(l)
    print(decoded)
