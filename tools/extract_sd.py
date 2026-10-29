import re

with open('/tmp/sd-eclipse.html', encoding='utf-8') as f:
    html = f.read()

# Extract all paragraphs
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.S)
seen = set()
for t in paras:
    clean = re.sub(r'<[^>]+>', '', t)
    clean = clean.replace('&amp;', '&')
    clean = clean.replace('&#039;', "'")
    clean = clean.replace('&quot;', '"')
    clean = re.sub(r'\s+', ' ', clean).strip()
    if clean and len(clean) > 15 and clean not in seen:
        seen.add(clean)
        print(clean)
    if len(seen) > 50:
        break
print(f"\n=== TOTAL PARAS: {len(seen)} ===")

# Look for source/journal links
links = re.findall(r'href="(https?://[^"]+)"', html)
journals = [l for l in links if any(k in l.lower() for k in ['nature', 'science', 'pnas', 'doi.org', 'elsevier', 'springer', 'nature.com', 'academic'])]
for l in journals[:5]:
    print("JOURNAL:", l)
