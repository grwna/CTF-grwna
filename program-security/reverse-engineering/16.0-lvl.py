"""
Let's continue deeper in reverse engineering obfuscated code! This challenge is using VM-based obfuscation: reverse engineer the custom emulator and architecture to understand how to get the flag!

This challenge is done by painstakingly debugging using gdb. Breakpoint on each interpret_cmp then examining what values are being compared.
"""

import struct
# payload = struct.pack(">Q", 0x634601caa6638759)     # 16.0
payload = struct.pack(">Q", 0xd653bcf178f88467)     # 16.1
print(payload)
open("payload", "wb").write(payload)

"""
The payload is read from these instructions (for 16.0) or use gdb if you like

   interpret_imm(param_1,1,99);
   interpret_stm(param_1,4,1);
   interpret_add(param_1,4,0x20);
   interpret_imm(param_1,1,0x46);
   interpret_stm(param_1,4,1);
   interpret_add(param_1,4,0x20);
   interpret_imm(param_1,1,1);
   interpret_stm(param_1,4,1);
   interpret_add(param_1,4,0x20);
   interpret_imm(param_1,1,0xca);
   interpret_stm(param_1,4,1);
   interpret_add(param_1,4,0x20);
   interpret_imm(param_1,1,0xa6);
   interpret_stm(param_1,4,1);
   interpret_add(param_1,4,0x20);
   interpret_imm(param_1,1,99);
   interpret_stm(param_1,4,1);
   interpret_add(param_1,4,0x20);
   interpret_imm(param_1,1,0x87);
   interpret_stm(param_1,4,1);
   interpret_add(param_1,4,0x20);
   interpret_imm(param_1,1,0x59);
"""