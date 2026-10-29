#!/usr/bin/env python3
"""Extract the actual URL from a Bing News RSS redirect link."""
import urllib.parse

urls = [
    "http://www.bing.com/news/apiclick.aspx?ref=FexRss&aid=&tid=6ae3921ce2654d02bfebb7868b36899f&url=https%3a%2f%2fwww.newsbytesapp.com%2fnews%2fscience%2f",
    "http://www.bing.com/news/apiclick.aspx?ref=FexRss&aid=&tid=6ae3921ce2654d02bfebb7868b36899f&url=https%3a%2f%2fphys.org%2fnews%2f2026-10-excess-oxygen-",
    "http://www.bing.com/news/apiclick.aspx?ref=FexRss&aid=&tid=6ae3921ce2654d02bfebb7868b36899f&url=https%3a%2f%2fscitechdaily.com%2fscientists-discover-a",
]
for u in urls:
    parsed = urllib.parse.urlparse(u)
    qs = urllib.parse.parse_qs(parsed.query)
    actual = qs.get("url", [u])[0]
    actual = urllib.parse.unquote(actual)
    print(actual)
