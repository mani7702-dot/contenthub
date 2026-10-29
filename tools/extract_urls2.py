import re

with open('/tmp/gsearch.html', 'r') as f:
    html = f.read()

# Find all href URLs
urls = re.findall(r'href="(https?://[^"]+)"', html)
seen = set()
for u in urls:
    if u not in seen and any(kw in u.lower() for kw in ['sweet', 'neuro', 'cognitive', 'brain', 'medical', 'health', 'science', 'diet', 'news', 'org', 'edu']):
        seen.add(u)
        print(u[:150])
print(f"\nTotal external URLs: {len(set(urls))}")
