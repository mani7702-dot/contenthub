#!/usr/bin/env python3
"""Verify the downloaded image content more carefully."""
from PIL import Image
import os

path = "assets/images/how-do-our-immune-cells-feel-the-world-around-them-with-a-hidden-sense-of-touch.jpg"
im = Image.open(path)

# Try resizing the full image to 400px wide
w, h = im.size
new_h = round(h * 400 / w)
small = im.resize((400, new_h), Image.Resampling.LANCZOS)
small.save("/tmp/verify_small.jpg", "JPEG", quality=85)
print(f"Original size: {im.size}")
print(f"Small size: {small.size}")
print(f"Small file: {os.path.getsize('/tmp/verify_small.jpg')} bytes")

# Crop center 400x300
left = (w - 400) // 2
top = (h - 300) // 2
crop = im.crop((left, top, left + 400, top + 300))
crop.save("/tmp/verify_center.jpg", "JPEG", quality=85)
print(f"Center crop saved: {crop.size}")
