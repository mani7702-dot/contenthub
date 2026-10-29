#!/usr/bin/env python3
import re
title = "How Did Five Tiny Cheetah Cubs Make the Camera Their Playground?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(slug)
