#!/usr/bin/env python3
"""Compute slug for the NYC cleanup article."""
import re

title = "How Did a New Yorker Named Service Clean Up a Brooklyn Dumping Site All on His Own?"
# deploy.sh pipeline: lowercase, replace non-alphanumeric with dashes, strip, truncate to 90
deploy_slug = title.lower()
deploy_slug = re.sub(r"[^a-z0-9]+", "-", deploy_slug).strip("-")[:90]
print(f"Title: {title}")
print(f"Slug:  {deploy_slug}")
print(f"File:  content/news/{deploy_slug}.md")
