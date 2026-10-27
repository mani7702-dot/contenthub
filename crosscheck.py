import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Cross-check 1: NASA ISS mission info for Frank Rubio
# Cross-check 2: Ysgol Cemaes school on Anglesey - badge to space project
# Cross-check 3: The ISS badge project details

urls = [
    ("nasa-rubio-iss", "https://www.nasa.gov/humans-in-space/artemis/"),
    ("rubio-wikipedia", "https://en.wikipedia.org/wiki/Frank_Rubio"),
    ("ysc-cemaes-wikipedia", "https://en.wikipedia.org/wiki/Ysgol_Cemaes"),
]

for slug, url in urls:
    try:
        p = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "25", "-A", UA, url], capture_output=True, timeout=30)
        data = p.stdout
        text = data.decode(errors='replace')
        print(f"\n=== {slug}: len={len(data)} ===")
        if len(data) > 0:
            # Check if HTML or actual content
            if "just a moment" in text.lower() or "checking your browser" in text.lower():
                print("CLOUDFLARE BLOCKED")
            else:
                # Look for key facts
                # For Rubio: ISS mission dates, return date
                # For school: Anglesey location
                clean = re.sub(r'<[^>]+>', ' ', text)
                clean = re.sub(r'\s+', ' ', clean)
                print(f"First 1000 chars: {clean[:1000]}")
        else:
            print("EMPTY")
    except Exception as e:
        print(f"\n=== {slug}: Error: {e} ===")
