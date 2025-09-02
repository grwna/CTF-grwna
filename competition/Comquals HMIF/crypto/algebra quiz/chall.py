from Crypto.Util.number import getPrime, bytes_to_long as b2l

FLAG = open('flag.txt', 'rb').read()
assert len(FLAG) < 1024 // 8
pt = b2l(FLAG)

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x10001

ct = pow(pt, e, n)

leak1 = 3*p**2*q**2 + 4*p*q**2 - 3*p*q
leak2 = 3*p*q + 2*q

print(f'n = {n}')
print(f'e = {e}')
print(f'ct = {ct}')
print(f'l1 = {leak1}')
print(f'l2 = {leak2}')
