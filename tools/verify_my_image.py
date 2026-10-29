#!/usr/bin/env python3
"""Verify the fetched image content is relevant to the article topic."""
from PIL import Image
import os

path = "assets/images/how-did-autistic-children-process-faces-differently-than-scientists-thought.jpg"
im = Image.open(path)
print(f"Size: {im.size}, Mode: {im.mode}")

# Sample pixels at various locations
w, h = im.size
corners = [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1)]
center = (w//2, h//2)
print(f"Top-left: {im.getpixel((0, 0))}")
print(f"Top-right: {im.getpixel((w-1, 0))}")
print(f"Bottom-left: {im.getpixel((0, h-1))}")
print(f"Bottom-right: {im.getpixel((w-1, h-1))}")
print(f"Center: {im.getpixel(center)}")

# Create a small preview for vision_analyze
preview = im.resize((400, round(h * 400 / w)), Image.LANCZOS)
preview.save("/tmp/verify_img.jpg", "JPEG", quality=85)
print("Preview saved to /tmp/verify_img.jpg")
