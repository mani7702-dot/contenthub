#!/usr/bin/env python3
"""Verify image content."""
from PIL import Image
import os

src = "assets/images/how-did-a-stranger-pay-420-for-a-group-s-lunch-in-south-korea.jpg"
im = Image.open(src)
print(f"Size: {im.size}, Mode: {im.mode}")
print(f"Top-left: {im.getpixel((0, 0))}")
print(f"Center: {im.getpixel((im.width//2, im.height//2))}")
print(f"Bottom-right: {im.getpixel((im.width-1, im.height-1))}")
print(f"Top-right: {im.getpixel((im.width-1, 0))}")
print(f"Bottom-left: {im.getpixel((0, im.height-1))}")

# Resize for vision
dst = "/tmp/verify2.jpg"
new_w = 400
new_h = round(im.height * 400 / im.width)
im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
im_resized.save(dst, "JPEG", quality=85)
print(f"Resized to {new_w}x{new_h}, saved to {dst}")
