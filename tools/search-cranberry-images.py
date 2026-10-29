#!/usr/bin/env python3
"""Search Wikimedia Commons more specifically for cranberry images."""
import requests, io, os
from PIL import Image

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ContentHub/1.0 (image sourcing)"}
MAXW = 1600

# Try a very specific search for cranberry images
queries = [
    "cranberry sauce fresh cranberries",
    "Vaccinium macrocarpon fruit",
    "cranberries in a glass jar",
]

for query in queries:
    print(f"\n=== Query: '{query}' ===")
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
            md = ii.get("extmetadata") or {}
            lic = (md.get("LicenseShortName") or {}).get("value", "").lower()
            print(f"  Title: {pg.get('title', '')}")
            print(f"  License: {lic}")
            print(f"  URL: {ii.get('thumburl') or ii.get('url', '')}")
            print(f"  Size: {ii.get('thumbwidth') or ii.get('width', '?')}x{ii.get('thumbheight') or ii.get('height', '?')}")
    except Exception as e:
        print(f"  Error: {e}")
