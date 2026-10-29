#!/usr/bin/env python3
"""Deeper image inspection — sample pixels across the image grid."""
from PIL import Image

path = "assets/images/how-did-autistic-children-process-faces-differently-than-scientists-thought.jpg"
im = Image.open(path)
w, h = im.size
print(f"Size: {w}x{h}")

# Sample a grid of pixels
step_x = w // 10
step_y = h // 10
for y in range(0, h, step_y):
    row = []
    for x in range(0, w, step_x):
        px = im.getpixel((x, y))
        row.append(px)
    print(f"Y={y}: {row}")

# Count how many pixels are non-black
non_black = 0
total = 0
for x in range(0, w, 5):
    for y in range(0, h, 5):
        px = im.getpixel((x, y))
        total += 1
        if px != (0, 0, 0):
            non_black += 1
print(f"\nNon-black sample pixels: {non_black}/{total} ({100*non_black/total:.1f}%)")

# Sample some brighter pixels
bright = []
for x in range(0, w, 10):
    for y in range(0, h, 10):
        px = im.getpixel((x, y))
        if px != (0, 0, 0):
            bright.append(px)
if bright:
    print(f"Sample bright pixels: {bright[:20]}")
