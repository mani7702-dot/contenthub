#!/usr/bin/env python3
"""Check which Wikimedia file was actually downloaded by re-querying with the same search."""
import requests
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ContentHub/1.0 (image sourcing)"}

# The fetch-images.py script tried these queries in order
# First query: "lightning strike rescue CPR"  -> NO usable image
# Second query: "lightning bolt nature" + "CPR first aid rescue" -> OK
# The script picks the first valid candidate from the first successful query

for q in ["lightning bolt nature", "CPR first aid rescue"]:
    d = requests.get(API, params={
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": q, "gsrlimit": 8, "gsrnamespace": 6,
        "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
        "iiurlwidth": 1600
    }, headers=UA, timeout=25).json()
    
    pages = (d.get("query") or {}).get("pages", {})
    print(f"\n=== Query: '{q}' ===")
    for pg in pages.values():
        ii = (pg.get("imageinfo") or [{}])[0]
        if not ii:
            continue
        ext_mime = ii.get("mime", "")
        thumb_url = ii.get("thumburl") or ii.get("url", "")
        w = ii.get("thumbwidth") or ii.get("width", 0)
        h = ii.get("thumbheight") or ii.get("height", 0)
        if w == 1600 and h == 1067:
            title = pg.get("title", "")
            md = ii.get("extmetadata") or {}
            lic = (md.get("LicenseShortName") or {}).get("value", "")
            artist_raw = (md.get("Artist") or {}).get("value", "")
            import re
            artist_clean = re.sub(r"<[^>]+>", "", artist_raw).strip()
            print(f"  MATCH: {title} ({w}x{h})")
            print(f"  License: {lic}")
            print(f"  Artist: {artist_clean[:120]}")
