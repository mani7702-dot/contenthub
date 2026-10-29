import re

# Bing News RSS results
try:
    data = open('/tmp/bing-eclipse.xml', encoding='utf-8').read()
    items = re.findall(r'<item>(.*?)</item>', data, re.S)
    print('items:', len(items))
    for it in items[:10]:
        t = re.search(r'<title>(.*?)</title>', it)
        l = re.search(r'<link>(.*?)</link>', it)
        s = re.search(r'<(?:News:)?Source>(.*?)</(?:News:)?Source>', it)
        if t:
            src = s.group(1).strip() if s else '?'
            print(f"{src} | {t.group(1).strip()[:110]}")
            if l:
                print(f"  LINK: {l.group(1).strip()[:200]}")
except FileNotFoundError:
    print("No bing-eclipse.xml file found")

# Also fetch the ScienceDaily article's cited original source
# Look for the journal DOI link in the SD article
with open('/tmp/sd-eclipse.html', encoding='utf-8') as f:
    html = f.read()
# Find doi.org links
dois = re.findall(r'href="(https?://doi\.org/[^"]+)"', html)
print("DOIS:", dois[:5])
# Find any external links to original research
ext = re.findall(r'href="(https?://(?!www\.sciencedaily|facebook|twitter|reddit|substack)[^"]+)"', html)
for e in ext[:10]:
    print("EXT:", e)
