#!/usr/bin/env python3
"""Verify the gut microbiome image content via PIL pixel inspection."""
from PIL import Image
im = Image.open("assets/images/how-did-the-bacteria-in-your-gut-reveal-how-fast-you-re-aging.jpg")
w, h = im.size
print(f"Size: {im.size}, Mode: {im.mode}")
print(f"Top-left: {im.getpixel((0, 0))}, Center: {im.getpixel((im.width//2, im.height//2))}")

# Grid sampling
step_x, step_y = w // 10, h // 10
print("\nGrid sampling (Y=row, X=col pixel values):")
for y in range(0, h, step_y):
    row = [im.getpixel((x, y)) for x in range(0, w, step_x)]
    print(f"  Y={y}: {row[:5]}...")

# Non-black pixel ratio
non_black = sum(1 for x in range(0, w, 5) for y in range(0, h, 5) if im.getpixel((x, y)) != (0, 0, 0))
total = sum(1 for _ in range(0, w, 5) for _ in range(0, h, 5))
print(f"\nNon-black: {non_black}/{total} ({100*non_black/total:.1f}%)")

# Color distribution
colors = im.getcolors(maxcolors=1000000)
if colors:
    top_colors = sorted(colors, key=lambda x: x[0], reverse=True)[:5]
    print(f"\nTop 5 colors (count, RGB):")
    for count, rgb in top_colors:
        print(f"  {count}: {rgb}")
