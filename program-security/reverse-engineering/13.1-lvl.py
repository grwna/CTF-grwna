import YAN86 as yan
import struct

"""
Difficulty of this challenge stems from re-coding the YAN86 emulator. (Read: YAN86.py)
"""

param_1 = 0

yan.interpret_imm(param_1,0x10,0x8c)
yan.interpret_imm(param_1,1,1)
yan.interpret_imm(param_1,2,0x1a)
yan.interpret_stm(param_1,0x10,2)
yan.interpret_add(param_1,0x10,1)
yan.interpret_imm(param_1,2,0xe7)
yan.interpret_stm(param_1,0x10,2)
yan.interpret_add(param_1,0x10,1)
yan.interpret_imm(param_1,2,0xc1)
yan.interpret_stm(param_1,0x10,2)
yan.interpret_add(param_1,0x10,1)
yan.interpret_imm(param_1,2,0x3c)
yan.interpret_stm(param_1,0x10,2)
yan.interpret_add(param_1,0x10,1)
yan.interpret_imm(param_1,2,0xec)
yan.interpret_stm(param_1,0x10,2)
yan.interpret_add(param_1,0x10,1)
yan.interpret_imm(param_1,2,0xbc)
yan.interpret_stm(param_1,0x10,2)
yan.interpret_add(param_1,0x10,1)
yan.interpret_imm(param_1,2,0x89)
yan.interpret_stm(param_1,0x10,2)
yan.interpret_add(param_1,0x10,1)
yan.interpret_imm(param_1,2,0xf0)
yan.interpret_stm(param_1,0x10,2)
yan.interpret_add(param_1,0x10,1)

print(yan.global_buffer[0x8c:0x8c+8])

payload = b''.join([struct.pack("B", byte) for byte in yan.global_buffer[0x8c:0x8c+8]])
print(payload)
open("payload", "wb").write(payload)