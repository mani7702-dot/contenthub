from PIL import Image

img_path = "assets/images/how-did-a-tiktok-video-reveal-a-whole-new-kind-of-underground-fish.jpg"
im = Image.open(img_path)
w, h = im.size

# Sample center region heavily
print(f"Image: {w}x{h}")
cx, cy = w // 2, h // 2
print(f"\nCenter region {cx-50},{cy-50} to {cx+50},{cy+50}:")
center_samples = []
for y in range(cy-50, cy+51, 10):
    row = [im.getpixel((x, y)) for x in range(cx-50, cx+51, 10)]
    center_samples.append(row)

# Check the caption that fetch-images.py would have set
# The image was "Photo: RatioTile / cc by-sa 4.0 / Wikimedia Commons"
# This is likely a Wikimedia Commons image - let's verify color distribution is natural

# Check color variance - natural photos have high variance
import colorsys
all_pixels = list(im.getdata())
# Sample every 50th pixel
sampled = all_pixels[::2000]
hues = []
for r, g, b in sampled:
    if (r, g, b) != (0, 0, 0):
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        hues.append(h)

# Count hue distribution
hue_buckets = {}
for h_val in hues:
    bucket = int(h_val * 12)  # 12 buckets for hue wheel
    hue_buckets[bucket] = hue_buckets.get(bucket, 0) + 1

print(f"\nHue distribution (12 buckets, 0=red, 3=green, 6=blue):")
for b in sorted(hue_buckets.keys()):
    print(f"  Bucket {b}: {hue_buckets[b]} pixels")

print(f"\nColor diversity: {len(set(sampled[:200]))} unique colors sampled")
print("If diverse blues + grays = likely underwater/natural photo")
