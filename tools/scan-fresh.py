#!/usr/bin/env python3
"""Fetch full feeds and grep-dedup against existing content."""
import subprocess, xml.etree.ElementTree as ET, gzip, os

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

def items(url):
    p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
    try:
        data = p.stdout
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
        root = ET.fromstring(data)
    except (ET.ParseError, TypeError, Exception):
        return []
    out = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        if not t or len(t) < 25:
            continue
        out.append({"title": t, "link": (it.findtext("link") or "").strip(),
                    "desc": (it.findtext("description") or "").strip()[:250]})
    return out

sources = {
    "science": [
        ("ScienceDaily top", "https://www.sciencedaily.com/rss/top.xml"),
    ],
    "animals": [
        ("Good News Network", "https://www.goodnewsnetwork.org/feed/"),
    ],
    "listicles": [
        ("Listverse", "https://listverse.com/feed/"),
    ],
    "explainers": [
        ("HowStuffWorks", "https://recipes.howstuffworks.com/recipes.rss"),
        ("ScienceDaily earth", "https://www.sciencedaily.com/news/earth_climate/earth_science/"),
    ],
}

# Collect existing content titles/keywords for dedup
existing = []
for board in ["news", "blog", "trending"]:
    bdir = os.path.join("content", board)
    if os.path.isdir(bdir):
        for f in os.listdir(bdir):
            if f.endswith(".md"):
                existing.append(f)

for lane, srcs in sources.items():
    print(f"\n=== LANE: {lane} ===")
    for label, url in srcs:
        rows = items(url)
        print(f"  {label}: {len(rows)} items")
        checked = 0
        for r in rows:
            # Simple dedup: check if title words appear in any existing filename
            tlower = r["title"].lower()
            # Extract slug-like words
            words = [w.strip(".,;:!?\"'()[]") for w in tlower.replace(" — ", " ").replace("-", " ").split() if len(w) > 3]
            is_dup = False
            for ef in existing:
                efl = ef.lower()
                # Check if any 2+ consecutive title words appear in filename
                for i in range(len(words)-1):
                    phrase = " ".join(words[i:i+2])
                    if phrase in efl or phrase.replace(" ", "-") in efl:
                        is_dup = True
                        break
                if is_dup:
                    break
                # Also check full title keywords
                for w in words:
                    if len(w) > 5 and w in efl:
                        is_dup = True
                        break
            if not is_dup:
                print(f"    [NEW] {r['title'][:90]}")
                print(f"          url: {r['link']}")
                print(f"          desc: {r['desc'][:150]}")
                checked += 1
                if checked >= 8:
                    break
