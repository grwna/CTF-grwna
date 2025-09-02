from pwn import *
from grwnapy.crypto.math import *
import subprocess

con = remote("titan.picoctf.net", 55341)

password = open("password.enc", "rb").read()

dec = b"decrypted ciphertext as hex (c ^ d mod n): "
enc = b"ciphertext (m ^ e mod n) "

con.sendline(b'e')
con.sendlineafter(b"keysize): ",long_to_bytes(2))
con.recvuntil(enc)
chosen_ciphertext = con.recvline().strip() 
con.sendline(b'd')
con.sendlineafter(b"decrypt: ", str((int(chosen_ciphertext) * int(password))).encode())
con.recvuntil(dec)
chosen_ciphertext_result = con.recvline().strip()
plain_password = long_to_bytes(int(chosen_ciphertext_result,16)//2)
print(plain_password)

cmd = "openssl enc -aes-256-cbc -d -in secret.enc".split(" ")
process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
# Send password to stdin and get output
output, error = process.communicate(input=plain_password)
print(output)

# This challenges takes advantage of the multiplicative property of RSA, aswell as the exponent property
# since C = m^e mod N, and m = C^d mod N, then (m^e)^d = m and equally (C^d)^e = C. This is because
# e*d = 1 mod N. 

# So, in this challenge we have  the encrypted password, lets say Enc(P), we can't decrypt Enc(P), but we can decrypt a modified
# version of it. Let's take a chosen plaintext M. If we find Enc(M), we can multiply to get Enc(M) * Enc(P).
# This is equal to getting Enc(M*P) according to multiplicative property. And since M*P is not P, we can decrypt it using the oracle
# to get M*P. Now we get P from M*P/M. And thus we recovered the password 
   