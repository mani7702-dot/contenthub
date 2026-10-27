import subprocess, sys, os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Try BBC Science & Environment RSS (usually works with curl)
urls = [
    ("BBC Science & Env", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
    ("NPR Space", "https://www.npr.org/rss/rss.php?f=1016"),
    ("NASA Image of the Day", "https://www.nasa.gov/rss/image-of-the-day/rss.jpg"),
]

os.makedirs("/tmp/raw", exist_ok=True)

for label, url in urls:
    try:
        p = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "25", "-A", UA, url], capture_output=True, timeout=30)
        data = p.stdout
        if len(data) == 0:
            print(f"{label}: EMPTY RESPONSE")
            continue
        text = data.decode(errors='replace')[:200]
        print(f"{label}: len={len(data)}, first200={text[:200]}")
        # Save for parsing
        with open(f"/tmp/raw/{label.replace(' ', '_').lower()}.html", "wb") as f:
            f.write(data)
    except subprocess.TimeoutExpired:
        print(f"{label}: TIMEOUT")
    except Exception as e:
        print(f"{label}: Error: {e}")
