import re

TITLE = "How did a stretch of Antarctic water get named after a BBC science reporter?"

# build.py logic (line 101)
slug_build = re.sub(r"[^a-z0-9]+", "-", TITLE.lower()).strip("-")[:90]
print("build.py slug:", slug_build)

# deploy.sh logic
import subprocess
deploy_slug = subprocess.run(
    ["bash", "-c", f'echo "{TITLE}" | tr "[:upper:]" "[:lower:]" | sed "s/[^a-z0-9]\\\\+/-/g; s/^-//; s/-$//" | cut -c1-90'],
    capture_output=True, text=True
).stdout.strip()
print("deploy.sh slug:", deploy_slug)
print("MATCH:", slug_build == deploy_slug)
