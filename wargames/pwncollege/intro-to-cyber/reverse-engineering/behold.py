import struct

header = b"cIMG"
version = struct.pack("<Q", 1)

w = 59
h = 17

width = struct.pack("<I", w)
height = struct.pack("<I", h)
payload = header+version+width+height
payload = payload + b"A"*(w*h*100)
open("mm.cimg", "wb").write(payload)
