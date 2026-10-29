#!/usr/bin/env python3
import re
title = "How Did a Texas Barber Return $128,000 He Found at an ATM to Its Owner?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(f"Title: {title}")
print(f"Slug:  {slug}")
