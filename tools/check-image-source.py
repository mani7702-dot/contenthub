#!/usr/bin/env python3
"""Check what image was downloaded — query Wikimedia for the title of the saved file."""
import requests, json
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ContentHub/1.0 (image sourcing)"}

# Search for "lightning bolt nature" — first 8 results
for q in ["lightning bolt nature", "CPR first aid rescue"]:
    d = requests.get(API, params={
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": q, "gsrlimit": 8, "gsrnamespace": 6,
        "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
        "iiurlwidth": 1600
    }, headers=UA, timeout=25).json()
    
    pages = (d.get("query") or {}).get("pages", {})
    print(f"\n=== Query: '{q}' ({len(pages)} results) ===")
    for pg in pages.values():
        ii = (pg.get("imageinfo") or [{}])[0]
        if not ii:
            continue
        md = ii.get("extmetadata") or {}
        lic = (md.get("LicenseShortName") or {}).get("value", "")
        artist = (md.get("Artist") or {}).get("value", "")
        w = ii.get("thumbwidth") or ii.get("width")
        h = ii.get("thumbheight") or ii.get("height")
        print(f"  Title: {pg.get('title', '')}")
        print(f"  Size: {w}x{h}, License: {lic}")
        print(f"  Artist: {artist[:100]}")
