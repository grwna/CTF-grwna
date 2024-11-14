from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

import os
import random
import hashlib

FLAG = open('flag.txt', 'rb').read()

p = 79795630955469521254453529874714715038350278079750097930779052971965384685581
r = random.randrange(2^68, 2^69)
print(r)

E = EllipticCurve(GF(p), [1, 3])

P = E.gen(0)
Q = P * r

key = hashlib.sha256(str(r).encode()).digest()[:16]
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)

ct = cipher.encrypt(pad(FLAG, 16))

print(f'P = {P}')
print(f'Q = {Q}')
print(f'ct = {ct}')
print(f'iv = {iv}')