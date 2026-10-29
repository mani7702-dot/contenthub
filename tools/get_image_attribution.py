#!/usr/bin/env python3
"""Get Wikimedia image metadata for attribution via API."""
import requests, json

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
filename = "Coconuts - single and cracked open.jpg"

url = "https://commons.wikimedia.org/w/api.php"
params = {
    "action": "query",
    "format": "json",
    "prop": "imageinfo",
    "titles": f"File:{filename}",
    "iiprop": "extmetadata",
    "iiextmetadata": "*",
}
headers = {"User-Agent": UA}
r = requests.get(url, params=params, headers=headers, timeout=30)
data = r.json()
pages = data.get("query", {}).get("pages", {})
for page in pages.values():
    if "imageinfo" in page and page["imageinfo"]:
        info = page["imageinfo"][0]
        ext = info.get("extmetadata", {})
        if ext:
            print("=== Image Metadata ===")
            for key, val in ext.items():
                if isinstance(val, dict) and "value" in val:
                    v = val["value"]
                    if isinstance(v, str):
                        print(f"  {key}: {v[:300]}")
                    else:
                        print(f"  {key}: {str(v)[:300]}")
                elif isinstance(val, str):
                    print(f"  {key}: {val[:300]}")
                elif isinstance(val, (int, float)):
                    print(f"  {key}: {val}")
                else:
                    print(f"  {key}: {str(val)[:300]}")
