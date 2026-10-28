#!/usr/bin/env python3
"""Search Wikimedia Commons for baseball-related images and inspect results."""
import subprocess, json, html

API = "https://commons.wikimedia.org/w/api.php"
UA = "Mozilla/5.0 (ContentHub image sourcing)"

# Search for baseball field images
params = {
    "action": "query",
    "format": "json",
    "generator": "search",
    "gsrsearch": "baseball field",
    "gsrlimit": 10,
    "gsrnamespace": 6,
    "prop": "imageinfo",
    "iiprop": "url|extmetadata|size|mime",
    "iiurlwidth": 1600,
}

r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "--data-urlencode", "action=query",
    "--data-urlencode", "format=json",
    "--data-urlencode", "generator=search",
    "--data-urlencode", "gsrsearch=baseball field",
    "--data-urlencode", "gsrlimit=10",
    "--data-urlencode", "gsrnamespace=6",
    "--data-urlencode", "prop=imageinfo",
    "--data-urlencode", "iiprop=url|extmetadata|size|mime",
    "--data-urlencode", "iiurlwidth=1600",
    API], capture_output=True, text=True)

data = json.loads(r.stdout)
pages = data.get("query", {}).get("pages", {})
for pgid, pg in pages.items():
    title = pg.get("title", "")
    ii = (pg.get("imageinfo") or [{}])[0]
    if not ii:
        continue
    desc_url = ii.get("thumburl") or ii.get("url")
    md = ii.get("extmetadata") or {}
    lic = (md.get("LicenseShortName") or {}).get("value", "")
    artist = (md.get("Artist") or {}).get("value", "")
    w = ii.get("thumbwidth") or ii.get("width")
    h = ii.get("thumbheight") or ii.get("height")
    mime = ii.get("mime", "")
    print(f"Title: {title}")
    print(f"URL: {desc_url}")
    print(f"Size: {w}x{h}, MIME: {mime}")
    print(f"License: {lic}")
    print(f"Artist: {artist[:80]}")
    print("---")
