from PIL import Image

path = "assets/images/how-did-two-electrons-working-together-break-physics-x-ray-energy-limit.jpg"
im = Image.open(path)
print(f"Size: {im.size}, Mode: {im.mode}")

# Grid-based pixel inspection
w, h = im.size
step_x, step_y = w // 10, h // 10
print("\n=== Grid sampling (every 10th pixel) ===")
for y in range(0, h, step_y):
    row = []
    for x in range(0, w, step_x):
        row.append(im.getpixel((x, y)))
    print(f"Y={y:4d}: {row}")

# Non-black pixel ratio
non_black = 0
total = 0
for x in range(0, w, 5):
    for y in range(0, h, 5):
        total += 1
        p = im.getpixel((x, y))
        if p != (0, 0, 0):
            non_black += 1
print(f"\nNon-black: {non_black}/{total} ({100*non_black/total:.1f}%)")

# Check if it looks like a physics/astronomy diagram (bright spots on dark bg)
# vs a natural photo
print(f"\nTop-left corner: {im.getpixel((0, 0))}")
print(f"Center: {im.getpixel((w//2, h//2))}")
print(f"Bottom-right: {im.getpixel((w-5, h-5))}")
