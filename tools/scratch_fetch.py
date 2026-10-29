#!/usr/bin/env python3
import subprocess, xml.etree.ElementTree as ET
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
BLOCK = ("war", "attack", "death toll", "killed", "murder", "court", "lawsuit", "covid",
         "pandemic", "election", "politic", "terror", "bomb", "shooting")

def items(url):
    p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
    try:
        data = p.stdout
        if data[:2] == b"\x1f\x8b":
            import gzip; data = gzip.decompress(data)
        root = ET.fromstring(data)
    except (ET.ParseError, TypeError):
        return []
    out = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        if not t or len(t) < 25:
            continue
        out.append({"title": t, "link": (it.findtext("link") or "").strip(),
                    "description": (it.findtext("description") or "").strip()[:200],
                    "blocked": any(b in t.lower() for b in BLOCK)})
    return out

# Check explainers and a couple other lanes that might have kid-safe content
CATEGORIES = {
    "explainers": [("HowStuffWorks", "https://recipes.howstuffworks.com/recipes.rss"),
                   ("ScienceDaily earth", "https://www.sciencedaily.com/news/earth_climate/earth_science/")],
    "animals": [("Good News Network", "https://www.goodnewsnetwork.org/feed/"),
                ("BBC Earth", "https://www.bbc.co.uk/news/science_env/rss"),
                ("ScienceDaily animals", "https://www.sciencedaily.com/news/plants_animals/animals/")],
    "science": [("ScienceDaily top", "https://www.sciencedaily.com/rss/top.xml"),
                ("BBC Science & Env", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
                ("Smithsonian", "https://www.smithsonianmag.com/feed/")],
    "listicles": [("Mental Floss", "https://mentalfloss.com/feeds/latest"),
                  ("Listverse", "https://listverse.com/feed/")],
}

for lane in ["explainers", "animals", "science", "listicles"]:
    rows = []
    for _label, url in CATEGORIES[lane]:
        rows += items(url)
    print(f"=== {lane}: {len(rows)} items fetched ===")
    for r in rows:
        tag = "BLOCKED" if r["blocked"] else "ok"
        print(f'  [{tag}] {r["title"]}')
        print(f'  url: {r["link"]}')
        if r["description"]:
            print(f'  desc: {r["description"]}')
    print()
