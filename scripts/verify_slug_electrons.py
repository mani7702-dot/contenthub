import re
title = "How Did Two Electrons Working Together Break Physics' X-Ray Energy Limit?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(f"Deploy.sh derived slug: {slug}")
print(f"Frontmatter slug key:  how-did-two-electrons-working-together-break-physics-x-ray-energy-limit")
print(f"Match: {slug == 'how-did-two-electrons-working-together-break-physics-x-ray-energy-limit'}")
