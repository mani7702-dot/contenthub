#!/bin/bash
# Test the exact deploy.sh title extraction and slug computation
MD="content/news/how-did-cranberry-juice-become-a-tooth-decay-fighter.md"
TITLE=$(sed -n "s/^title: *[\\"\x27]*\\(.*\\)[\\"\x27]*$/\\1/p" "$MD" | head -1)
echo "TITLE: [$TITLE]"
SLUG=$(echo "$TITLE" | tr "[:upper:]" "[:lower:]" | sed "s/[^a-z0-9]\+/-/g; s/^-//; s/-\$//" | cut -c1-90)
echo "SLUG: [$SLUG]"
