import subprocess, os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
os.makedirs("/tmp/raw", exist_ok=True)

urls = [
    ("badge-sends-to-space", "https://www.bbc.co.uk/news/articles/cq78pzl85nglo"),
    ("spaceplane", "https://www.bbc.co.uk/news/articles/cmdxwzz7x4pno"),
    ("musk-merger", "https://www.bbc.co.uk/news/articles/cr93z1e87e0do"),
]

for slug, url in urls:
    try:
        p = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "25", "-A", UA, url], capture_output=True, timeout=30)
        data = p.stdout
        print(f"\n=== {slug}: len={len(data)}, status={p.returncode} ===")
        with open(f"/tmp/raw/{slug}.html", "wb") as f:
            f.write(data)
    except Exception as e:
        print(f"\n=== {slug}: Error: {e} ===")
