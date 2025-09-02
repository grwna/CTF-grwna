import struct

header = b"cIMG"
version = struct.pack("<H", 2)

w = 2
h = 2

width = struct.pack("<B", w)
height = struct.pack("<B", h)
payload = header+version+width+height
# char desired_output[] = "\x1b[38;2;184;244;119mc\x1b[0m\x1b[38;2;061;136;031mI\x1b[0m\x1b[38;2;072;235;041mM\x1b[0m\x1b[38;2;243;117;197mG\x1b[0m\x00";
payload = payload + b"\xb8\xf4\x77c"
payload = payload + b"\x3d\x88\x1fI"
payload = payload + b"\x48\xeb\x29M"
payload = payload + b"\xf3\x75\xc5G"
open("mm.cimg", "wb").write(payload)
