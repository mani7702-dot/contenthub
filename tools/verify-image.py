#!/usr/bin/env python3
"""Verify the downloaded image is relevant to the article topic."""
from PIL import Image
import os

path = "assets/images/how-do-our-immune-cells-feel-the-world-around-them-with-a-hidden-sense-of-touch.jpg"
im = Image.open(path)
print(f"Original: {im.size}, mode: {im.mode}")

# Resize for vision verification
small = im.resize((400, 300), Image.Resampling.LANCZOS)
small.save("/tmp/verify_immune.jpg", "JPEG", quality=85)
print(f"Saved resized to /tmp/verify_immune.jpg")
print(f"File size: {os.path.getsize(path)} bytes")
