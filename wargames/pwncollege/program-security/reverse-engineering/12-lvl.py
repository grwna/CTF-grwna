import struct
payload = struct.pack(">Q",0x3d4e364dc3540000)
open("payload", "wb").write(payload)


"""
This challenge claims to be the start of an emulator, but this one is a simple decompile read

Things To Remind myself
- GDB displays native CPU data (in little endian)
- Struct Packing Bytes Padding
"""