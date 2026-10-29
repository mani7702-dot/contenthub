#!/usr/bin/env python3
"""
Search Wikimedia Commons API for coconut images and jet engine images separately.
"""
import requests
import os
import re
from PIL import Image

UA = "Mozilla/5.0 (ContentHub picker; contact andugulanani722@gmail.com)"

def search_wikimedia(query, limit=10):
    """Search Wikimedia Commons for images."""
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srnamespace": 6,
        "srfileiki": "bitmap",
        "srlimit": limit,
    }
    headers = {"User-Agent": UA}
    r = requests.get(url, params=params, headers=headers, timeout=30)
    results = r.json().get("query", {}).get("search", [])
    return results

def get_image_info(filename):
    """Get image info from Wikimedia."""
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "titles": f"File:{filename}",
        "iiprop": "url|metadata",
        "iiurlwidth": 1200,
    }
    headers = {"User-Agent": UA}
    r = requests.get(url, params=params, headers=headers, timeout=30)
    pages = r.json().get("query", {}).get("pages", {})
    for page in pages.values():
        if "imageinfo" in page and page["imageinfo"]:
            return page["imageinfo"][0]
    return None

def download_image(url, path):
    """Download an image from URL."""
    headers = {"User-Agent": UA}
    r = requests.get(url, headers=headers, timeout=60, stream=True)
    if r.status_code == 200:
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    return False

# Try different queries
queries = [
    "coconut oil",
    "coconut tree",
    "jet engine",
    "aviation fuel",
    "airplane jet engine",
    "coconut fruit",
]

for q in queries:
    print(f"\n=== Searching: {q} ===")
    results = search_wikimedia(q, limit=8)
    for item in results:
        title = item.get("title", "")
        filename = title.replace("File:", "")
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        info = get_image_info(filename)
        if not info:
            continue
        download_url = info.get("url", "")
        desc = item.get("snippet", "")
        print(f"  FILENAME: {filename}")
        print(f"  DESC: {desc[:100]}")
        
        # Try to download
        dest = f"/tmp/test_img.jpg"
        if download_image(download_url, dest):
            im = Image.open(dest)
            print(f"  SIZE: {im.size}, MODE: {im.mode}")
            print(f"  CENTER: {im.getpixel((im.width//2, im.height//2))}")
