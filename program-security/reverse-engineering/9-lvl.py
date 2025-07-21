# Interesting challenge, new concept
# The crux of this challenge is, the code is made modifiable using mmap
# This causes it to be able to be modified during runtime
# So opcodes of assembly can be modified to any other opcodes (in this challenge 5 bytes)

# This makes it possible to skip a jmp or other conditionals

base = 0x100000
edit_location = 0x1028d5
offset = edit_location - base
print(hex(offset))

"""
In ghidra this is the conditionals that skips win()

        001028d5 75  14           JNZ        LAB_001028eb
        001028d7 b8  00  00       MOV        EAX ,0x0
                 00  00

we want to change three bytes to NOP, or one byte to make JZ (74) instead,
Since challenge 10.0 only allows patching 1 byte, im just going to patch to JZ instead.

NOTE: the location might be different, but it is trivial to locate the address so 
i won't bother being accurate with them
"""