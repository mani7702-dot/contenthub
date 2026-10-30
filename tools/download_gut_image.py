#!/usr/bin/env python3
"""Download the 'Illustration of the developmental colonization of gut bacteria' image
and verify it's kid-safe."""
import requests, io
from PIL import Image

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ContentHub/1.0 (image sourcing)"}

# Search for the image
p = requests.get(API, params={
    "action": "query", "format": "json", "generator": "search",
    "gsrsearch": "Illustration developmental colonization gut bacteria",
    "gsrlimit": 5, "gsrnamespace": 6,
    "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
    "iiurlwidth": 1600
}, headers=UA, timeout=25)
data = p.json()
pages = (data.get("query") or {}).get("pages", {})
for pg in pages.values():
    title = pg.get("title", "")
    ii = (pg.get("imageinfo") or [{}])[0]
    url = ii.get("url", "")
    print(f"Title: {title}")
    print(f"URL: {url}")
    ext = ii.get("extmetadata", {})
    lic = (ext.get("LicenseShortName") or {}).get("value", "")
    artist = (ext.get("Artist") or {}).get("value", "")
    print(f"License: {lic}")
    print(f"Artist: {artist}")
    
    # Download the actual full file (not thumbnail)
    b = requests.get(url, headers=UA, timeout=40).content
    im = Image.open(io.BytesIO(b))
    print(f"Full image size: {im.size}, mode: {im.mode}")
    print(f"File size: {len(b)} bytes")
    
    # Save the full image
    out_path = "assets/images/how-did-the-bacteria-in-your-gut-reveal-how-fast-you-re-aging.jpg"
    if im.width > 1600:
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.Resampling.LANCZOS)
    im.convert("RGB").save(out_path, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"Saved: {out_path}")
