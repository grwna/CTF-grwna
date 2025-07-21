expected = list(bytes.fromhex("9dff3b3d0cf449f28aa9e13f31393f066dd343564d0a0050be2a3bc7c8eb3cce58a4cbe89c"))
l = len(expected)

# Flow (this process is reversed in this script)
# REVERSE
# REVERSE
# XOR with 7 bytes
# CONCAT
# REVERSE
# CONCAT
# XOR with 6 bytes 

for i in range(l):
    match i % 6:
        case 0:
            expected[i] = expected[i] ^ 0xf5
        case 1:
            expected[i] = expected[i] ^ 0x84
        case 2:
            expected[i] = expected[i] ^ 0xf7
        case 3:
            expected[i] = expected[i] ^ 99
        case 4:
            expected[i] = expected[i] ^ 0xa7
        case 5:
            expected[i] = expected[i] ^ 0x91

# GHIDRA is the most accurate in terms of index
var_18 = 0x38-0x18+2
var_20 = 0x38-0x20+7
var28 = 0x38-0x28+6


temp = expected[var28]
expected[var28] = expected[var_18]
expected[var_18] = temp

expected.reverse()

temp = expected[var28]
expected[var28] = expected[var_20]
expected[var_20] = temp

for i in range(l):
    match i % 7:
        case 0:
            expected[i] = expected[i] ^ 0xf
        case 1:
            expected[i] = expected[i] ^ 3
        case 2:
            expected[i] = expected[i] ^ 0xd3
        case 3:
            expected[i] = expected[i] ^ 0xa0
        case 4:
            expected[i] = expected[i] ^ 0xc6
        case 5:
            expected[i] = expected[i] ^ 0x2c
        case 6:
            expected[i] = expected[i] ^ 0xaf

print(''.join([chr(i) for i in expected]))