from cryptography import x509
from cryptography.hazmat.backends import default_backend
from Crypto.PublicKey import RSA
from grwnapy.crypto.math import factor

with open("cert", 'rb') as cert:
    cert = x509.load_pem_x509_certificate(cert.read(), default_backend())

public_keys = cert.public_key().public_numbers()
N = public_keys.n
e = public_keys.e

p, q = factor(N)

print("picoCTF{" + f"{q},{p}" "}")