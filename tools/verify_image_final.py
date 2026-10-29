from PIL import Image

img_path = "assets/images/how-did-a-tiktok-video-reveal-a-whole-new-kind-of-underground-fish.jpg"
im = Image.open(img_path)
w, h = im.size

# Sample key regions to understand the image content
# Top-left corner
print(f"Image: {w}x{h}, Mode: {im.mode}")

# Check the four quadrants
quadrants = {
    "Top-Left": (0, 0, w//2, h//2),
    "Top-Right": (w//2, 0, w, h//2),
    "Bottom-Left": (0, h//2, w//2, h),
    "Bottom-Right": (w//2, h//2, w, h),
}

for name, box in quadrants.items():
    crop = im.crop(box)
    pixels = list(crop.getdata())
    avg_r = sum(p[0] for p in pixels) / len(pixels)
    avg_g = sum(p[1] for p in pixels) / len(pixels)
    avg_b = sum(p[2] for p in pixels) / len(pixels)
    # Check for dark background (common in fish-underwater images with dark bg)
    dark = sum(1 for p in pixels if p[0] < 30 and p[1] < 30 and p[2] < 30)
    bright = sum(1 for p in pixels if p[0] > 200 and p[1] > 200 and p[2] > 200)
    print(f"{name}: avg=({avg_r:.0f},{avg_g:.0f},{avg_b:.0f}), dark={dark}, bright={bright} ({len(pixels)} total)")

# Check if the image might be a Wikimedia underwater fish photo
# Let's sample the center region for a possible focal subject
center_crop = im.crop((w//2 - 200, h//2 - 200, w//2 + 200, h//2 + 200))
cpixels = list(center_crop.getdata())
avg_r = sum(p[0] for p in cpixels) / len(cpixels)
avg_g = sum(p[1] for p in cpixels) / len(cpixels)
avg_b = sum(p[2] for p in cpixels) / len(cpixels)
print(f"\nCenter: avg=({avg_r:.0f},{avg_g:.0f},{avg_b:.0f})")
# Diverse colors = likely has a fish subject
unique_colors = len(set(list(center_crop.getdata())[::50]))
print(f"Center unique colors (sampled): {unique_colors}")
