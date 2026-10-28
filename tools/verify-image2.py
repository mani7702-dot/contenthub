#!/usr/bin/env python3
"""Resize image to smaller size for vision analysis."""
import sys
sys.path.insert(0, "/home/ubuntu/.local/lib/python3.14/site-packages")
from PIL import Image

path = "/home/ubuntu/contenthub/assets/images/how-did-knitted-traffic-cops-help-slow-down-speeding-drivers-in-a-quiet-english-village.jpg"
im = Image.open(path)
print(f"Original size: {im.size}")

# Resize to a smaller size for vision analysis
small = im.resize((400, 300), Image.Resampling.LANCZOS)
small_path = "/home/ubuntu/contenthub/assets/images/verify_small.jpg"
small.save(small_path, "JPEG", quality=85)
print(f"Saved small version to: {small_path}")

# Also print pixel statistics
import os
print(f"Small file size: {os.path.getsize(small_path)} bytes")
