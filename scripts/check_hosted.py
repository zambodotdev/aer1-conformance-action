#!/usr/bin/env python3
"""Check a hosted AER-1 verify response.

Usage: check_hosted.py <verify-response.json> <receipt-id>

Fails unless the response is for the requested receipt id and its
verification_status is "verified".
"""
import json
import sys


def main():
    path, rid = sys.argv[1], sys.argv[2]
    doc = json.load(open(path))
    if doc.get("id") != rid:
        print(f"hosted verify returned id {doc.get('id')!r}, expected {rid!r}")
        return 1
    status = doc.get("verification_status")
    if status != "verified":
        print(f"hosted verification_status is {status!r}, expected 'verified'")
        return 1
    print(f"hosted verification_status: verified ({rid})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
