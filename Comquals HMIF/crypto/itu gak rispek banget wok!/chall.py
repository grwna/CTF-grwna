from Crypto.Util.number import getPrime, bytes_to_long as b2l
import random

FLAG = open('flag.txt', 'rb').read()

primes = [getPrime(512) for _ in range(8)]

p = primes[0]
q = primes[1]
n = p * q
e = 0x10001

pt = b2l(FLAG)
ct = pow(pt, e, n)

mods = [n]
for prime in primes[2:]:
    mods.append(p * prime + random.randrange(2**15, 2**16))

print(f'n = {n}')
print(f'e = {e}')
print(f'ct = {ct}')
print(f'mods = {mods}')
