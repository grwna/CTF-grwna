from pwn import *
from sage.all import *
from grwnapy.crypto.math import long_to_bytes

# Very large e causes a very small d, this is vulnerable to wiener's attack
# Which uses continued fractions to approximate d
# CHeck this https://ir0nstone.gitbook.io/crypto/rsa/public-exponent-attacks/wieners-attack 

def wiener(e,n,c):
    en = (ZZ(e)/ZZ(n))

    # Note: this solution is very inefficient, there are many steps you can take
    # to make wiener's attack more efficient, but this is easier to understand :)
    frac = en.continued_fraction()
    frac_con = frac.convergents()

    for con in frac_con:
        cand_d = con.denominator()

        try: 
            pt = long_to_bytes((pow(c,cand_d,n)))
            if b"pico" in pt:
                print((pt))
        except:
            pass

con = remote("mercury.picoctf.net",37455)
con.recvuntil(b"e: ")
e = con.recvuntil(b"n: ")[:-3].strip()
n = con.recvuntil(b"c: ")[:-3].strip()
c = con.recvline().strip()

wiener(int(e),int(n),int(c))
