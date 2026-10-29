#!/usr/bin/env python3
"""Quick pixel inspection of a downloaded image to verify relevance."""
import sys
from PIL import Image

path = sys.argv[1] if len(sys.argv) > 1 else "assets/images/how-did-magma-store-a-hidden-oxygen-tank-deep-inside-earth-and-could-it-have-filled-our-at.jpg"
im = Image.open(path)
w, h = im.size
print(f"Size: {w}x{h}, Mode: {im.mode}")

# Sample grid of pixels
step_x, step_y = max(w // 10, 1), max(h // 10, 1)
print("\nPixel grid (R,G,B):")
for y in range(0, h, step_y):
    row = []
    for x in range(0, w, step_x):
        px = im.getpixel((x, y))
        if isinstance(px, tuple) and len(px) >= 3:
            row.append(px[:3])
        else:
            row.append(px)
    print(f"  Y={y}: {row[:8]}")

# Non-black pixel ratio
non_black = 0
total = 0
for x in range(0, w, 5):
    for y in range(0, h, 5):
        px = im.getpixel((x, y))
        total += 1
        if isinstance(px, tuple) and len(px) >= 3:
            if px[:3] != (0, 0, 0):
                non_black += 1
        else:
            if px != 0:
                non_black += 1
print(f"\nNon-black: {non_black}/{total} ({100*non_black/total:.1f}%)")

# Color analysis - average RGB
pixels = list(im.getdata())
if isinstance(pixels[0], tuple) and len(pixels[0]) >= 3:
    avg_r = sum(p[0] for p in pixels) // len(pixels)
    avg_g = sum(p[1] for p in pixels) // len(pixels)
    avg_b = sum(p[2] for p in pixels) // len(pixels)
    print(f"Avg RGB: ({avg_r}, {avg_g}, {avg_b})")
