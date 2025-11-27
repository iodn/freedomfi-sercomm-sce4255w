#!/usr/bin/env python3

"""
Iodn - Kaijin Lab
Generates the root SSH password and debug GUI password for the 
FreedomFi Indoor CBRS Radio (Sercomm SCE4255W) from a MAC address.
From calc_f2 algorithm.
"""

import argparse, hashlib, re, sys

KEYWORDS = {
    "ID": "Q?*ztBa3",
    "Debug": "BYEBKCSe",
    "Telnet": "O6QSBT5l",
    "Partner": "zv8t3ZjU",
    "Sc_femto": "gv9tdTj1",
    "Admin": "lw8w3djo",
    "scert": "y2QMsQ==",
}
ALPHABET36 = "kj9uzli3x5t8ah1wbgm2c0on6epd4fsy7qvr"
ALLOWED = {"debug":"Debug","telnet":"Telnet"}

def sanitize_mac(mac):
    mac = re.sub(r'[^0-9a-f]', '', mac.strip().lower())
    if len(mac) != 12 or not re.fullmatch(r'[0-9a-f]{12}', mac):
        raise ValueError("MAC must be 12 hex digits (with or without separators).")
    return mac

def map36_byte(b):
    return ALPHABET36[b % 36]

def derive_code(base, key):
    key_mapped = KEYWORDS.get(key, key if key is not None else "")
    base16 = (base or "")[:16]
    key16 = (key_mapped or "")[:16]
    d = hashlib.md5((base16 + key16).encode('latin-1', errors='ignore')).digest()
    return ''.join(map36_byte(b) for b in d)

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--mac", required=True)
    parser.add_argument("-k", dest="key", required=True)
    parser.add_argument("-h", "-?", action="store_true", dest="helpflag")
    args = parser.parse_args()
    if args.helpflag:
        sys.stderr.write("Usage: python3 calc_f2.py --mac MAC -k {Debug,Telnet}\n")
        sys.exit(1)
    norm_key = ALLOWED.get(args.key.lower())
    if not norm_key:
        sys.stderr.write("Key must be one of: Debug, Telnet\n")
        sys.exit(1)
    try:
        mac = sanitize_mac(args.mac)
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(1)
    base_id = derive_code(mac, "ID")
    out = derive_code(base_id, norm_key)
    sys.stdout.write(out)

if __name__ == "__main__":
    main()
