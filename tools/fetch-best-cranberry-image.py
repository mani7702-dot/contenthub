#!/usr/bin/env python3
"""Download the USDA cranberry image via Wikimedia API thumbnail URL."""
import requests, io, os, re
from PIL import Image

slug = "how-did-cranberry-juice-become-a-tooth-decay-fighter"
filepath = f"/home/ubuntu/contenthub/content/news/{slug}.md"
imgpath = f"/home/ubuntu/contenthub/assets/images/{slug}.jpg"

# Get the actual thumbnail URL from the Wikimedia API
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ContentHub/1.0 (image sourcing)"}

params = {
    "action": "query",
    "format": "json",
    "titles": "File:Cranberrys beim Ernten.jpeg",
    "prop": "imageinfo",
    "iiprop": "url|extmetadata|size|mime",
    "iiurlwidth": 1600,
}

r = requests.get(API, params=params, headers=UA, timeout=25)
d = r.json()
pages = d.get("query", {}).get("pages", {})
for pgid, pg in pages.items():
    ii = (pg.get("imageinfo") or [{}])[0]
    if not ii:
        continue
    url = ii.get("thumburl") or ii.get("url", "")
    print(f"Image URL: {url}")
    
    md = ii.get("extmetadata") or {}
    lic = (md.get("LicenseShortName") or {}).get("value", "").lower()
    artist = (md.get("Artist") or {}).get("value", "")
    artist_clean = re.sub(r"<[^>]+>", "", artist).strip()[:80]
    print(f"License: {lic}")
    print(f"Artist: {artist_clean}")

    b = requests.get(url, headers=UA, timeout=40).content
    im = Image.open(io.BytesIO(b)).convert("RGB")
    print(f"Size: {im.size}")

    if im.width > 1600:
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)

    os.makedirs(os.path.dirname(imgpath), exist_ok=True)
    im.save(imgpath, "JPEG", quality=82, optimize=True, progressive=True)
    rel = os.path.relpath(imgpath, "/home/ubuntu/contenthub").replace(os.sep, "/")
    print(f"Saved: {rel}")

    # Verify red cranberry pixels
    w, h = im.size
    red_count = 0
    red_total = 0
    for x in range(0, w, 10):
        for y in range(0, h, 10):
            px = im.getpixel((min(x, w-1), min(y, h-1)))
            r_val, g_val, b_val = px[0], px[1], px[2]
            red_total += 1
            if r_val > 120 and g_val < 80 and b_val < 80:
                red_count += 1
    red_pct = 100 * red_count / red_total if red_total > 0 else 0
    print(f"Red cranberry pixels: {red_pct:.1f}%")

    cap = f"Photo: {artist_clean} / {lic} / Wikimedia Commons" if artist_clean else f"Photo: {lic} / Wikimedia Commons"
    print(f"Caption: {cap}")

    # Update frontmatter
    txt = open(filepath, encoding="utf-8").read()
    txt = re.sub(r"^image:.*$", f"image: {rel}", txt, count=1, flags=re.M)
    txt = re.sub(r"^image_caption:.*$", f'image_caption: "{cap}"', txt, count=1, flags=re.M)
    open(filepath, "w", encoding="utf-8").write(txt)
    print("Frontmatter updated!")
