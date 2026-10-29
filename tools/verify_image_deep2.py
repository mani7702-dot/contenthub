from PIL import Image
import json

img_path = "assets/images/how-did-a-tiktok-video-reveal-a-whole-new-kind-of-underground-fish.jpg"
im = Image.open(img_path)
w, h = im.size

# Convert to flat pixel list properly
pixels = list(im.getdata())

print(f"Image size: {w}x{h}")
print(f"Total pixels: {len(pixels)}")

# Check center crop (200x200 from center) for the main subject
cx, cy = w // 2, h // 2
box = (cx-100, cy-100, cx+100, cy+100)
center = im.crop(box)
center_pixels = list(center.getdata())

# Count bright vs dark in center
bright = sum(1 for r,g,b in center_pixels if r > 128 and g > 128 and b > 128)
dark = sum(1 for r,g,b in center_pixels if r < 64 and g < 64 and b < 64)
mid = len(center_pixels) - bright - dark

print(f"\nCenter 200x200 crop:")
print(f"  Bright pixels: {bright}")
print(f"  Dark pixels: {dark}")
print(f"  Mid pixels: {mid}")
print(f"  Bright ratio: {bright/len(center_pixels)*100:.1f}%")

# Sample some center pixels
print(f"\nSample center pixels:")
for i in range(0, min(20, len(center_pixels)), 2):
    print(f"  {center_pixels[i]}")

# Check if there's a clear horizontal structure (fish = elongated)
# Check the horizontal pixel variance in the middle row
mid_row = h // 2
row_pixels = [im.getpixel((x, mid_row)) for x in range(0, w, 20)]
print(f"\nMiddle row variance (every 20px):")
prev = row_pixels[0]
transitions = 0
for p in row_pixels:
    diff = sum(abs(p[i]-prev[i]) for i in range(3))
    if diff > 30:
        transitions += 1
    prev = p
print(f"  Color transitions in middle row: {transitions}")

# Overall brightness
avg_r = sum(p[0] for p in pixels) / len(pixels)
avg_g = sum(p[1] for p in pixels) / len(pixels)
avg_b = sum(p[2] for p in pixels) / len(pixels)
print(f"\nOverall average: R={avg_r:.0f}, G={avg_g:.0f}, B={avg_b:.0f}")
if avg_b > avg_r and avg_b > avg_g:
    print("  Blue-dominant = likely underwater/aquarium scene")
elif avg_r > avg_g and avg_r > avg_b:
    print("  Red-dominant = likely warm/light surface scene")
else:
    print("  Mixed = likely natural scene")
