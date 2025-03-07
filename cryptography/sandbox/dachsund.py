from pwn import *
from sage.all import *
from grwnapy.crypto.rsa import get_convergences

con = remote("mercury.picoctf.net",37455)
context.log_level = "debug"
con.recvuntil(b"e: ")
e = con.recvuntil("n: ")[:-3].strip()
n = con.recvuntil("c: ")[:-3].strip()
c = con.recvline().strip()
print(e)
print(n)
print(c)