#!/usr/bin/env python3
"""Regenerate the encryption keys in index.html for new passwords.

Usage: python3 scripts/rotate_passwords.py NEW_CLUB_PASSWORD NEW_FINANCE_PASSWORD
Requires: pip install cryptography

Download a backup from the site BEFORE running this. Data encrypted under the
old passwords cannot be read afterwards, so after deploying, unlock with the new
passwords and re-enter or re-import the data. Also change the Firebase finance
user's password to the new finance password.
"""
import base64, json, os, re, sys
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

if len(sys.argv) != 3:
    sys.exit(__doc__)
club_pw, fin_pw = sys.argv[1], sys.argv[2]
ITER = 250000
b64 = lambda x: base64.b64encode(x).decode()
key = lambda pw, salt: PBKDF2HMAC(hashes.SHA256(), 32, salt, ITER).derive(pw.encode())
def enc(k, data):
    iv = os.urandom(12)
    return {"iv": b64(iv), "ct": b64(AESGCM(k).encrypt(iv, data, None))}

ms, fs = os.urandom(16), os.urandom(16)
priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pkcs8 = priv.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
spki = priv.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
cfg = {"iter": ITER, "memberSalt": b64(ms), "finSalt": b64(fs),
       "memberCheck": enc(key(club_pw, ms), b"megm-ok"),
       "pub": b64(spki), "privWrapped": enc(key(fin_pw, fs), pkcs8)}

path = Path(__file__).resolve().parent.parent / "index.html"
html = path.read_text(encoding="utf-8")
new, n = re.subn(r"^const CFG = \{.*\};$", "const CFG = " + json.dumps(cfg) + ";", html, count=1, flags=re.M)
if n != 1:
    sys.exit("Couldn't find the 'const CFG = {...};' line in index.html")
path.write_text(new, encoding="utf-8")
print("index.html updated with new keys. Remember to change the Firebase finance user's password.")
