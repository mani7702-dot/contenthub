import subprocess, xml.etree.ElementTree as ET, sys

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
urls = [
    ("NASA Image + Videos", "https://api.nasa.gov/rss/image-of-the-day.rss"),
    ("NASA APOD", "https://apod.nasa.gov/apod.rss"),
    ("Sky & Telescope", "https://skyandtelescope.org/feed/"),
]

for label, url in urls:
    p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
    print(f"{label}: status={p.returncode}, len={len(p.stdout)}, stderr={p.stderr[:200].decode() if p.stderr else 'none'}")
    data = p.stdout
    if data[:2] == b"\x1f\x8b":
        import gzip; data = gzip.decompress(data)
    try:
        root = ET.fromstring(data)
        items = root.iter("item")
        count = 0
        for it in items:
            t = (it.findtext("title") or "").strip()
            if t and len(t) > 25:
                print(f"  TITLE: {t}")
                count += 1
        print(f"  Total items with titles: {count}")
    except Exception as e:
        print(f"  Parse error: {e}")
        print(f"  First 500 chars: {data[:500].decode(errors='replace')}")
