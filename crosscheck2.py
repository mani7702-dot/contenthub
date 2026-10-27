import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Use Wikipedia API for clean content
urls = [
    ("rubio-wikipedia-api", "https://en.wikipedia.org/w/api.php?action=query&format=json&titles=Francisco_Rubio_(astronaut)&prop=extracts&explaintext=1&redirects=1"),
    ("ysc-cemaes-api", "https://en.wikipedia.org/w/api.php?action=query&format=json&titles=Ysgol_Cemaes&prop=extracts&explaintext=1&redirects=1"),
    ("iss-api", "https://en.wikipedia.org/w/api.php?action=query&format=json&titles=International_Space_Station&prop=extracts&explaintext=1&redirects=1&exintro=1"),
]

for slug, url in urls:
    try:
        p = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "25", "-A", UA, url], capture_output=True, timeout=30)
        data = p.stdout
        text = data.decode(errors='replace')
        print(f"\n=== {slug}: len={len(data)} ===")
        if len(data) > 0:
            # Clean up JSON
            try:
                import json
                result = json.loads(text)
                pages = result.get("query", {}).get("pages", {})
                for page_id, page in pages.items():
                    title = page.get("title", "Unknown")
                    extract = page.get("extract", "")
                    if not extract:
                        # Try to get more
                        extract = page.get("extract", "No extract available")
                    print(f"TITLE: {title}")
                    print(f"EXTRACT: {extract[:2000]}")
            except json.JSONDecodeError:
                print(f"JSON parse failed: {text[:500]}")
        else:
            print("EMPTY")
    except Exception as e:
        print(f"\n=== {slug}: Error: {e} ===")
