#!/usr/bin/env python3
"""Fetch a better image for the laser memory article."""
import requests, io, os
from PIL import Image

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ContentHub/1.0 (image sourcing)"}
MAXW = 1600

def api(params):
    r = requests.get(API, params=params, headers=UA, timeout=25)
    return r.json()

def search_files(query, limit=15):
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
        import os
        ext = os.path.splitext(pg.get("title", ""))[1].lower()
        bad_ext = (".svg", ".tif", ".tiff", ".gif", ".webm", ".ogg", ".ogv", ".pdf", ".djvu")
        if ext in bad_ext:
            continue
        md = ii.get("extmetadata") or {}
        lic = (md.get("LicenseShortName") or {}).get("value", "").lower()
        ok_licenses = ("public domain", "cc0", "cc by")
        if not any(k in lic for k in ok_licenses):
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
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    return im

# Try queries specifically about laser, computer chips, data storage
queries = [
    "laser beam computer chip technology",
    "laser pulse data storage",
    "computer memory chip closeup",
    "laser technology abstract",
    "microprocessor computer chip",
]

slug = "how-did-a-tiny-laser-beam-make-computer-memory-1000-times-faster"
out_path = f"assets/images/{slug}.jpg"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

for query in queries:
    print(f"\nTrying query: '{query}'")
    try:
        cands = search_files(query, limit=15)
        print(f"  Found {len(cands)} candidates")
        for c in cands:
            try:
                im = download(c["url"])
            except Exception as e:
                print(f"  Download failed: {e}")
                continue
            if im is None:
                continue
            
            # Check if it's a photo-like image (not a map, not a screenshot)
            # Sample some pixels
            w, h = im.size
            center_pixel = im.getpixel((w//2, h//2))
            corner_pixel = im.getpixel((0, 0))
            
            # Check non-grayscale ratio
            colorful = 0
            total = 0
            for y in range(0, h, max(1, h//20)):
                for x in range(0, w, max(1, w//20)):
                    r, g, b = im.getpixel((x, y))
                    if max(r,g,b) - min(r,g,b) > 20:
                        colorful += 1
                    total += 1
            
            ratio = colorful / total if total > 0 else 0
            print(f"  Candidate: {c['title'][:60]}")
            print(f"    Size: {w}x{h}, Colorful ratio: {ratio:.1%}, Center: {center_pixel}, Corner: {corner_pixel}")
            print(f"    License: {c['lic']}")
            
            # We want a photo-like image (high natural color variance) or a clear tech image
            # Not a map (which has uniform colors) or a screenshot
            if ratio > 0.05:  # At least 5% colorful - likely a photo
                im.save(out_path, "JPEG", quality=82, optimize=True, progressive=True)
                artist = c['artist'][:120] if c['artist'] else ""
                # Clean HTML from artist
                import re
                clean_artist = re.sub(r"<[^>]+>", "", artist).strip()[:80]
                cap = f"Photo: {clean_artist} / {c['lic']} / Wikimedia Commons" if clean_artist else f"Photo: Wikimedia Commons / {c['lic']}"
                print(f"    SELECTED! Saved to {out_path}")
                print(f"    Caption: {cap}")
                
                # Update frontmatter
                path = f"content/news/{slug}.md"
                txt = open(path, encoding="utf-8").read()
                import re
                txt = re.sub(r'^image:.*$', f"image: {out_path.replace(chr(92), '/').replace('assets/images/', 'assets/images/')}", txt, count=1, flags=re.M)
                # Actually use relative path
                rel = os.path.relpath(out_path, ".")
                txt = re.sub(r'^image:.*$', f"image: {rel}", txt, count=1, flags=re.M)
                txt = re.sub(r'^image_caption:.*$', f'image_caption: "{cap}"', txt, count=1, flags=re.M)
                open(path, "w", encoding="utf-8").write(txt)
                print(f"    Frontmatter updated!")
                
                # Also save caption
                with open("/tmp/laser_caption.txt", "w") as f:
                    f.write(cap)
                exit(0)
    except Exception as e:
        print(f"  Error: {e}")
        continue

print("\nNo suitable image found after all queries")
