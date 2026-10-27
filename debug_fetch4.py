import subprocess, os

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
os.makedirs("/tmp/raw", exist_ok=True)

# Try NASA's main RSS feeds and other space sources
urls = [
    ("NASA Top News", "https://www.nasa.gov/rss/toprss"),
    ("NASA Earth", "https://earthobservatory.nasa.gov/feeds/earth-rss.php"),
    ("ESA News", "https://www.esa.int/Science_Exploration/Herschel_Cosmic_Evolved_Satellite_2/rss"),
    ("ESA Top News", "https://www.esa.int/News_e/ESA_rss_news_top_2e247c9d8796a3114950e8d4c88e7c2c.rss"),
    ("ESA Science", "https://www.esa.int/Science_Exploration/Space_Science/rss"),
    ("ESA Space Technology", "https://www.esa.int/Enabling_Support/Space_Technology/rss"),
    ("Phys.org Space", "https://phys.org/rss/earth-news/space-exploration/"),
    ("Phys.org Astronomy", "https://phys.org/rss/earth-news/astronomy/"),
]

for label, url in urls:
    try:
        p = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "25", "-A", UA, url], capture_output=True, timeout=30)
        data = p.stdout
        if len(data) == 0:
            print(f"{label}: EMPTY")
            continue
        # Check if it's XML
        text = data[:500].decode(errors='replace')
        if "<rss" in text or "<?xml" in text:
            print(f"{label}: XML, len={len(data)}")
        elif "<html" in text.lower():
            print(f"{label}: HTML (blocked), len={len(data)}")
        else:
            print(f"{label}: Unknown format, len={len(data)}, first200={text[:200]}")
    except Exception as e:
        print(f"{label}: Error: {e}")
