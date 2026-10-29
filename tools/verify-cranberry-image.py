#!/usr/bin/env python3
"""Verify the downloaded cranberry image content using PIL pixel inspection."""
from PIL import Image
import os

path = "/home/ubuntu/contenthub/assets/images/how-did-cranberry-juice-become-a-tooth-decay-fighter.jpg"
if not os.path.exists(path):
    print("Image file not found!")
    exit(1)

im = Image.open(path)
print(f"Size: {im.size}, Mode: {im.mode}")

w, h = im.size
print(f"\nCorner pixels:")
px = im.getpixel((0, 0))
print(f"  Top-left: {px}")
px = im.getpixel((w-1, 0))
print(f"  Top-right: {px}")
px = im.getpixel((0, h-1))
print(f"  Bottom-left: {px}")
px = im.getpixel((w-1, h-1))
print(f"  Bottom-right: {px}")
px = im.getpixel((w//2, h//2))
print(f"  Center: {px}")

# Grid sampling
print(f"\nGrid sampling (10x10):")
step_x, step_y = w // 10, h // 10
for y in range(0, h, step_y):
    row = []
    for x in range(0, w, step_x):
        px = im.getpixel((min(x, w-1), min(y, h-1)))
        row.append(px)
    print(f"  Y={y}: {row[:5]}...")

# Non-black pixel ratio
non_black = sum(1 for x in range(0, w, 5) for y in range(0, h, 5) if im.getpixel((min(x, w-1), min(y, h-1))) != (0, 0, 0))
total = sum(1 for _ in range(0, w, 5) for _ in range(0, h, 5))
print(f"\nNon-black: {non_black}/{total} ({100*non_black/total:.1f}%)")

# Check if image has red/pink tones (cranberries)
red_count = 0
red_total = 0
for x in range(0, w, 10):
    for y in range(0, h, 10):
        px = im.getpixel((min(x, w-1), min(y, h-1)))
        r, g, b = px[0], px[1], px[2]
        red_total += 1
        if r > 100 and g < 100 and b < 100:
            red_count += 1
print(f"Red/pink pixels: {red_count}/{red_total} ({100*red_count/red_total:.1f}%)")
