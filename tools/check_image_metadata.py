#!/usr/bin/env python3
"""Try to read EXIF and more detailed image info."""
from PIL import Image
import sys

img_path = sys.argv[1] if len(sys.argv) > 1 else "assets/images/how-do-t-cells-feel-their-surroundings-to-help-us-stay-healthy.jpg"

im = Image.open(img_path)
print(f"Format: {im.format}")
print(f"Size: {im.size}")
print(f"Mode: {im.mode}")

# Check for EXIF data
if im._getexif():
    print(f"EXIF: {im._getexif()}")
else:
    print("No EXIF data")

# Save a downscaled version and also check histogram for color distribution
hist = im.histogram()
# RGB histogram - sum channels to see overall brightness distribution
# Check if it's mostly dark (microscopy) or natural colors
r_hist = hist[:256]
g_hist = hist[256:512]
b_hist = hist[512:768]

# Count pixels in different brightness ranges
total = sum(r_hist)
dark_r = sum(r_hist[:50]) / total * 100
mid_r = sum(r_hist[50:200]) / total * 100
bright_r = sum(r_hist[200:]) / total * 100
print(f"\nRed channel: {dark_r:.1f}% dark, {mid_r:.1f}% mid, {bright_r:.1f}% bright")
print(f"Image appears to be: {'microscopy/illustration on dark bg' if dark_r > 30 else 'natural photo'}")

# Check color saturation
r_avg = sum(i * r_hist[i] for i in range(256)) / total
g_avg = sum(i * g_hist[i] for i in range(256)) / total
b_avg = sum(i * b_hist[i] for i in range(256)) / total
print(f"Average RGB: ({r_avg:.0f}, {g_avg:.0f}, {b_avg:.0f})")
