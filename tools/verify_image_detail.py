from PIL import Image
import numpy as np

im = Image.open("assets/images/who-was-panther-pat-the-first-woman-to-play-pro-football.jpg")
w, h = im.size
print(f"Size: {w}x{h}, Mode: {im.mode}")

arr = np.array(im)
print(f"Channel means: R={arr[:,:,0].mean():.0f}, G={arr[:,:,1].mean():.0f}, B={arr[:,:,2].mean():.0f}")
print(f"Channel stds:  R={arr[:,:,0].std():.0f}, G={arr[:,:,1].std():.0f}, B={arr[:,:,2].std():.0f}")

# Sample grid for color distribution
step_x, step_y = w // 8, h // 8
for y in range(0, h, step_y):
    row = [im.getpixel((x, y)) for x in range(0, w, step_x)]
    print(f"Y={y:4d}: {row}")

# Check for skin tones (typical RGB 180-240 range in at least one channel)
skin_pixels = 0
for x in range(0, w, 5):
    for y in range(0, h, 5):
        r, g, b = im.getpixel((x, y))
        if r > 150 and g > 100 and b < 200 and r > g:
            skin_pixels += 1
print(f"Potential skin-tone pixels: {skin_pixels}")

# Histogram of brightness
brightness = (arr[:,:,0].astype(int) + arr[:,:,1].astype(int) + arr[:,:,2].astype(int)) // 3
print(f"Brightness range: {brightness.min()} - {brightness.max()}, median: {np.median(brightness):.0f}")
