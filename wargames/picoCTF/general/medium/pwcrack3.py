import hashlib

pos_pw_list = ["6997", "3ac8", "f0ac", "4b17", "ec27", "4e66", "865e"]

def hash_pw(pw_str):
    pw_bytes = bytearray()
    pw_bytes.extend(pw_str.encode())
    m = hashlib.md5()
    m.update(pw_bytes)
    return m.digest()

pw_hash = open("level3.hash.bin", "rb").read()

for pw in pos_pw_list:
    if(hash_pw(pw) == pw_hash):
        print(pw)
        # 865e
        # input this into the password checker

# picoCTF{m45h_fl1ng1ng_2b072a90}