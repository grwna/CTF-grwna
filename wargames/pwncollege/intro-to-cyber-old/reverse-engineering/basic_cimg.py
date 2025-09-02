import struct

header = b"cIMG"
version = struct.pack("B", 2)

w = 39
h = 21

width = struct.pack("<B", w)
height = struct.pack("<I", h)
payload = header+version+width+height
payload = payload + b"\x8c\x1d\x40\x24"*(w*h)
open("mm.cimg", "wb").write(payload)
