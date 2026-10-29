#!/usr/bin/env python3
"""
Download a coconut image from Wikimedia Commons using a simpler approach.
"""
import requests
from PIL import Image
import os

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Search for coconut images on Wikimedia
url = "https://commons.wikimedia.org/w/api.php"
params = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": "coconut",
    "srnamespace": 6,
    "srfileiki": "bitmap",
    "srlimit": 20,
}
headers = {"User-Agent": UA}
try:
    r = requests.get(url, params=params, headers=headers, timeout=30)
    results = r.json().get("query", {}).get("search", [])
    print(f"Found {len(results)} results for 'coconut'")
    for item in results:
        title = item.get("title", "")
        filename = title.replace("File:", "")
        if not filename.lower().endswith((".jpg", ".jpeg")):
            continue
        print(f"  {filename}")
except Exception as e:
    print(f"Error: {e}")
