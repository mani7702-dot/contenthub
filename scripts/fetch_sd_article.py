import urllib.request, re, sys

url = sys.argv[1]
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')

body = re.findall(r'<p[^>]*>(.*?)</p>', raw, re.DOTALL)
clean = []
for p in body:
    txt = re.sub(r'<[^>]+>', '', p).strip()
    if len(txt) > 30:
        clean.append(txt)

print(f"FOUND {len(clean)} paragraphs")
for i, p in enumerate(clean[:30]):
    print(f"[{i}] {p[:400]}")

desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', raw, re.IGNORECASE)
if desc:
    print(f"\nDESCRIPTION: {desc.group(1)[:600]}")
