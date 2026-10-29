#!/usr/bin/env python3
"""Verify image content with PIL — check dimensions, mode, and pixel values."""
from PIL import Image
path = "assets/images/how-did-a-lightning-strike-lead-to-a-proposal-when-she-restarted-his-heart-twice.jpg"
im = Image.open(path)
print(f"Size: {im.size}, Mode: {im.mode}")
print(f"Top-left: {im.getpixel((0, 0))}")
print(f"Center: {im.getpixel((im.width//2, im.height//2))}")
print(f"Bottom-right: {im.getpixel((im.width-1, im.height-1))}")
