import subprocess, os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

urls = [
    ("badge-sends-to-space", "https://www.bbc.co.uk/news/articles/cq78pzl85nglo"),
    ("spaceplane", "https://www.bbc.co.uk/news/articles/cmdxwzz7x4pno"),
]

for slug, url in urls:
    p = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "25", "-A", UA, url], capture_output=True, timeout=30)
    data = p.stdout
    text = data.decode(errors='replace')
    with open(f"/home/ubuntu/contenthub/temp_{slug}.html", "w", errors='replace') as f:
        f.write(text)
    print(f"{slug}: {len(data)} bytes saved to /home/ubuntu/contenthub/temp_{slug}.html")
