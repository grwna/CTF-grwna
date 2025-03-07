from pwn import *

con = remote("mercury.picoctf.net", 64260 )
con.recvuntil(b"flag!\n")
enc_flag = con.recvline()[:-1].decode()

len_flag = len(enc_flag) //2

payload = cyclic(50000-len_flag)
con.recvuntil(b"encrypt?")
con.sendline(payload)
con.recvuntil(b"Here ya go!\n")
con.recvline()

payload = cyclic(len_flag)
con.recvuntil(b"encrypt?")
con.sendline(payload)
con.recvuntil(b"Here ya go!\n")
enc_pyld = con.recvuntil(b"\n")[:-1].decode()
print(enc_pyld)

key = xor(payload,bytes.fromhex(enc_pyld))
flag = xor(key,bytes.fromhex(enc_flag))
print(flag.decode())
# 3a16944dad432717ccc3945d3d96421a

# The flag has to be wrapped with picoCTF{} i genuinely seriously hate
# these kinds of challenges because how much would it take to just 
# put picoCTF to the obtained flag?



