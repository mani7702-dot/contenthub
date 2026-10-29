import re

with open('/tmp/pubmed_sugar.html', 'r') as f:
    html = f.read()

# Find meta description which often contains the abstract summary
meta_desc = re.search(r'<meta name="description" content="([^"]*)"', html)
if meta_desc:
    print("META DESC:", meta_desc.group(1)[:500])

# Find abstract div
abstract_match = re.search(r'<div class="abstract.*?</div>', html, re.DOTALL)
if abstract_match:
    text = re.sub(r'<[^>]+>', ' ', abstract_match.group(0))
    text = re.sub(r'\s+', ' ', text).strip()
    print("\nABSTRACT:", text[:1000])

# Look for citation info
for kw in ['Neurology', 'DOI', '10.1212', 'sweetener', 'cognitive decline', 'brain aging']:
    idx = html.lower().find(kw.lower())
    if idx >= 0:
        context = re.sub(r'\s+', ' ', html[max(0,idx-100):idx+300])
        context = re.sub(r'<[^>]+>', ' ', context)
        print(f"\n--- '{kw}' ---")
        print(context[:300])
