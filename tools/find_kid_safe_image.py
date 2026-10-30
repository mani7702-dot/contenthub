#!/usr/bin/env python3
"""Test multiple queries against Wikimedia Commons to find a kid-safe gut bacteria illustration."""
import requests, os, io
from PIL import Image

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ContentHub/1.0 (image sourcing)"}
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".webm", ".ogg", ".ogv", ".pdf", ".djvu")
OK_LICENSE = ("public domain", "cc0", "cc by")
MAXW = 1600

def api(params):
    r = requests.get(API, params=params, headers=UA, timeout=25)
    r.raise_for_status()
    return r.json()

def search_files(query, limit=8):
    d = api({"action": "query", "format": "json", "generator": "search",
             "gsrsearch": query, "gsrlimit": limit, "gsrnamespace": 6,
             "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
             "iiurlwidth": MAXW})
    pages = (d.get("query") or {}).get("pages", {})
    out = []
    for pg in pages.values():
        ii = (pg.get("imageinfo") or [{}])[0]
        if not ii:
            continue
        ext = os.path.splitext(pg.get("title", ""))[1].lower()
        if ext in BAD_EXT:
            continue
        md = ii.get("extmetadata") or {}
        lic = (md.get("LicenseShortName") or {}).get("value", "").lower()
        if not any(k in lic for k in OK_LICENSE):
            continue
        out.append({"title": pg["title"], "url": ii.get("thumburl") or ii.get("url"),
                    "w": ii.get("thumbwidth") or ii.get("width"),
                    "h": ii.get("thumbheight") or ii.get("height"),
                    "lic": lic,
                    "artist": (md.get("Artist") or {}).get("value", "")})
    return out

def download(url):
    b = requests.get(url, headers=UA, timeout=40).content
    im = Image.open(io.BytesIO(b)).convert("RGB")
    if im.width < 500:
        return None
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.Resampling.LANCZOS)
    return im

queries = [
    "gut microbiome illustration bacteria",
    "digestive system bacteria illustration",
    "probiotic bacteria illustration",
    "human gut bacteria microscopic",
    "intestine microbiome cross section",
    "bifidobacterium bacteria",
    "good bacteria gut probiotics",
    "microbiome diagram children",
    "digestive tract illustration",
    "bacteria cell illustration",
    "healthy gut bacteria",
    "bifidobacterium longum",
]

for q in queries:
    try:
        cands = search_files(q, limit=8)
    except Exception as e:
        print(f"[{q}] API error: {e}")
        continue
    print(f"\n[{q}] Found {len(cands)} candidates:")
    for c in cands:
        # Check image dimensions and color diversity
        try:
            im = download(c["url"])
            if im is None:
                print(f"  SKIP (too small): {c['title']}")
                continue
            # Analyze: check for bright colors (kid-safe illustration)
            colors = im.getcolors(maxcolors=1000000)
            if colors:
                # Check if it's mostly black/white (avoid abstract art)
                non_bw = sum(cnt for cnt, rgb in colors if any(v < 240 for v in rgb[:3]) and any(v > 15 for v in rgb[:3]))
                total = sum(cnt for cnt, _ in colors)
                color_ratio = non_bw / total if total else 0
                top_colors = sorted(colors, key=lambda x: x[0], reverse=True)[:3]
                print(f"  {c['title']}: {c['w']}x{c['h']} lic={c['lic']} color_ratio={color_ratio:.2f}")
                print(f"    Top colors: {[(cnt, rgb) for cnt, rgb in top_colors[:3]]}")
                if color_ratio > 0.2 and c['w'] >= 800:
                    print(f"    *** POTENTIAL MATCH ***")
        except Exception as e:
            print(f"  Error: {e}")
