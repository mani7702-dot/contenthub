#!/usr/bin/env python3
"""Check what image was downloaded by looking at EXIF or file details."""
from PIL import Image
import os, struct

path = "assets/images/how-do-our-immune-cells-feel-the-world-around-them-with-a-hidden-sense-of-touch.jpg"
im = Image.open(path)
print(f"Format: {im.format}")
print(f"Size: {im.size}")
print(f"Mode: {im.mode}")
print(f"File size: {os.path.getsize(path)} bytes")

# Check EXIF data for any clues
try:
    exif = im.getexif()
    if exif:
        for tag_id, value in exif.items():
            from PIL.ExifTags import TAGS
            tag = TAGS.get(tag_id, tag_id)
            if isinstance(value, str) and len(value) < 500:
                print(f"EXIF {tag}: {value}")
except Exception as e:
    print(f"No EXIF: {e}")

# Check if it's a Wikimedia image - look at the first few bytes
# Wikimedia images often have comments
# Let's get basic pixel statistics
import numpy as np
arr = np.array(im)
print(f"Pixel stats: min={arr.min()}, max={arr.max()}, mean={arr.mean():.1f}")
print(f"Unique colors (approx): {len(np.unique(arr.reshape(-1, arr.shape[-1]), axis=0))}")

# Check for color distribution - is this mostly blue (immune cells), 
# or does it have text/diagrams?
# Sample some pixels
print(f"\nTop-left corner pixel: {arr[0, 0]}")
print(f"Center pixel: {arr[arr.shape[0]//2, arr.shape[1]//2]}")
print(f"Bottom-right pixel: {arr[-1, -1]}")
