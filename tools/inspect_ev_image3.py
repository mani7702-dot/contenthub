#!/usr/bin/env python3
"""Detailed PIL inspection of the EV battery image."""
from PIL import Image

path = "assets/images/how-did-scientists-make-electric-car-batteries-smaller-and-longer-lasting.jpg"
im = Image.open(path)
print(f"Size: {im.size}, Mode: {im.mode}, Format: {im.format}")

# Sample a grid of pixels to understand the image
w, h = im.size
print(f"\nImage dimensions: {w}x{h}")

# Sample corners, edges, and center
positions = {
    "top-left": (0, 0),
    "top-center": (w//2, 0),
    "top-right": (w-1, 0),
    "center-left": (0, h//2),
    "center": (w//2, h//2),
    "center-right": (w-1, h//2),
    "bottom-left": (0, h-1),
    "bottom-center": (w//2, h-1),
    "bottom-right": (w-1, h-1),
}
for name, (x, y) in positions.items():
    print(f"  {name} ({x},{y}): {im.getpixel((x, y))}")

# Check if image is mostly bright (suggests white background + dark object)
# or mostly dark (suggests dark object against light background)
pixels = list(im.getdata())
total = len(pixels)
bright_count = sum(1 for r,g,b in pixels if r > 200 and g > 200 and b > 200)
dark_count = sum(1 for r,g,b in pixels if r < 80 and g < 80 and b < 80)
print(f"\nBright pixels (>200): {bright_count} ({100*bright_count/total:.1f}%)")
print(f"Dark pixels (<80): {dark_count} ({100*dark_count/total:.1f}%)")
print(f"Mid-range pixels: {total - bright_count - dark_count} ({100*(total-bright_count-dark_count)/total:.1f}%)")
