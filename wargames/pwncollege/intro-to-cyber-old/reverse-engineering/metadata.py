# Example of the version challenge, the rest is more or less similar

import struct

version = struct.pack("<Q", 1)
open("version.cimg", "wb").write(b"[M4G"+version)
