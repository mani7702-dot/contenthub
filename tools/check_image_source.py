#!/usr/bin/env python3
"""Check what image was downloaded from Wikimedia."""
import requests, json

UA = {"User-Agent": "ContentHub/1.0 (image sourcing)"}
API = "https://commons.wikimedia.org/w/api.php"

# Search for the exact images we downloaded
# The image was found via "optical data storage laser memory" or "laser data storage computer drive"
# Let's re-run the search that succeeded and get the actual filename/title
params = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": "optical data storage laser memory",
    "srnamespace": 6,
    "srprop": "snippet",
    "srlimit": 10
}

r = requests.get(API, params=params, headers=UA, timeout=30)
data = r.json()
results = data.get("query", {}).get("search", [])
print("=== Search: 'optical data storage laser memory' ===")
for item in results:
    print(f"Title: {item.get('title', 'N/A')}")
    print(f"Snippet: {item.get('snippet', 'N/A')[:150]}")
    print()

# Check file info for potential matches
params2 = {
    "action": "query",
    "format": "json",
    "generator": "search",
    "gsrsearch": "laser data storage computer drive",
    "gsrnamespace": 6,
    "gsrlimit": 10,
    "prop": "imageinfo",
    "iiprop": "url|extmetadata|size|mime",
    "iiurlwidth": 1600
}

r2 = requests.get(API, params=params2, headers=UA, timeout=30)
data2 = r2.json()
pages = (data2.get("query") or {}).get("pages", {})
print("\n=== Search: 'laser data storage computer drive' ===")
for pgid, pg in pages.items():
    title = pg.get("title", "N/A")
    ii = (pg.get("imageinfo") or [{}])[0]
    ext = ii.get("extmetadata", {}) or {}
    print(f"  Title: {title}")
    print(f"  URL: {ii.get('url', 'N/A')[:100]}")
    artist = ext.get("Artist", {}).get("value", "")
    license_short = ext.get("LicenseShortName", {}).get("value", "")
    print(f"  Artist: {artist[:80]}")
    print(f"  License: {license_short}")
    print()
