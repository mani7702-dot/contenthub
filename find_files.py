import os, sys

# Find build.py
for root, dirs, files in os.walk("."):
    for f in files:
        if f == "build.py":
            path = os.path.join(root, f)
            print(f"Found: {path}")
            # Show size
            print(f"  Size: {os.path.getsize(path)} bytes")

# Also find deploy.sh
for root, dirs, files in os.walk("."):
    for f in files:
        if f == "deploy.sh":
            path = os.path.join(root, f)
            print(f"Found: {path}")
            print(f"  Size: {os.path.getsize(path)} bytes")
