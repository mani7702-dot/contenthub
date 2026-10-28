#!/usr/bin/env python3
"""Inspect the downloaded image content."""
from PIL import Image
import os

img_path = "/home/ubuntu/contenthub/assets/images/how-did-a-dartmouth-high-school-baseball-team-stay-smiling-through-6-winless-seasons.jpg"
im = Image.open(img_path)
print(f"Size: {im.size}")
print(f"Mode: {im.mode}")
print(f"Format: {im.format}")
print(f"File size: {os.path.getsize(img_path)} bytes")

# Check corners
print(f"Top-left pixel: {im.getpixel((0,0))}")
print(f"Top-right pixel: {im.getpixel((im.width-1,0))}")
print(f"Bottom-left pixel: {im.getpixel((0,im.height-1))}")
print(f"Bottom-right pixel: {im.getpixel((im.width-1,im.height-1))}")

# Check center pixel
print(f"Center pixel: {im.getpixel((im.width//2, im.height//2))}")

# Save a small thumbnail for human review
im.thumbnail((200, 200))
im.save("/home/ubuntu/contenthub/tools/img_preview.jpg", "JPEG", quality=85)
print("Preview saved to tools/img_preview.jpg")
