#!/usr/bin/env python3
"""Check what image was downloaded - find the Wikimedia source."""
import subprocess, re, json

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Search Wikimedia Commons for T cell + immune system
API = "https://commons.wikimedia.org/w/api.php"

# Check the file info
params = {
    "action": "query",
    "format": "json",
    "titles": "File:T_cells.jpg",
    "prop": "imageinfo",
    "iiprop": "url|extmetadata|size|mime",
    "iiurlwidth": 1600,
}
r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, API], capture_output=True)
# Actually let's search for images related to T cells
search_params = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": "T cell immune system",
    "srnamespace": 6,
    "srlimit": 10,
}
import urllib.parse
url = API + "?" + urllib.parse.urlencode(search_params)
p = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, url], capture_output=True)
data = json.loads(p.stdout)
for item in data.get("query", {}).get("search", []):
    title = item.get("title", "")
    pageid = item.get("pageid", "")
    print(f"Title: {title} (pageid: {pageid})")
    # Get page info for image description
    info_params = {
        "action": "query",
        "format": "json",
        "pageids": str(pageid),
        "prop": "images",
    }
    # Actually let's just get the imageinfo
    img_params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
    }
    url2 = API + "?" + urllib.parse.urlencode(img_params)
    p2 = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, url2], capture_output=True)
    try:
        data2 = json.loads(p2.stdout)
        pages = data2.get("query", {}).get("pages", {})
        for pid, pg in pages.items():
            ii = pg.get("imageinfo", [{}])[0]
            if ii:
                ext = ii.get("extmetadata", {})
                artist = (ext.get("Artist", {}).get("value", "") or "")[:100]
                lic = (ext.get("LicenseShortName", {}).get("value", "") or "")[:50]
                desc = (ext.get("ObjectName", {}).get("value", "") or "")[:100]
                url_img = ii.get("url", "")
                thumb_url = ii.get("thumburl", "")
                print(f"  Artist: {artist}")
                print(f"  License: {lic}")
                print(f"  Description: {desc}")
                print(f"  URL: {url_img[:100]}")
                print(f"  Thumb: {thumb_url[:100]}")
                print()
    except Exception as e:
        print(f"  Error: {e}")
