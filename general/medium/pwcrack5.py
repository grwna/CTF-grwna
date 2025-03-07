import hashlib

pos_pw_list = [pw.strip() for pw in open('dictionary.txt', 'r').readlines()]

def hash_pw(pw_str):
    pw_bytes = bytearray()
    pw_bytes.extend(pw_str.encode())
    m = hashlib.md5()
    m.update(pw_bytes)
    return m.digest()

pw_hash = open("level5.hash.bin", "rb").read()

for pw in pos_pw_list:
    if(hash_pw(pw) == pw_hash):
        print(pw)
        # 7e5f
# picoCTF{h45h_sl1ng1ng_40f26f81}