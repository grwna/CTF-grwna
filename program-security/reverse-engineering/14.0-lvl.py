import struct
payload = struct.pack("<Q", 0xa871461ac1553ac9) # 14.0
payload = struct.pack("<I", 0xccdaa66b)  # 14.1
open("payload", "wb").write(payload)

"""
Just debug memcmp bro. if stripped, double check assembly using ghidra  
"""