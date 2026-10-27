import subprocess, xml.etree.ElementTree as ET, sys, gzip

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

urls = [
    ("NASA Image + Videos", "https://api.nasa.gov/rss/image-of-the-day.rss"),
    ("NASA APOD", "https://apod.nasa.gov/apod.rss"),
    ("Sky & Telescope", "https://skyandtelescope.org/feed/"),
    ("ScienceDaily space", "https://www.sciencedaily.com/news/space_time/"),
]

for label, url in urls:
    try:
        p = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True, timeout=35)
        data = p.stdout
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
        if len(data) == 0:
            print(f"{label}: EMPTY RESPONSE")
            continue
        text = data.decode(errors='replace')[:300]
        try:
            root = ET.fromstring(data)
            items = list(root.iter("item"))
            print(f"{label}: {len(items)} items")
            for it in items[:3]:
                t = (it.findtext("title") or "").strip()
                if t:
                    print(f"  TITLE: {t}")
        except Exception as e:
            print(f"{label}: Parse error: {e}")
            print(f"  First 300 chars: {text}")
    except subprocess.TimeoutExpired:
        print(f"{label}: TIMEOUT")
    except Exception as e:
        print(f"{label}: Error: {e}")
