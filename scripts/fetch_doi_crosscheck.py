import urllib.request, re, sys

url = sys.argv[1]
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')

# Find DOI links
dois = re.findall(r'(10\.\d+/[^\s"<>]+)', raw)
print(f"DOIs found: {dois[:10]}")

# Find Nature/Springer links
nature_links = re.findall(r'https://[^\s"<>]*nature\.com[^\s"<>]*', raw)
print(f"Nature links: {nature_links[:10]}")

# Find journal citation
journals = re.findall(r'(Nature Photonics|Nature|nature)', raw, re.IGNORECASE)
print(f"Journal mentions: {journals[:5]}")

# Meta keywords / tags
tags = re.findall(r'<meta[^>]+name="keywords"[^>]+content="([^"]+)"', raw, re.IGNORECASE)
print(f"Keywords: {tags[:3]}")

# Print any text mentioning DOI or Nature
for m in re.finditer(r'(.{0,80}(?:nature|doi|photonics).{0,80})', raw, re.IGNORECASE):
    txt = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    if len(txt) > 20:
        print(f"CTX: {txt[:200]}")
