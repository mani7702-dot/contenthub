#!/usr/bin/env python3
"""Grid-based PIL pixel inspection to verify image content."""
from PIL import Image
import sys

im = Image.open(sys.argv[1]).convert("RGB")
w, h = im.size
print(f"Size: {w}x{h}, Mode: {im.mode}")

# Grid sampling
step_x, step_y = w // 10, h // 10
for y in range(0, h, step_y):
    row = [im.getpixel((x, y)) for x in range(0, w, step_x)]
    print(f"Y={y}: {row}")

# Non-black pixel ratio
non_black = sum(1 for x in range(0, w, 5) for y in range(0, h, 5) if im.getpixel((x, y)) != (0, 0, 0))
total = sum(1 for _ in range(0, w, 5) for _ in range(0, h, 5))
print(f"Non-black: {non_black}/{total} ({100 * non_black / total:.1f}%)")

# Check if it's a natural photo (warm earth tones) vs abstract
colors = im.getcolors(maxcolors=100000)
if colors:
    sorted_colors = sorted(colors, key=lambda c: c[0], reverse=True)[:5]
    print("Top 5 colors (count, (R,G,B)):")
    for count, color in sorted_colors:
        print(f"  {count}: {color}")
