"""
Let's continue deeper in reverse engineering obfuscated code! This challenge is using VM-based obfuscation: reverse engineer the custom emulator and architecture to understand how to get the flag!

Understand teh interpret functions, it is actually not that difficult to do these challenges
"""

import struct
payload = struct.pack(">Q", 0x1ba9e61b39303bc8)  + struct.pack(">I",0xb01ea990)  # 17.0
# payload = struct.pack(">Q", 0xd653bcf178f88467)     # 17.1
print(payload)
open("payload", "wb").write(payload)

"""
The payload is read from these instructions (for 17.0) or use gdb if you like
"""