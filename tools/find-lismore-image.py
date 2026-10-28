#!/usr/bin/env python3
"""Search Wikimedia Commons API directly for Lismore images."""
import requests, json, os, io
from PIL import Image

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ContentHub/1.0 (image sourcing)"}

queries = [
    "Lismore Scotland cathedral ruins",
    "Lismore Inner Hebrides Scotland aerial",
    "Celtic monastery Scotland archaeological site",
    "Saint Moluag Lismore Scotland",
]

for q in queries:
    print(f"\n=== Query: {q} ===")
    try:
        r = requests.get(API, params={
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": q,
            "gsrlimit": 5,
            "gsrnamespace": 6,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|size|mime",
            "iiurlwidth": 1600,
        }, headers=UA, timeout=25)
        d = r.json()
        pages = (d.get("query") or {}).get("pages", {})
        if not pages:
            print(f"  No results")
            continue
        for pg in pages.values():
            ii = (pg.get("imageinfo") or [{}])[0]
            if not ii:
                continue
            import os as _os
            ext = _os.path.splitext(pg.get("title", ""))[1].lower()
            md = ii.get("extmetadata") or {}
            lic = (md.get("LicenseShortName") or {}).get("value", "").lower()
            print(f"  Title: {pg['title']}")
            print(f"  License: {lic}")
            print(f"  URL: {ii.get('url', 'N/A')}")
            print(f"  Size: {ii.get('width', '?')}x{ii.get('height', '?')}")
            if any(k in lic for k in ("public domain", "cc0", "cc by")):
                print(f"  *** LICENSE OK ***")
    except Exception as e:
        print(f"  Error: {e}")

# Try sleep before retry
import time
print("\n\n=== Sleeping 30s before retry ===")
time.sleep(30)

# Try a simpler search
for q in ["Lismore Scotland cathedral"]:
    print(f"\n=== Retry Query: {q} ===")
    try:
        r = requests.get(API, params={
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": q,
            "gsrlimit": 5,
            "gsrnamespace": 6,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|size|mime",
            "iiurlwidth": 1600,
        }, headers=UA, timeout=25)
        d = r.json()
        pages = (d.get("query") or {}).get("pages", {})
        if not pages:
            print(f"  No results")
            continue
        for pg in pages.values():
            ii = (pg.get("imageinfo") or [{}])[0]
            if not ii:
                continue
            ext = os.path.splitext(pg.get("title", ""))[1].lower()
            md = ii.get("extmetadata") or {}
            lic = (md.get("LicenseShortName") or {}).get("value", "").lower()
            print(f"  Title: {pg['title']}")
            print(f"  License: {lic}")
            print(f"  URL: {ii.get('url', 'N/A')}")
            if any(k in lic for k in ("public domain", "cc0", "cc by")):
                print(f"  *** LICENSE OK ***")
    except Exception as e:
        print(f"  Error: {e}")
