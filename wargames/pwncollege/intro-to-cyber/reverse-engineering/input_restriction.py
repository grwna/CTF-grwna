# Example of the version challenge, the rest is more or less similar


header = b"cIMG"
version = struct.pack("<I", 1)
width = b"\x50"
height = b"\x0d"
payload = header+version+height+width
payload = payload + b" "*1000
open("mm.cimg", "wb").write(payload)
