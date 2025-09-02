import struct
payload = struct.pack("<I", 0xd96bfa2b) # 15.0
# payload = struct.pack("<I", 0xccdaa66b)  # 15.1
open("payload", "wb").write(payload)

"""
Just debug memcmp bro. 
if stripped, run -> ctrl+c -> info file and get the entrypoint address, then 
double check assembly using ghidra  
No explicit Flag output, but using the interpreter it basically does the same things
"""