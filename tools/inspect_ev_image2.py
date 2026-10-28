#!/usr/bin/env python3
"""Inspect image content using PIL."""
from PIL import Image

path = "assets/images/how-did-scientists-make-electric-car-batteries-smaller-and-longer-lasting.jpg"
im = Image.open(path)
print(f"Size: {im.size}, Mode: {im.mode}")
print(f"Top-left: {im.getpixel((0, 0))}")
print(f"Center: {im.getpixel((im.width//2, im.height//2))}")
print(f"Top-right: {im.getpixel((im.width-1, 0))}")
print(f"Bottom-left: {im.getpixel((0, im.height-1))}")
# Resize for vision verification
small = im.resize((400, 300), Image.Resampling.LANCZOS)
small.save("/tmp/verify2.jpg", "JPEG", quality=85)
print("Resized to /tmp/verify2.jpg")
