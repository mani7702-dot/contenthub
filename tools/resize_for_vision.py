#!/usr/bin/env python3
"""Resize image for vision_analyze."""
from PIL import Image
im = Image.open("assets/images/how-did-a-new-yorker-named-service-clean-up-a-brooklyn-dumping-site-all-on-his-own.jpg")
im.resize((400, 300), Image.Resampling.LANCZOS).save("/tmp/verify_nyc_cleanup.jpg", "JPEG", quality=85)
print("Resized and saved to /tmp/verify_nyc_cleanup.jpg")
