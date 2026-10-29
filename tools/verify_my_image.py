#!/usr/bin/env python3
"""Verify image content for the NYC cleanup article."""
from PIL import Image
path = "assets/images/how-did-a-new-yorker-named-service-clean-up-a-brooklyn-dumping-site-all-on-his-own.jpg"
im = Image.open(path)
print(f"Size: {im.size}, Mode: {im.mode}")
print(f"Top-left: {im.getpixel((0, 0))}")
print(f"Center: {im.getpixel((im.width//2, im.height//2))}")
print(f"Bottom-right: {im.getpixel((im.width-1, im.height-1))}")
# Sample a few more pixels
w, h = im.size
for y in range(0, h, h//6):
    for x in range(0, w, w//6):
        print(f"  Pixel ({x},{y}): {im.getpixel((x, y))}")
