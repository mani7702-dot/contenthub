#!/usr/bin/env python3
"""Detailed image analysis - check center region for content relevance."""
from PIL import Image

img_path = "assets/images/how-did-a-tiny-laser-beam-make-computer-memory-1000-times-faster.jpg"
im = Image.open(img_path)
w, h = im.size
im_rgb = im.convert("RGB")

print(f"Full image: {w}x{h}")

# Check center region
cx1, cx2 = w // 5, 4 * w // 5
cy1, cy2 = h // 5, 4 * h // 5
print(f"Center region: ({cx1},{cy1}) to ({cx2},{cy2})")

# Sample center region
print("\n=== Center region grid ===")
step_x = (cx2 - cx1) // 15
step_y = (cy2 - cy1) // 15
colorful = 0
total = 0
pixels_list = []

for y in range(cy1, cy2, step_y):
    row = []
    for x in range(cx1, cx2, step_x):
        p = im_rgb.getpixel((x, y))
        row.append(p)
        pixels_list.append(p)
        total += 1
        r, g, b = p
        if max(r, g, b) - min(r, g, b) > 30:
            colorful += 1
    if len(row) >= 5:
        print(f"  Y={y}: {row[:5]}...")

print(f"\nColorful pixels in center: {colorful}/{total} ({100*colorful/total:.1f}%)")

# Check overall color distribution
gray_count = 0
for y in range(0, h, 10):
    for x in range(0, w, 10):
        p = im_rgb.getpixel((x, y))
        r, g, b = p
        if abs(r - g) < 10 and abs(g - b) < 10 and abs(r - b) < 10:
            gray_count += 1

total_sampled = len(range(0, h, 10)) * len(range(0, w, 10))
print(f"Grayscale-like pixels: {gray_count}/{total_sampled} ({100*gray_count/total_sampled:.1f}%)")

# Print some center-row samples
print("\n=== Sample pixels from center rows ===")
center_y = h // 2
for x in range(0, w, w // 15):
    p = im_rgb.getpixel((x, center_y))
    print(f"  ({x}, {center_y}): {p}")
