#!/usr/bin/env python3

import os
import base64
import argparse
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, unquote

# === Mimetype fallback map ===
MIMETYPE_MAP = {
    "HTML": ".html",
    "script": ".js",
    "style": ".css",
    "image": ".png",  # Customize as needed
    "json": ".json",
    "xml": ".xml",
    "text": ".txt",
}

def decode_and_save(item, base_dir):
    url = item.findtext("url")
    mimetype = item.findtext("mimetype")
    response = item.find("response")

    if response is None or response.attrib.get("base64") != "true":
        return None

    try:
        encoded = response.text.strip()
        decoded = base64.b64decode(encoded)

        # Strip HTTP headers if present
        split_at = b"\r\n\r\n" if b"\r\n\r\n" in decoded else b"\n\n"
        body = decoded.split(split_at, 1)[-1]

        parsed_url = urlparse(url)
        path = unquote(parsed_url.path.lstrip("/"))
        ext = os.path.splitext(path)[1]

        if not ext:
            ext = MIMETYPE_MAP.get(mimetype, ".bin")

        if not path or path.endswith("/"):
            path = os.path.join(path, f"index{ext}")
        elif not os.path.splitext(path)[1]:
            path += ext

        full_path = os.path.join(base_dir, parsed_url.netloc, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "wb") as f:
            f.write(body)

        return full_path

    except Exception as e:
        print(f"[!] Failed to process URL '{url}': {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Extract base64-encoded response bodies from a Burp Suite XML export.",
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the Burp XML file.")
    parser.add_argument("-o", "--output", default="extracted_files", help="Output directory for extracted files.")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[!] Input file does not exist: {args.input}")
        return

    os.makedirs(args.output, exist_ok=True)
    tree = ET.parse(args.input)
    root = tree.getroot()

    saved = 0
    for item in root.findall(".//item"):
        result = decode_and_save(item, args.output)
        if result:
            print(f"[✓] Saved: {result}")
            saved += 1

    print(f"\n✅ Done: {saved} file(s) saved in '{args.output}/'")

if __name__ == "__main__":
    main()
