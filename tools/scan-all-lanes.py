#!/usr/bin/env python3
import subprocess, xml.etree.ElementTree as ET, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

def items(url):
    p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
    try:
        data = p.stdout
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
        root = ET.fromstring(data)
    except (ET.ParseError, TypeError):
        return []
    out = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        if not t or len(t) < 25:
            continue
        out.append({"title": t, "link": (it.findtext("link") or "").strip(),
                    "description": (it.findtext("description") or "").strip()[:200]})
    return out

sources = {
    "animals": [
        ("Good News Network", "https://www.goodnewsnetwork.org/feed/"),
        ("BBC Earth", "https://www.bbc.co.uk/news/science_env/rss"),
        ("ScienceDaily animals", "https://www.sciencedaily.com/news/plants_animals/animals/"),
    ],
    "science": [
        ("ScienceDaily top", "https://www.sciencedaily.com/rss/top.xml"),
        ("BBC Science", "https://feeds.bbc.co.uk/news/science_and_environment/rss.xml"),
        ("Smithsonian", "https://www.smithsonianmag.com/feed/"),
    ],
    "history": [
        ("Smithsonian", "https://www.smithsonianmag.com/feed/"),
        ("NPR History", "https://www.npr.org/rss/rss.php?f=1026"),
        ("Atlas Obscura", "https://www.atlasobscura.com/articles/rss"),
    ],
    "listicles": [
        ("Mental Floss", "https://mentalfloss.com/feeds/latest"),
        ("Listverse", "https://listverse.com/feed/"),
    ],
    "space": [
        ("NASA Image + Videos", "https://api.nasa.gov/rss/image-of-the-day.rss"),
        ("NASA APOD", "https://apod.nasa.gov/apod.rss"),
        ("Sky & Telescope", "https://skyandtelescope.org/feed/"),
    ],
    "explainers": [
        ("HowStuffWorks", "https://recipes.howstuffworks.com/recipes.rss"),
        ("ScienceDaily earth", "https://www.sciencedaily.com/news/earth_climate/earth_science/"),
    ],
}

for lane, srcs in sources.items():
    print(f"\n=== LANE: {lane} ===")
    for label, url in srcs:
        rows = items(url)
        print(f"  {label}: {len(rows)} items")
        for r in rows[:6]:
            print(f"    - {r['title'][:90]}")
