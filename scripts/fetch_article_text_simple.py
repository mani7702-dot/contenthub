import urllib.request, re, sys

url = sys.argv[1]
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')

# Try to find the ScienceDaily article body
# ScienceDaily uses <p> tags in a div with id="text" or similar
body = re.findall(r'<p[^>]*>(.*?)</p>', raw, re.DOTALL)
if not body:
    body = re.findall(r'<div[^>]*id="abstract"[^>]*>(.*?)</div>', raw, re.DOTALL)
    print("ABSTRACT:", body[:1] if body else "none")

print(f"FOUND {len(body)} paragraph matches")
clean = []
for p in body:
    txt = re.sub(r'<[^>]+>', '', p).strip()
    if len(txt) > 30:
        clean.append(txt)

if clean:
    print("\n=== FIRST 30 PARAGRAPHS ===")
    for i, p in enumerate(clean[:30]):
        print(f"[{i}] {p[:300]}")

# Also look for meta description
desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', raw, re.IGNORECASE)
if desc:
    print(f"\nDESCRIPTION: {desc.group(1)[:400]}")
