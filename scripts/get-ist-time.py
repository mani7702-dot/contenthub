#!/usr/bin/env python3
"""Get current time in IST."""
import os, time
# Set timezone to IST
os.environ["TZ"] = "Asia/Kolkata"
try:
    time.tzset()
except AttributeError:
    pass  # Windows doesn't have tzset

print(time.strftime("%H:%M IST", time.localtime()))
