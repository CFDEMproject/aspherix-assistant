#!/usr/bin/env python3
"""Fetch and decompress an Aspherix docs section's Sphinx object inventory.

Usage:
    scripts/doc_index.py [--product solver|calibration] [filter]

With no filter, prints the full inventory (name domain:role priority uri displayname).
With a filter, prints only lines whose name or displayname contains it (case-insensitive).
--product selects the docs section (default: solver).
"""
import sys
import urllib.request
import zlib

URL = "https://doc.aspherix-dem.com/{product}/objects.inv"


def fetch_inventory(url):
    with urllib.request.urlopen(url) as resp:
        data = resp.read()
    # Sphinx objects.inv: 4 header lines, then zlib-compressed body.
    body = data.split(b"\n", 4)[4]
    return zlib.decompress(body).decode()


def main():
    args = sys.argv[1:]
    product = "solver"
    if args[:1] == ["--product"]:
        if len(args) < 2:
            sys.exit("usage: doc_index.py [--product solver|calibration] [filter]")
        product, args = args[1], args[2:]
    keyword = args[0].lower() if args else None
    text = fetch_inventory(URL.format(product=product))
    for line in text.splitlines():
        if keyword is None or keyword in line.lower():
            print(line)


if __name__ == "__main__":
    main()
