from grwnapy.crypto.math import *
from pwn import *

# Using the multiplicative property of RSA, we can manipulate the oracle
# to decrypt a reversible manipulation of the flag's ciphertext
# By multiplying CT with a known integer mod n, the oracle allows decryption
# which results with modified pt that follows mpt c= pt * s mod n.

# This is because mpt^e = pt^e * s^e mod n
# when teh oracle decrypts, all powers of e becomes 1
# this allows us to get the plaintext for the flag

con = remote("mercury.picoctf.net", 60368)

s = 2 # arbitrary scale

con.recvuntil(b"n: ")
n = con.recvuntil(b"e: ")[:-3].strip()
e = con.recvuntil(b"ciphertext: ")[:-12].strip()
ct = con.recvline().strip() 
mct = (int(ct) * pow(s,int(e), int(n))) % int(n)

con.sendlineafter(b"decrypt: ", str(mct).encode())
con.recvuntil(b"go: ")

mpt = con.recvline().strip()
flag = int(mpt) // s
print(long_to_bytes(flag))