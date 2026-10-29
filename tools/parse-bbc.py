#!/usr/bin/env python3
"""Parse BBC article and extract body text."""
import urllib.request, re, sys, json

url = "https://www.bbc.co.uk/news/articles/cm2ke80nd929o?at_medium=RSS&at_campaign=rss"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"})
try:
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode("utf-8", errors="replace")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

# Find JSON-LD structured data
json_lds = re.findall(r'\{("@context":"http://schema\.org").*?("@type":"ReportageNewsArticle").*?\}', html, re.DOTALL)
for j in json_lds:
    jstr = "".join(j)
    full = "{" + jstr + "}"
    try:
        data = json.loads(full)
        print(f"Headline: {data.get('headline','')}")
        print(f"Published: {data.get('datePublished','')}")
        print(f"Description: {data.get('description','')}")
        print(f"Author: {data.get('author',[{}])[0].get('name','') if data.get('author') else ''}")
        print(f"Image: {data.get('image',{}).get('url','')}")
    except:
        pass

# Extract text content between tags
texts = re.findall(r'>([^<]{20,500})<', html)
seen = set()
for t in texts:
    t = t.strip()
    if t in seen:
        continue
    seen.add(t)
    if len(t) > 30 and not t.startswith(('http', 'var ', '{', 'function', 'window', 'document', 'if (', 'for (')):
        # Skip non-content
        if re.match(r'^[a-zA-Z\s\d\.\,\-\'\"]{20,}$', t):
            print(f"\nTEXT: {t[:400]}")