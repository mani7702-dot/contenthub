#!/usr/bin/env python3
"""Check what Wikimedia images were returned for our search."""
import requests, json

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ContentHub/1.0 (image sourcing)"}

params = {
    "action": "query", "format": "json",
    "generator": "search", "gsrsearch": "community volunteering helping others",
    "gsrlimit": 8, "gsrnamespace": 6,
    "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": 1600
}
r = requests.get(API, params=params, headers=UA, timeout=25)
data = r.json()
pages = (data.get("query") or {}).get("pages", {})
for pg in pages.values():
    title = pg.get("title", "")
    ii = (pg.get("imageinfo") or [{}])[0]
    if ii:
        md = ii.get("extmetadata") or {}
        cat = (md.get("Categories") or {}).get("value", "")
        artist = (md.get("Artist") or {}).get("value", "")
        desc = (md.get("ImageDescription") or {}).get("value", "")
        lic = (md.get("LicenseShortName") or {}).get("value", "")
        print(f"Title: {title}")
        print(f"License: {lic}")
        print(f"Artist: {artist[:150]}")
        print(f"Categories: {cat[:200]}")
        print(f"Desc: {desc[:300]}")
        print("---")
