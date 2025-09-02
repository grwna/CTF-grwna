import random

# Flag is in the format FLAG{}

p128 = 2**128 - 2**97 - 1
a128 = -3
b128 = int("E87579C11079F43DD824993C2CEE5ED3", 16)

G128 = (
    int("6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296", 16),
    int("4FE342E2FE1A7F9B8EE7EB4A7C0F9E162CBCE33576B315ECECBB6406837BF51F", 16)
)

class ECC:
    def __init__(self, a=a128, b=b128, p=p128):
        """
        Elliptic curve: y^2 = x^3 + ax + b (mod p).
        """
        self.a = a
        self.b = b
        self.p = p

    def is_on_curve(self, x, y):
        return (y**2 - (x**3 + self.a * x + self.b)) % self.p == 0


def point_addition(P, Q, curve):
    if P is None: return Q
    if Q is None: return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2:
        if (y1 != y2): return None
        else: return point_doubling(P, curve)
    
    m = ((y2 - y1) * pow(x2 - x1, -1, curve.p)) % curve.p
    x3 = (m**2 - x1 - x2) % curve.p
    y3 = (m * (x1 - x3) - y1) % curve.p
    return (x3, y3)


def point_doubling(P, curve):
    if P is None: return None
    
    x, y = P

    m = ((3 * x**2 + curve.a) * pow(2 * y, -1, curve.p)) % curve.p
    x3 = (m**2 - 2 * x) % curve.p
    y3 = (m * (x - x3) - y) % curve.p
    return (x3, y3)


def scalar_multiplication(k, P, curve):
    """
    k * P on the elliptic curve using the double-and-add algorithm.
    """
    if k == 0 or P is None:  return None

    result = None
    addend = P

    while k:
        if k & 1:
            result = point_addition(result, addend, curve)
        addend = point_doubling(addend, curve)
        k >>= 1  

    return result


def generate_keys(curve, G=G128):
    # Private key
    d = random.randint(1, curve.p - 1)
    
    # Public key
    Q = scalar_multiplication(d, G, curve)
    
    return d, Q


def encrypt(plaintext, public_key, curve, G=G128):
    k = random.randint(1, curve.p - 1)
    C1 = scalar_multiplication(k, G, curve)
    kQ = scalar_multiplication(k, public_key, curve)
    
    shared_x = kQ[0] 
    ciphertext_list = [str(ord(M) + shared_x) for M in plaintext]
    ciphertext = ' '.join(ciphertext_list)
    return C1, ciphertext


def decrypt_ecc(ciphertext, R, private_key, curve):
    kQ = scalar_multiplication(private_key, R, curve)
    
    shared_x = kQ[0]
    ciphertext_list = list(map(int, ciphertext.split()))
    plaintext_list = [chr(char - shared_x) for char in ciphertext_list]
    plaintext = ''.join(plaintext_list)
    return plaintext

if __name__=="__main__":
    ecc = ECC()
    private, public = generate_keys(ecc)
    C1, C2 = encrypt("REDACTED", public, ecc)
    with open("flag.txt", "w") as f:
        f.write(f"C1: {C1}")
        f.write(f"\n")
        f.write(f"Ciphertext: {C2}")