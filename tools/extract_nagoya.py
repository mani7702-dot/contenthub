import re

with open('/tmp/nagoya-eclipse.html', encoding='utf-8') as f:
    html = f.read()

paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.S)
seen = set()
for t in paras:
    clean = re.sub(r'<[^>]+>', '', t)
    clean = clean.replace('&amp;', '&')
    clean = clean.replace('&#039;', "'")
    clean = clean.replace('&quot;', '"')
    clean = re.sub(r'&[a-z]+;', ' ', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    if clean and len(clean) > 20 and clean not in seen:
        seen.add(clean)
        print(clean)
    if len(seen) > 45:
        break
print(f"=== TOTAL: {len(seen)} ===")
