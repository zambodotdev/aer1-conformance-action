#!/usr/bin/env python3
"""Download the AER-1 conformance corpus tree named by a corpus manifest.

Usage: fetch_corpus.py <manifest-url> <dest-dir>

Every file listed in the manifest (the evaluated vector files plus the
downloadable runners and license) is fetched from the manifest's base_url
and its SHA-256 is checked against the manifest before it is written. The
manifest itself is saved as index.json in the destination, which is the
layout the corpus runner (conformance.py) expects. Any hash mismatch is a
hard failure.
"""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path


def get(url):
    last = None
    for _ in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 - retry any transport error
            last = e
    raise last


def main():
    manifest_url, dest = sys.argv[1], Path(sys.argv[2])
    dest.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(get(manifest_url))
    (dest / "index.json").write_text(json.dumps(manifest, indent=2))
    base = manifest["base_url"]
    items = [(f["path"], f["sha256"]) for f in manifest["files"]]
    items += [(d["path"], d["sha256"]) for d in manifest["downloads"]]
    for path, want in items:
        raw = get(base + path)
        got = hashlib.sha256(raw).hexdigest()
        if got != want:
            print(f"HASH MISMATCH {path}: got {got}, manifest says {want}")
            return 1
        target = dest / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    print(f"Downloaded {len(items)} corpus files; all SHA-256 hashes match the manifest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
