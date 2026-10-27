import subprocess, os, xml.etree.ElementTree as ET, gzip

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# BBC has multiple feeds
urls = [
    ("BBC Science & Env", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
    ("BBC World News", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("BBC World Service", "https://feeds.bbci.co.uk/news/world_service/rss.xml"),
]

for label, url in urls:
    try:
        p = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "25", "-A", UA, url], capture_output=True, timeout=30)
        data = p.stdout
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
        if len(data) == 0:
            print(f"{label}: EMPTY")
            continue
        try:
            root = ET.fromstring(data)
            items = list(root.iter("item"))
            print(f"\n{label}: {len(items)} items")
            for it in items:
                t = (it.findtext("title") or "").strip()
                if any(kw in t.lower() for kw in ["space", "moon", "mars", "star", "galaxy", "nasa", "rocket", "planet", "telescope", "orbit", "astronom", "spaceplane", "satellite", "probe", "jupiter", "venus", "apollo", "cosmic", "alien", "exoplanet", "supernova", "nebula"]):
                    l = (it.findtext("link") or "").strip()
                    print(f"  *** SPACE: {t}")
                    print(f"  URL: {l}")
        except Exception as e:
            print(f"{label}: Parse error: {e}")
    except Exception as e:
        print(f"{label}: Error: {e}")
