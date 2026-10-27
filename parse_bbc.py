import subprocess, xml.etree.ElementTree as ET, gzip, sys

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# BBC Science & Environment RSS - usually returns clean XML
url = "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"

p = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "25", "-A", UA, url], capture_output=True, timeout=30)
data = p.stdout

if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)

try:
    root = ET.fromstring(data)
    print(f"Root tag: {root.tag}")
    items = list(root.iter("item"))
    print(f"Total items: {len(items)}")
    for it in items:
        t = (it.findtext("title") or "").strip()
        l = (it.findtext("link") or "").strip()
        d = (it.findtext("description") or "").strip()[:300]
        print(f"\nTITLE: {t}")
        print(f"URL: {l}")
        print(f"DESC: {d}")
except Exception as e:
    print(f"Parse error: {e}")
    print(f"First 500 chars: {data[:500].decode(errors='replace')}")
