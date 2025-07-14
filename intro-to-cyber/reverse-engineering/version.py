# Example of the version challenge, the rest is more or less similar

import struct

header = b"[M4G"
version = struct.pack("<Q", 1)
width = b"\x0e"
height = struct.pack("<H", 40)
payload = header+version+height+width
payload = payload + b"A"*1000
open("mm.cimg", "wb").write(header+version+height+width)
