#!/usr/bin/env python3
"""Resize image for vision_analyze and inspect pixel content."""
from PIL import Image
import sys

path = "assets/images/how-did-a-texas-barber-return-128-000-he-found-at-an-atm-to-its-owner.jpg"
im = Image.open(path)
print(f"Size: {im.size}, Mode: {im.mode}")
print(f"Top-left: {im.getpixel((0, 0))}")
print(f"Center: {im.getpixel((im.width//2, im.height//2))}")
print(f"Top-right: {im.getpixel((im.width-1, 0))}")
print(f"Bottom-left: {im.getpixel((0, im.height-1))}")
print(f"Bottom-right: {im.getpixel((im.width-1, im.height-1))}")

# Resize for vision_analyze (max 400px width)
im_small = im.resize((400, round(im.height * 400 / im.width)), Image.Resampling.LANCZOS)
im_small.save("/tmp/verify_atm.jpg", "JPEG", quality=85)
print("Saved resized version to /tmp/verify_atm.jpg")
