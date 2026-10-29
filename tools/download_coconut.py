#!/usr/bin/env python3
"""Download a specific coconut image from Wikimedia Commons."""
import requests
from PIL import Image
import os

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
filename = "Coconuts - single and cracked open.jpg"

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
        info = page["imageinfo"][0]
        download_url = info.get("url", "")
        print(f"Download URL: {download_url}")
        
        # Download the image
        r2 = requests.get(download_url, headers={"User-Agent": UA}, timeout=60)
        dest = "/home/ubuntu/contenthub/assets/images/coconut-jet-fuel.jpg"
        with open(dest, "wb") as f:
            f.write(r2.content)
        print(f"Downloaded to {dest}")
        
        # Verify
        im = Image.open(dest)
        print(f"Size: {im.size}, Mode: {im.mode}")
        print(f"Center pixel: {im.getpixel((im.width//2, im.height//2))}")
        
        # Check metadata for caption
        metadata = info.get("metadata", {})
        for key in metadata:
            if isinstance(metadata[key], dict) and "value" in metadata[key]:
                val = metadata[key]["value"]
                if val and isinstance(val, str) and ("author" in key.lower() or "credit" in key.lower() or "license" in key.lower()):
                    print(f"  {key}: {val[:100]}")
        
        # Get the description
        description = info.get("description", "")
        print(f"Description: {description[:200]}")
