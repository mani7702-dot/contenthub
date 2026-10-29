#!/usr/bin/env python3
"""Download a specific cranberry image from Wikimedia Commons and update frontmatter."""
import requests, io, os, re
from PIL import Image

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ContentHub/1.0 (image sourcing)"}
MAXW = 1600

slug = "how-did-cranberry-juice-become-a-tooth-decay-fighter"
filepath = f"/home/ubuntu/contenthub/content/news/{slug}.md"
imgpath = f"/home/ubuntu/contenthub/assets/images/{slug}.jpg"

# Use a very specific query to get actual cranberry fruit images
queries = [
    "Vaccinium macrocarpon fruit cranberry",
    "fresh cranberries whole fruit",
]

downloaded = False
for query in queries:
    if downloaded:
        break
    print(f"=== Trying query: '{query}' ===")
    try:
        d = requests.get(API, params={
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": query,
            "gsrlimit": 8,
            "gsrnamespace": 6,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|size|mime",
            "iiurlwidth": MAXW,
        }, headers=UA, timeout=25).json()
        
        pages = (d.get("query") or {}).get("pages", {})
        for pg in pages.values():
            ii = (pg.get("imageinfo") or [{}])[0]
            if not ii:
                continue
            ext = os.path.splitext(pg.get("title", ""))[1].lower()
            if ext in (".svg", ".tif", ".tiff", ".gif", ".webm", ".ogg", ".ogv", ".pdf", ".djvu"):
                continue
            md = ii.get("extmetadata") or {}
            lic = (md.get("LicenseShortName") or {}).get("value", "").lower()
            if not any(k in lic for k in ("public domain", "cc0", "cc by")):
                continue
            
            url = ii.get("thumburl") or ii.get("url", "")
            title = pg.get("title", "")
            artist = (md.get("Artist") or {}).get("value", "")
            artist_clean = re.sub(r"<[^>]+>", "", artist).strip()[:80]
            
            print(f"  Candidate: {title}, License: {lic}, Size: {ii.get('thumbwidth', '?')}x{ii.get('thumbheight', '?')}")
            
            # Download
            try:
                b = requests.get(url, headers=UA, timeout=40).content
                im = Image.open(io.BytesIO(b)).convert("RGB")
                if im.width < 500:
                    print("  Skipped: width < 500")
                    continue
                if im.width > MAXW:
                    im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
                
                os.makedirs(os.path.dirname(imgpath), exist_ok=True)
                im.save(imgpath, "JPEG", quality=82, optimize=True, progressive=True)
                rel = os.path.relpath(imgpath, "/home/ubuntu/contenthub").replace(os.sep, "/")
                
                cap = f"Photo: {artist_clean} / {lic} / Wikimedia Commons" if artist_clean else f"Photo: {lic} / Wikimedia Commons"
                print(f"  Downloaded: {rel} ({im.size[0]}x{im.size[1]})")
                print(f"  Caption: {cap}")
                
                # Verify image content - check for red cranberry pixels
                w, h = im.size
                red_count = 0
                red_total = 0
                for x in range(0, w, 10):
                    for y in range(0, h, 10):
                        px = im.getpixel((min(x, w-1), min(y, h-1)))
                        r, g, b = px[0], px[1], px[2]
                        red_total += 1
                        # Cranberries are bright red: R high, G and B low
                        if r > 120 and g < 80 and b < 80:
                            red_count += 1
                red_pct = 100 * red_count / red_total if red_total > 0 else 0
                print(f"  Red cranberry pixels: {red_pct:.1f}%")
                
                if red_pct > 3:
                    # Update frontmatter
                    txt = open(filepath, encoding="utf-8").read()
                    txt = re.sub(r"^image:.*$", f"image: {rel}", txt, count=1, flags=re.M)
                    txt = re.sub(r"^image_caption:.*$", f'image_caption: "{cap}"', txt, count=1, flags=re.M)
                    open(filepath, "w", encoding="utf-8").write(txt)
                    print(f"  Frontmatter updated!")
                    downloaded = True
                else:
                    print(f"  Not cranberry-enough (red {red_pct:.1f}%), deleting and trying next")
                    os.remove(imgpath)
                    
            except Exception as e:
                print(f"  Download error: {e}")
                continue
                
    except Exception as e:
        print(f"  API error: {e}")
        continue

if not downloaded:
    print("\nNo suitable cranberry image found — will publish image-less")
