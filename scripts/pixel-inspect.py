#!/usr/bin/env python3
"""Detailed pixel inspection of the image."""
from PIL import Image
import os

src = "assets/images/how-did-a-stranger-pay-420-for-a-group-s-lunch-in-south-korea.jpg"
im = Image.open(src)
print(f"Size: {im.size}, Mode: {im.mode}")
print(f"File: {os.path.getsize(src)} bytes")

# Sample a grid of pixels
print("\n=== Pixel grid (every 200px) ===")
for y in range(0, im.height, 200):
    row = []
    for x in range(0, im.width, 200):
        row.append(f"({x},{y}): {im.getpixel((x, y))}")
    print(" | ".join(row))

# Check overall color distribution
# Sample center regions
w, h = im.size
print(f"\n=== Center region samples ===")
for y in range(h//2 - 100, h//2 + 100, 50):
    for x in range(w//2 - 100, w//2 + 100, 50):
        px = im.getpixel((x, y))
        r, g, b = px[0], px[1], px[2]
        # Classify color
        if r > 200 and g > 200 and b > 200:
            cat = "bright/white"
        elif r > 150 and g > 100 and b < 100:
            cat = "warm/yellow"
        elif r > 150 and abs(g - r) < 30 and abs(b - r) < 30:
            cat = "bright/neutral"
        elif r < 100 and g < 100 and b < 100:
            cat = "dark"
        else:
            cat = "mid-tone"
        print(f"  ({x},{y}): {px} -> {cat}")
