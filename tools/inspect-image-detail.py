#!/usr/bin/env python3
"""Detailed image content verification using PIL."""
from PIL import Image

path = "assets/images/how-did-a-texas-barber-return-128-000-he-found-at-an-atm-to-its-owner.jpg"
im = Image.open(path).convert("RGB")
w, h = im.size
print(f"Image size: {w}x{h}")

# Sample a grid of pixels to understand the image content
print("\n=== Grid sampling (every 200px) ===")
for y in range(0, h, 200):
    row = []
    for x in range(0, w, 200):
        row.append(im.getpixel((x, y)))
    print(f"  y={y}: {row}")

# Get pixel data as a flat list of tuples
pixels = []
for y in range(h):
    for x in range(w):
        pixels.append(im.getpixel((x, y)))

total = len(pixels)
green_count = sum(1 for r, g, b in pixels if g > r and g > b and g > 80)
dark_count = sum(1 for r, g, b in pixels if r < 40 and g < 40 and b < 40)
light_count = sum(1 for r, g, b in pixels if r > 200 and g > 200 and b > 200)
blue_gray_count = sum(1 for r, g, b in pixels if b > r and b > g and 50 < b < 230)

print(f"\n=== Color distribution ===")
print(f"Green-ish pixels (money?): {green_count}/{total} ({100*green_count//total}%)")
print(f"Dark pixels: {dark_count}/{total} ({100*dark_count//total}%)")
print(f"Light pixels: {light_count}/{total} ({100*light_count//total}%)")
print(f"Blue-gray pixels: {blue_gray_count}/{total} ({100*blue_gray_count//total}%)")

if dark_count > total // 2:
    print("\n=> Image has significant dark areas — likely a dark background with money or objects")
if green_count > 1000:
    print("\n=> Image has notable green tones — could be US currency visible")
