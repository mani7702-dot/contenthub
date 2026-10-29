from PIL import Image

img_path = "assets/images/how-did-a-tiktok-video-reveal-a-whole-new-kind-of-underground-fish.jpg"
im = Image.open(img_path)
w, h = im.size
print(f"Size: {w}x{h}, Mode: {im.mode}")

# Grid sampling
step_x, step_y = w // 10, h // 10
print("\nGrid samples (sampled across image):")
for y in range(0, h, step_y):
    row = [im.getpixel((x, y)) for x in range(0, w, step_x)]
    print(f"Y={y}: {row}")

# Non-black pixel ratio
non_black = sum(1 for x in range(0, w, 5) for y in range(0, h, 5) if im.getpixel((x, y)) != (0, 0, 0))
total = sum(1 for _ in range(0, w, 5) for _ in range(0, h, 5))
print(f"\nNon-black: {non_black}/{total} ({100*non_black/total:.1f}%)")
