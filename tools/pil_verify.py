from PIL import Image
import os

img_path = "assets/images/how-did-an-ancient-eclipse-show-earth-spun-faster-2-700-years-ago.jpg"
im = Image.open(img_path)
print(f"Size: {im.size}, Mode: {im.mode}, Format: {im.format}")

w, h = im.size
# Sample pixels at corners, center, and a grid
sample_points = [
    (0, 0), (w-1, 0), (0, h-1), (w-1, h-1),
    (w//4, h//4), (3*w//4, h//4), (w//4, 3*h//4), (3*w//4, 3*h//4),
    (w//2, h//2),
]
print("--- Pixel samples (R,G,B) ---")
for (x, y) in sample_points:
    px = im.getpixel((x, y))
    print(f"  ({x},{y}): {px}")

# Compute average color of a small center box (likely the bright solar disk in an eclipse photo)
cx, cy = w//2, h//2
box = im.crop((cx-30, cy-30, cx+30, cy+30))
pixels = list(box.getdata())
avg = tuple(sum(c)//len(pixels) for c in zip(*pixels))
print(f"--- Center 60x60 avg: {avg} ---")

# Check brightness distribution in center box
bright = sum(1 for p in pixels if sum(p)/3 > 200)
dark = sum(1 for p in pixels if sum(p)/3 < 60)
print(f"Center bright pixels (>200): {bright}/{len(pixels)}, dark pixels (<60): {dark}/{len(pixels)}")

# Save a small version for potential vision retry
small = im.resize((400, round(h*400//w)), Image.Resampling.LANCZOS)
small.save("/tmp/verify_eclipse.jpg", "JPEG", quality=85)
print("--- Saved /tmp/verify_eclipse.jpg (400px) for vision retry ---")
