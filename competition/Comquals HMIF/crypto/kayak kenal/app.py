from flask import Flask
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

app = Flask(__name__)
KEY = os.urandom(16)


@app.route("/get-flag")
def get_flag():
    with open("flag.txt", "rb") as f:
        flag = f.read().strip()
    assert len(flag) == 67
    cipher = AES.new(KEY, AES.MODE_CBC)
    ct = cipher.decrypt(pad(flag, 16))
    encrypted_flag = (cipher.iv + ct).hex()
    return {"flag": encrypted_flag}


@app.route("/encrypt/<plaintext>")
def encrypt_route(plaintext):
    plaintext = bytes.fromhex(plaintext)
    cipher = AES.new(KEY, AES.MODE_CBC)
    ct = cipher.decrypt(pad(plaintext, 16))
    encrypted_message = (cipher.iv + ct).hex()
    return {"encrypted_message": encrypted_message}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8765)
